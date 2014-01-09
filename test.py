from flask import Flask, render_template, request, jsonify ,json

from eval_py.apply_test import exec_sandbox
from eval_py.Redis_Cola import Cola, Task
import docker
import requests


dC = docker.Client(base_url='unix://var/run/docker.sock', version="1.6", timeout=60)
BASE_IMAGE = 'mariosky/sandbox_worker'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test_execute.html')


@app.route('/_execute', methods=['POST'])
def execute():
    rpc = request.json
    code = rpc["params"][0]
    out = exec_sandbox(code,test)
    return jsonify(result=out)


@app.route('/_execute_sandboxed', methods=['POST'])
def execute_sand(code=None):
    dC = docker.Client(base_url='unix://var/run/docker.sock', version="1.6", timeout=60)
    rpc = request.json
    code = rpc["params"][0]

    data = {"jsonrpc": "2.0", "method": "_execute", "params": [code], "id": 1 }
    cont = make_container()
    start(cont)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    port = dC.inspect_container(cont)['NetworkSettings']['Ports']['5000/tcp'][0]['HostPort']
    url = "http://127.0.0.1:%s/_execute" % (port)
    while dC.logs(cont) == "":
        print dC.logs(cont)
        print "waiting..."
    r = None
    try:
         r = requests.post(url, data=json.dumps(data), headers=headers)
    except Exception:
        print Exception.message

    return jsonify(r.json())


@app.route('/_execute_queue', methods=['POST'])
def _execute_queue(code=None):
    server = Cola("curso")
    #server.initialize()
    rpc = request.json
    code = rpc["params"][0]
    task = {"id": None,"method": "exec","params": {"code": code, "test": test}}
    task_id = server.enqueue(**task)

    result= {"result":"added" , "error": None, "id": task_id}
    return jsonify(**result)



@app.route('/_get_result',methods=['POST'])
def get_result():
    rpc = request.json
    #We only need the Task identifier
    #TO DO:
    # No ID, Task Not Found
    task_id = rpc["id"]
    t = Task(id=task_id)

    # outcome:
    # -1 No result found
    # 0 Sub-process Success
    # 1 Sub-process Failure
    if t.get_result('curso'):
        return jsonify(result=t.result[0], outcome=t.result[1])
    else:
        return jsonify(outcome=-1)


test = '''
import unittest, sys, json

class Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_order(self):
        self.assertEqual(solution([2,6,1,5]),[1,2,5,6])

    def test_none(self):
        self.assertEqual(solution(None),[])

    #def test_hang(self):
    #    self.assertEqual(hang(), None)

class TestFoo(unittest.TestCase):
    def test_foo(self):
        from StringIO import StringIO

        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            foo()
            output = out.getvalue().strip()

            assert output == 'hello world!'
        finally:
            sys.stdout = saved_stdout
            print output


suite = unittest.TestLoader().loadTestsFromTestCase(Test)
test_result = unittest.TextTestRunner(verbosity=2, stream=sys.stderr).run(suite)
'''

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


def make_container():
    return dC.create_container( get_image()['Id'], command = "python /home/sandbox/execute_ws.py", ports={"5000/tcp": {}})


def start(cont):
    dC.start(cont['Id'], port_bindings={"5000/tcp": [{'HostIp': '', 'HostPort': ''}]})


if __name__ == "__main__":
    app.run(host='0.0.0.0')