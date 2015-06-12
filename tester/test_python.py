# -*- coding: utf-8 -*-
# Based on: http://readevalprint.github.com/blog/python-sandbox-with-pypy-part2.html


import shutil, os, tempfile
import subprocess,json



def run_test(code, test):
    try:
        code = """# -*- coding: utf-8 -*-
        """ + code + test
        code = unicode(code)
        tmp_dir = tempfile.mkdtemp()
        tmp_script = open(os.path.join(tmp_dir, "script.py"),'w')
        tmp_script.write(code.encode('utf8'))
        tmp_script.close()
        script_path = os.path.join(tmp_dir, "script.py")
        result = [],""
        try:
            out = subprocess.check_output(['python',script_path], stderr=subprocess.STDOUT)
            result = (process_out_as_json(out),0)

        except subprocess.CalledProcessError , e:
            print "Error"
            result = process_error_as_json(e.output), e.returncode

        finally:
            shutil.rmtree(tmp_dir)
        return result
    except Exception, e:
        return ['Error, could not evaluate'], e

def process_out_as_json(output):
    # La salida de STDOUT estara primero
    # Extraerla y agregarla al json out

    if output:
        out_list = output.split("!!!---\n")
        stdout = out_list[0]
        output_temp = json.loads(out_list[1])
        output_temp["stdout"] = stdout
        return json.dumps(output_temp)

def process_error_as_json(output):
    res = []
    if output:
        for l in output.split('\n'):
            if len(l)>0  and l[:3] != '===' and l[:3] != '---' and 'Traceback' not in l and l[:2] != '  ':
                res.append(l)

    result = {}
    result['result'] = "ProcessError"
    result['errors']=  res
    result['failures']=  []
    result['successes']=  []
    return json.dumps(result)

#def process_output_as_json(output):



if __name__ == '__main__':
    code = u'''
def foo():
    print 'hello world!'


def solution(nums):
    print "José"
    if nums > 0 :
        nums.sort()

        return nums

    else:
        return []


def hang():
    while True:
        pass
'''

    test = u'''
import sys
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
Resultado = ResultadoPrueba()
suite.run(Resultado)
result = {}

if Resultado.wasSuccessful():
    result['result'] = "Success"
else:
    result['result'] = "Failure"
result['errors']=  [str(e[0])   for e in Resultado.errors]
result['failures']=  [str(e[0]) for e in Resultado.failures]
result['successes']=  [str(e)  for e in Resultado.success]
print "!!!---"
print json.dumps(result)
'''

    out = run_test(code,test)
    print out

def solution(nums):
    if nums > 0 :
        nums.sort()
        #return [1,2]
        for r in range(10):
            print "Hola"
        return nums
    else:
        return [1]


import sys
import unittest

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
    def test_order(self):
        self.assertEqual(solution([2,6,1,5]),[1,2,5,6])
    def test_none(self):
        self.assertEqual(solution(None),[])


