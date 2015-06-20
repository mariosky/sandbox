
import docker
import os
import time
from tester.Redis_Cola import Cola

LANGS = ["csharp","python"]

dC = docker.Client(base_url='unix://var/run/docker.sock', version="1.6", timeout=60)
BASE_IMAGE = 'mariosky/sandbox_worker'


def create_worker(conf):
    # TODO catch ContainerError - requests.exceptions.ConnectionError
    container = make_container(conf)
    start(container)
    return container


class ContainerException(Exception):
    """
    There was some problem generating or launching a docker container
    for the user
    """
    pass


class ImageException(Exception):
    """
    There was some problem reading image
    """
    pass


def get_image(image_name=BASE_IMAGE):
    # TODO catch ConnectionError - requests.exceptions.ConnectionError
    for image in dC.images():
        if image['Repository'] == image_name and image['Tag'] == 'latest':
            return image
    raise ImageException()
    return None



def make_container(env):
    command="python /home/sandbox/worker.py %s "
    return dC.create_container( get_image()['Id'], environment=env ,command=command, mem_limit=6291456, labels={'worker':1} ,ports={"6379/tcp": {}})


def start(cont):
    dC.start(cont['Id'], port_bindings={"6379/tcp": [{'HostIp': '', 'HostPort': ''}]})


def kill_all(image=BASE_IMAGE):
    for container in get_containers(image):
        print "Killing: ", container
        dC.kill(container)


def get_containers(image=BASE_IMAGE):
    return [ container['Id'][:12] for container in dC.containers() if container['Image'].split(':')[0] == image ]


if __name__ == "__main__":
    kill_all()
    colas = [Cola(name)for name in LANGS]
    for cola in colas:
        print "Init Queue", cola.app_name
        print create_worker({'LANG':cola.app_name, 'REDIS_HOST':os.environ['REDIS_HOST']})
        print create_worker({'LANG':cola.app_name, 'REDIS_HOST':os.environ['REDIS_HOST']})
    time.sleep(4)
    while True:
        time.sleep(1)
        containers = get_containers(BASE_IMAGE)
        workers = Cola.get_all_workers()
        # w (0=lang;1=worker;2=id)
        print containers
        print workers

        #for c in containers:
        #    if c not in [w[1] for w in workers]:
        #        print "Killing: ", c
        #        dC.kill(c)
        #        print create_worker({"lang":w[0]})


