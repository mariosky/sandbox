
import docker
import time
from tester.Redis_Cola import Cola

LANGS = ["csharp","python"]


dC = docker.Client(base_url='unix://var/run/docker.sock', version="1.6", timeout=60)
BASE_IMAGE = 'mariosky/sandbox_worker'




def create_worker(params):
    cont = make_container()
    start(cont)
    return cont


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


def make_container(command = "python /home/sandbox/worker.py"):
    return dC.create_container( get_image()['Id'], command=command, mem_limit=6291456, ports={"6379/tcp": {}})


def start(cont):
    dC.start(cont['Id'], port_bindings={"6379/tcp": [{'HostIp': '', 'HostPort': ''}]})

def kill_all(image=BASE_IMAGE):
    for c in get_containers(image):
        print "Killing: ", c
        dC.kill(c)


def get_containers(image=BASE_IMAGE):
    return [ c['Id'][:12] for c in dC.containers() if c['Image'].split(':')[0] == image ]


if __name__ == "__main__":
    kill_all()
    servers = [Cola(name)for name in LANGS]
    for s in servers:
        print "Init Queue", s.app_name
        print create_worker()
    print create_worker()
    time.sleep(4)
    while True:
        time.sleep(1)
        containers = get_containers(BASE_IMAGE)
        workers = [ w.split(":")[2] for w in server.get_workers()]
        for c in containers:
            if c not in workers:
                print "Killing: ", c
                dC.kill(c)
                print create_worker()


