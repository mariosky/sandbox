from flask import Flask, request, jsonify
from eval_py.apply_test import exec_sandbox

app = Flask(__name__)



@app.route('/_execute', methods=['POST'])
def execute():
    rpc = request.json
    code = rpc["params"][0]
    try:
        out = exec_sandbox(code, test)
    except Exception:
        print Exception.message
    return jsonify(result=out)

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
test_result = unittest.TextTestRunner(descriptions=False, verbosity=0, stream=sys.stderr).run(suite)
'''

if __name__ == "__main__":
    app.run(host='0.0.0.0')
