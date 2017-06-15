import os
import sys
import time

import docker

print docker.version

from redis_cola import Cola

LANGS = ["csharp"]

argv =sys.argv[1:]
ip = ""

dC = docker.DockerClient(base_url='unix://var/run/docker.sock', version="auto", timeout=60)
BASE_IMAGE = 'mariosky/csharp_tester:latest'


def create_worker(env):
    # TODO catch ContainerError - requests.exceptions.ConnectionError
    container = make_container(env)
    container.start()
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


#memlimit moved
#mem_limit=6291456,

def make_container(env):
    command="python /home/sandbox/worker.py %s "
    return dC.containers.create( BASE_IMAGE, environment=env ,command=command,  labels={'worker':env['LANG'] })


def start(cont):
#   dC.start(cont['Id'], port_bindings={"6666/tcp": [{'HostIp': '', 'HostPort': ''}]})
    dC.start(cont['Id'])




def kill_all():
    for container in get_containers('worker'):
        print "Killing: ", container
        container.kill()


def remove_all():
    for container in get_containers('worker', all=True):
        print "Removing: ", container
        container.remove()



def get_containers(label='worker', all=False):
    return dC.containers.list(all=all, filters={'label': label})


if __name__ == "__main__":
    kill_all()
    remove_all()
    colas = [Cola(name)for name in LANGS]
    for cola in colas:
        print "Init Queue:", cola.app_name
        print create_worker({'LANG':cola.app_name, 'REDIS_HOST':os.environ['REDIS_HOST'], 'REDIS_PORT':os.environ['REDIS_PORT']})
        print create_worker({'LANG':cola.app_name, 'REDIS_HOST':os.environ['REDIS_HOST'], 'REDIS_PORT':os.environ['REDIS_PORT']})
        print {'LANG':cola.app_name, 'REDIS_HOST':os.environ['REDIS_HOST'], 'REDIS_PORT':os.environ['REDIS_PORT']}

        time.sleep(4)
    while True:
        time.sleep(1)
        containers = get_containers()
        workers = [ w.split(':worker:') for w in Cola.get_all_workers()]
        print workers
        print containers
        for container in containers:


            if container.id not in [w_id for w_lang, w_id  in workers]:
                print "Killing: ", container.id
                print container.attrs
                print container.attrs[u'Config']['Labels']
                container.kill()
                container.remove()
                print "Removing: ", container.id
                print create_worker({'LANG':container.labels['worker'], 'REDIS_HOST':os.environ['REDIS_HOST'], 'REDIS_PORT':os.environ['REDIS_PORT']})
                time.sleep(4)


