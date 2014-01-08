
import docker
import time
from eval_py.Redis_Cola import Cola


dC = docker.Client(base_url='unix://var/run/docker.sock', version="1.6", timeout=60)
BASE_IMAGE = 'mariosky/sandbox_worker'




def create_worker():
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
    return dC.create_container( get_image()['Id'], command=command , ports={"6379/tcp": {}})


def start(cont):
    dC.start(cont['Id'], port_bindings={"6379/tcp": [{'HostIp': '', 'HostPort': ''}]})



if __name__ == "__main__":
    server = Cola("curso")
    server.initialize()
    print create_worker()
    print create_worker()
    time.sleep(15)
    while True:
        time.sleep(15)
        dead_workers = server.get_dead_workers()
        for w in dead_workers:
            container = w.split(':')[-1]
            print "Killing: ",container
            dC.kill(container)
            print create_worker()


