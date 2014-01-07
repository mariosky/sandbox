
from eval_py.Redis_Cola import Cola, Task, Worker

from eval_py.apply_test import exec_sandbox

import uuid
import time

test = '''
import sys
import unittest

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



server = Cola("curso")


## Each Worker
worker = Worker(uuid.uuid4(), server)

while True:
    t = worker.pull_task()

    if (t):
        code = t.params['code']
        t.result = exec_sandbox(code,test)
        t.put_result(worker)
    else:
        pass

    worker.send_heartbeat()



