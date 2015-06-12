from tester.Redis_Cola import Cola, Task, Worker


import os


server = Cola("curso")
worker = Worker(os.environ['HOST'], server)



# Send a heartbeat after created
worker.send_heartbeat()
lang = os.environ['LANG']

if lang == 'Python':
    from tester.test_python import run_test
elif lang == 'C#':
    from tester.test_csharp import run_test

while True:
    t = worker.pull_task()

    if (t):
        code = t.params['code']
        test = t.params['test']
        worker.send_heartbeat() #About to start working
        t.result = run_test(code,test)
        t.put_result(worker)
    else:
        pass

    worker.send_heartbeat()



