import os
import importlib

from redis_cola import Cola, Worker

lang = os.environ['LANG']
server = Cola(lang)
worker = Worker(os.environ['HOSTNAME'], server)


# Send a heartbeat after created
worker.send_heartbeat()


tester_module =  'tester.test_%s' % lang
tester = importlib.import_module(tester_module)

while True:
    t = worker.pull_task()

    if (t):
        code = t.params['code']
        test = t.params['test']
        worker.send_heartbeat() #About to start working
        t.result = tester.run_test(code,test)
        t.put_result(worker)
    else:
        pass

    worker.send_heartbeat()



