
from eval_py.Redis_Cola import Cola, Task, Worker

from eval_py.apply_test import exec_sandbox

import uuid
import time




server = Cola("curso")


## Each Worker
worker = Worker(uuid.uuid4(), server)

while True:
    t = worker.pull_task()
    if (t):
        print t
        #t.result = suma(**t.params)
        print time.sleep(10)
        #t.put_result(worker)

    else:
        pass

    worker.send_heartbeat()
