from eval_py.Redis_Cola import Cola, Task, Worker
from eval_py.apply_test import exec_sandbox

import os


server = Cola("curso")
worker = Worker(os.environ['HOSTNAME'], server)

while True:
    t = worker.pull_task()

    if (t):
        code = t.params['code']
        test = t.params['test']
        t.result = exec_sandbox(code,test)
        t.put_result(worker)
    else:
        pass

    worker.send_heartbeat()



