# -*- coding: utf-8 -*-
__author__ = 'mariosky'

import json
import os
import time


from redis_cola import Cola, Task

server = Cola("python")

code = """
def suma(a,b):
    return a+b
"""

test= u"""
class Test(unittest.TestCase):
    def setUp(self):
        pass
    def test_Action(self):
        self.assertEqual(add( 1, 3)), 4)"""


def put():
    task = {"id": None, "method": "exec", "params": {"code": code, "test": test}}
    print task
    task_id = server.enqueue(**task)
    return task_id


def get(t_id,lang):
    t = Task(id=t_id)
    t.get_result(lang)
    if t.result:
        return t.result
        #return json.loads( t.result[0])
    else:
        return "Snif"


tid = put()
print tid
time.sleep(4)
print get(tid,'python')


server = Cola("perl6")

code = """
    sub add($a, $b) {
        say "Hi";
        return $a+$b;
    }
"""

test = """
# .... tests
is add(6,1),          7, 'Suma dos enteros';
is add(6,1),          5, 'Suma dos enteros error';
"""

tid = put()
print tid
time.sleep(6)
print get(tid,'perl6')





