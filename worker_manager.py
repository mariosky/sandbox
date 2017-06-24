import os
import sys
import time

import docker

print docker.version

from redis_cola import Cola
from settings import *



dC = docker.DockerClient(base_url='unix://var/run/docker.sock', version="auto", timeout=60)



def create_worker(env, language ):
    # TODO catch ContainerError - requests.exceptions.ConnectionError
    container = make_container(env, language)
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


def make_container(env, language):
    return dC.containers.create(settings[language]["image"], environment=env ,command = settings[language]["command"],  labels= {'worker': language })


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
    colas = [(Cola(language),settings[language]["containers"]) for language  in settings.keys()]

    for (cola, number)  in colas:
        print "Init Queue:", cola.app_name
        for i in range(number):
            create_worker({'PL':cola.app_name,'REDIS_HOST':os.environ['REDIS_HOST'], 'REDIS_PORT':os.environ['REDIS_PORT']}, language=cola.app_name)
            print cola.app_name, {'PL':cola.app_name,'REDIS_HOST':os.environ['REDIS_HOST'], 'REDIS_PORT':os.environ['REDIS_PORT']}
        time.sleep(4)
    while True:
        ## Time between checks
        time.sleep(2)
        containers = get_containers()
        workers = [ w.split(':worker:') for w in Cola.get_all_workers()]

        for container in containers:
            if container.short_id not in [w_id for w_lang, w_id  in workers]:
                print "Killing: ", container.short_id
                container.kill()
                container.remove()
                print "Removing: ", container.short_id
                print create_worker({'PL': container.labels['worker'],'REDIS_HOST':os.environ['REDIS_HOST'], 'REDIS_PORT':os.environ['REDIS_PORT']}, language=container.labels['worker'])
                time.sleep(4)


