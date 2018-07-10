import os
import shutil
import json
import datetime
import time
import threading
import subprocess

# path = '/home/milash/work/smappi/Measor/tasks'
path = "/home/tasks"
CHECK_TIME = 20

dirs = list(os.walk(path))[0][1]
tasks = {}
threads = {}

intervals = (
    (0, 1),
    (1, 60),
    (2, 3600),
    (3, 3600 * 24),
)


def prepare_tasks(dirs):
    tmp_tasks = {}
    for dir in dirs:
        try:
            f = open(os.path.join(path, dir, 'conf.json'), 'r')
            data = json.loads(f.read())
            f.close()
            tmp_tasks[dir] = data
        except FileNotFoundError:
            pass
    return tmp_tasks


def exec_taskfile(dirpath):
    status = True
    if not os.path.exists(os.path.join(dirpath, 'logs')):
        os.makedirs(os.path.join(dirpath, 'logs'))
    ts = round(datetime.datetime.now().timestamp())
    try:
        f = open(os.path.join(dirpath, 'logs', 'log%s.txt' % ts), 'w', encoding='utf-8')
        try:
            st = subprocess.call(['python3', os.path.join(dirpath, "task.py")], stdout=f, stderr=f)
            if not st == 0:
                status = False
            else:
                f.write('\nsuccess')
        except Exception as e:
            f.write('error while exicution\n')
            f.write(str(e))
            status = False
        f.close()
    except PermissionError:
        status = False
    return status


def run_task(dir, task):
    if not task.get('pause', False) or task.get('build_now', False):
        dirpath = os.path.join(path, dir)
        f = open(os.path.join(dirpath, 'running'), 'w')
        t_start = datetime.datetime.now().timestamp()
        f.write('%s' % t_start)
        f.close()
        status = exec_taskfile(dirpath)
        # print('start run %s' % task['name'])
        time.sleep(5)
        # print('sleep %s' % task['name'])
        os.remove(os.path.join(dirpath, 'running'))

        f = open(os.path.join(dirpath, 'conf.json'), 'r')
        t_end = datetime.datetime.now().timestamp()
        try:
            task = json.loads(f.read())
        except ValueError:
            pass
        f.close()
        task['last_run'] = t_end
        task['last_duriation'] = round(t_end - t_start)
        task['last_status'] = status
        f = open(os.path.join(dirpath, 'conf.json'), 'w')
        f.write(json.dumps(task))
        f.close()


def runner(dir, task, *args, **kwargs):
    t = threading.currentThread()
    # print('new thread %s' % task['name'])
    while getattr(t, "do_run", True):
        try:
            interval = int(task.get('interval')) * intervals[int(task.get('interval_units'))][1]
            run_task(dir, task)
            sleep = 0
            while getattr(t, "do_run", True) and sleep < interval:
                time.sleep(2)
                sleep += 2
        except FileNotFoundError:
            pass
    # print('stop run %s' % task['name'])


def clean_logs(task):
    max_log_life = task.get('max_log_life', 0)
    max_logs_count =  task.get('max_logs_count', 0)
    logs_path = os.path.join(path, task['slug'], 'logs')
    if os.path.exists(logs_path) and (max_log_life or max_logs_count):
        try:
            logs_names = list(os.walk(logs_path))[0][2]
            logs_names.sort()
            if max_log_life:
                max_date = datetime.datetime.now() - datetime.timedelta(int(max_log_life))
                max_date = max_date.timestamp()
                for name in logs_names:
                    date = int(name.split('log')[1].split('.')[0])
                    if date - max_date < 0:
                        try:
                            os.remove(os.path.join(logs_path, name))
                        except OSError:
                            pass
                logs_names = list(os.walk(logs_path))[0][2]
                logs_names.sort()
            del_l = len(logs_names) - int(max_logs_count)
            if max_logs_count and del_l > 0:
                to_delete = logs_names[:del_l]
                for name in to_delete:
                    try:
                        os.remove(os.path.join(logs_path, name))
                    except OSError:
                        pass
        except IndexError:
            return True
    return True


# main task
try:
    try:
        tasks = prepare_tasks(dirs)
        for dir, task in tasks.items():
            thread = threading.Thread(
                target=runner,
                args=[dir, task],
                daemon=True
            )
            thread.start()
            threads[dir] = thread
        while True:
            time.sleep(CHECK_TIME)
            dirs = list(os.walk(path))[0][1]
            new_tasks = prepare_tasks(dirs)
            old_tasks = tasks.copy()
            tasks = new_tasks.copy()
            for name, task in new_tasks.items():
                changed = delete = False
                delete = task.get('wait_for_delete', False)
                if not delete:
                    clean_logs(task)
                old_task = old_tasks.pop(name, None)
                if old_task and not delete:
                    if task.get('build_now', False):
                        print('build_now')
                        changed = True
                    else:
                        for key, val in old_task.items():
                            if key not in ['last_run', 'last_status']:
                                if not task[key] == val:
                                    changed = True
                                    break
                    if changed:
                        print('run changed %s', task.get('name'))
                        t = threads.get(name, None)
                        if t:
                            t.do_run = False
                            t.join()
                            threads[name] = None
                        if not task.get('pause', False) and not delete:
                            print('gonna runs', task.get('slug'))
                            t2 = threading.Thread(
                                target=runner,
                                args=[task.get('slug'), task],
                                daemon=True
                            )
                            t2.start()
                            threads[name] = t2
                        else:
                            print('task is paused %s', task.get('name'))
                else:
                    t = threads.get(name, None)
                    if t:
                        t.do_run = False
                        t.join()
                        threads[name] = None
                    if not task.get('pause', False) and not delete:
                        t2 = threading.Thread(
                            target=runner,
                            args=[task.get('slug'), task],
                            daemon=True
                        )
                        t2.start()
                        threads[name] = t2
                    else:
                        print('task is paused %s', task.get('name'))
                if changed and not delete:
                    task['build_now'] = False
                    f = open(os.path.join(path, task.get('slug'), 'conf.json'), 'w')
                    f.write(json.dumps(task))
                    f.close()
                if delete:
                    shutil.rmtree(os.path.join(path, task.get('slug')))
            for name, task in old_tasks.items():
                t = threads.get(name, None)
                if t:
                    t.do_run = False
                    t.join()
                threads[name] = None
        # endwhile
    except (KeyboardInterrupt, SystemExit):
        raise
except:
    pass
