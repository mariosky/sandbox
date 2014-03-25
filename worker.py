from eval_py.Redis_Cola import Cola, Task, Worker
from eval_py.apply_test import exec_sandbox

import os


server = Cola("curso")
worker = Worker(os.environ['HOSTNAME'], server)

# Send a heartbeat after created
worker.send_heartbeat()

while True:
    t = worker.pull_task()

    if (t):
        code = t.params['code']
        test = t.params['test']
        worker.send_heartbeat() #About to start working
        t.result = exec_sandbox(code,test)
        t.put_result(worker)
    else:
        pass

    worker.send_heartbeat()



