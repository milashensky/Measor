import os
import shutil
import json
import datetime
import time
import threading
import subprocess

# path = '/home/milash/work/smappi/splinmon/tasks'
path = "/home/tasks"
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
    dirpath = os.path.join(path, dir)
    interval = int(task.get('interval')) * intervals[int(task.get('interval_units'))][1]
    f = open(os.path.join(dirpath, 'running'), 'w')
    t_start = datetime.datetime.now().timestamp()
    f.write('%s' % t_start)
    f.close()
    status = exec_taskfile(dirpath)
    print('start run %s' % task['name'])
    time.sleep(5)
    print('sleep %s' % task['name'])
    os.remove(os.path.join(dirpath, 'running'))
    f = open(os.path.join(dirpath, 'conf.json'), 'w')
    t_end = datetime.datetime.now().timestamp()
    task['last_run'] = t_end
    task['last_duriation'] = round(t_end - t_start)
    task['last_status'] = status
    f.write(json.dumps(task))
    f.close()
    time.sleep(interval)


def runner(dir, task, *args, **kwargs):
    t = threading.currentThread()
    print('new thread %s' % task['name'])
    while getattr(t, "do_run", True):
        try:
            run_task(dir, task)
        except FileNotFoundError:
            pass
    print('stop run %s' % task['name'])


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
            time.sleep(30)
            dirs = list(os.walk(path))[0][1]
            new_tasks = prepare_tasks(dirs)
            old_tasks = tasks.copy()
            for name, task in new_tasks.items():
                old_task = old_tasks.pop(name, None)
                if old_task:
                    changed = False
                    for key, val in old_task.items():
                        if not task[key] == val:
                            changed = True
                            break
                    if changed:
                        t = threads.get(name, None)
                        if t:
                            t.do_run = False
                            t.join()
                        t2 = threading.Thread(
                            target=runner,
                            args=[dir, task],
                            daemon=True
                        )
                        t2.start()
                        threads[name] = t2
                else:
                    t = threads.get(name, None)
                    if t:
                        t.do_run = False
                        t.join()
                    t2 = threading.Thread(
                        target=runner,
                        args=[dir, task],
                        daemon=True
                    )
                    t2.start()
                    threads[name] = t2
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
