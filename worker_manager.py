
import docker
import os
import time
import sys, getopt

from tester.Redis_Cola import Cola

LANGS = ["csharp","python","java"]

argv =sys.argv[1:]
ip = ""
dC = None

if argv:
    try:
        opts, args = getopt.getopt(argv,"i:",["ip="])
    except getopt.GetoptError:
        print 'test.py -i <ip>'
        sys.exit(2)

    ip = opts[0][1]
    import docker.tls as tls
    from os import path

    CERTS = path.join(path.expanduser('~'), '.docker', 'machine', 'machines', 'sandmanbox')

    tls_config = tls.TLSConfig(
        client_cert=(path.join(CERTS, 'cert.pem'), path.join(CERTS,'key.pem')),
        ca_cert=path.join(CERTS, 'ca.pem'),
        verify=True
        )
    dC = docker.Client(base_url='https://sandman:2376', tls=tls_config)
else:
    dC = docker.Client(base_url='unix://var/run/docker.sock', version="auto", timeout=60)





BASE_IMAGE = 'mariosky/sandbox_worker:latest'


def create_worker(env):
    # TODO catch ContainerError - requests.exceptions.ConnectionError
    container = make_container(env)
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


#memlimit moved
#mem_limit=6291456,

def make_container(env):
    command="python /home/sandbox/worker.py %s "
    return dC.create_container( BASE_IMAGE, environment=env ,command=command,  labels={'worker':env['LANG'] } ,ports={"6666/tcp": {}})


def start(cont):
    dC.start(cont['Id'], port_bindings={"6666/tcp": [{'HostIp': '', 'HostPort': ''}]})


def kill_all():
    for lang , container in get_containers('worker'):
        print "Killing: ", container
        dC.kill(container)


def remove_all():
    for lang , container in get_containers('worker', all=True):
        print "Removing: ", container
        dC.remove_container(container)


def get_containers(label='worker', all=False):
    return [ (container['Labels'][label], container['Id'][:12] ) for container in dC.containers(all=all) if label in container['Labels'] ]




if __name__ == "__main__":
    kill_all()
    remove_all()
    colas = [Cola(name)for name in LANGS]
    for cola in colas:
        print "Init Queue:", cola.app_name
        print create_worker({'LANG':cola.app_name, 'REDIS_HOST':os.environ['REDIS_HOST']})
        print create_worker({'LANG':cola.app_name, 'REDIS_HOST':os.environ['REDIS_HOST']})
        time.sleep(4)
    while True:
        time.sleep(1)
        containers = get_containers()
        workers = [ w.split(':worker:') for w in Cola.get_all_workers()]
        for c_lang, c_id in containers:


            if c_id not in [w_id for w_lang, w_id  in workers]:
                print "Killing: ", c_id, c_lang
                dC.kill(c_id)
                dC.remove_container(c_id)
                print "Removing: ", c_id

                print create_worker({'LANG':c_lang, 'REDIS_HOST':os.environ['REDIS_HOST']})


