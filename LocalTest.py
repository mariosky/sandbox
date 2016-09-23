# -*- coding: utf-8 -*-
__author__ = 'mariosky'

import os
import json


print os.environ['REDIS_HOST']
print os.environ['LANG']

from tester.Redis_Cola import Cola, Task

server = Cola("python")

code = """def producto(l1,l2):
    pass"""



test= u"""import sys
import unittest
import json

class ResultadoPrueba(unittest.TestResult):
    def __init__(self):
         super(ResultadoPrueba, self).__init__()
         self.success = []
    def addSuccess(self, test):
         self.success.append(test)
    def shouldStop(self, test):
         return False


class Test(unittest.TestCase):
    def setUp(self):
        pass
    def test_Action(self):
        self.assertEqual(producto([2, 1, 3], [2, 3, 1]), 10)"""



def put():
    task = {"id": None, "method": "exec", "params": {"code": code, "test": test}}
    print task
    task_id = server.enqueue(**task)
    return task_id


def get(t_id):
    t = Task(id=t_id)
    t.get_result('python')
    if t.result:
        return t.result
        return json.loads( t.result[0])
    else:
        return "Snif"
tid = put()
print tid

for i in range(500):
    print get(tid)
