# -*- coding: utf-8 -*-
# Based on: http://readevalprint.github.com/blog/python-sandbox-with-pypy-part2.html


import shutil, os, tempfile
import subprocess,json



def run_test(code, test):
    try:
        code = """# -*- coding: utf-8 -*-
        """ + code + test_begin + test +test_end
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


test_begin = u"""
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
"""

test_end = u"""
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
"""

