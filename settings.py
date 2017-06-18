

settings = {
   "csharp":
       {"command" :"python /home/sandbox/worker.py", "image": 'mariosky/sandbox-test-csharp:latest',"containers":1},
   "python":
       {"command": "python /home/sandbox/worker.py", "image": 'mariosky/sandbox-test-python:latest',"containers": 1},
   "java"  :
       {"command" :"python /home/sandbox/worker.py", "image": 'mariosky/sandbox-test-java:latest'  ,"containers":1},
   "perl6" :
       {"command": "python /home/sandbox/worker.py", "image": 'mariosky/sandbox-test-perl6:latest' ,"containers": 1},
}



