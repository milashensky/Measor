import os
import docker


def init_docker(settings):
    client = docker.from_env()
    path = os.path.join(settings['BASE_DIR'], 'container')
    try:
        c = client.containers.get('measor_tasks_runner')
        c.kill()
        c.remove()
    except docker.errors.APIError:
        pass

    image = client.images.list()[0]
    volume = {settings['TASKS_DIR']: {'bind': '/home/tasks', 'mode': 'rw'}}
    container = client.containers.run(image, volumes=volume, name="measor_tasks_runner", detach=True)
    f = open(path, 'w')
    f.write(container.id)
    f.close()
    return container
