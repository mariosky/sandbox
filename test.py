from flask import Flask, render_template, request, jsonify ,json

from eval_py.apply_test import exec_sandbox
from eval_py.Redis_Cola import Cola, Task
import docker
import requests


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test_execute.html')



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

if __name__ == "__main__":
    app.run(host='0.0.0.0')