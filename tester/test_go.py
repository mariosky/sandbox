# -*- coding: utf-8 -*-
import shutil
import os
import tempfile
import subprocess
import json
import re

def run_test(code, test):
    try:
        code = unicode(code)
        test = unicode(test)



        tmp_dir = tempfile.mkdtemp(prefix="/Users/mariosky/go/src/")
        print tmp_dir
        program_name = tmp_dir.split('/')[-1]

        tmp_program = open(os.path.join(tmp_dir, "%s.go" % program_name ),'w')
        tmp_program.write(code.encode('utf8'))
        tmp_program.close()
        result = [],0


        tmp_test = open(os.path.join(tmp_dir, "%s_test.go" % program_name ),'w')
        tmp_test.write(test.encode('utf8'))
        tmp_test.close()



        #COMPILE Program
        try:
            out = subprocess.check_output(['go','install',program_name], stderr=subprocess.STDOUT)
            print out
            result = (out,0)
        except subprocess.CalledProcessError , e:
            result = (json.dumps({ 'successes':[],'failures':[], 'errors': e.output.split('\n'), 'stdout': "", 'result': "Failure"}),e.returncode)
            return result

        #TEST
        try:
            out = subprocess.check_output(['go','test', program_name], stderr=subprocess.STDOUT)
            print result
            result = (process_out_as_json(out),0)
        except subprocess.CalledProcessError , e:
            print e.output
            result = process_error_as_json(e.output), e.returncode
        finally:
            shutil.rmtree(tmp_dir)
        return result
    except Exception, e:
         return ["Error, could not evaluate"], e


def process_out_as_json(output):
    # La salida de STDOUT estara primero
    # Extraerla y agregarla al json out
    stdout = []
    res = []
    if output:
        for l in output.split('\n'):
            if len(l) >0:
                if  l.startswith('JUnit'):
                    res.append(l)
                    continue
                if l.startswith('.'):
                    no_dots = re.sub(r'^\.*', '', l)
                    stdout.append(no_dots)
                    continue
                if l.startswith('Time') or l.startswith('OK'):
                    stdout.append(l)
                    continue
                stdout.append(l)
    result = {}
    result['result'] = "Success"
    result['errors']=  res
    result['failures']=  []
    result['successes']=  []
    result['stdout']=  stdout
    return json.dumps(result)


def process_error_as_json(output):
    res = []
    if output:
        for l in output.split('\n'):
            if len(l) >0 and not l.startswith('\t'):
                if  l.startswith('JUnit'):
                    res.append(l)
                    continue

                if l.startswith('.'):
                    no_dots = re.sub(r'^\.*', '', l)
                    res.append(no_dots)
                    continue
                res.append(l)
    result = {}
    result['result'] = "ProcessError"
    result['errors']=  res
    result['failures']=  []
    result['successes']=  []
    return json.dumps(result)



if __name__ == "__main__":
    code= r"""
    package math

    func Average(xs []float64) float64 {
      total := float64(0)
      for _, x := range xs {
        total += x
      }
      return total / float64(len(xs))
    }
    """

    test = r"""
    package math

    import "testing"

    func TestAverage(t *testing.T) {
      var v float64
      v = Average([]float64{1,2})
      if v != 1.3 {
        t.Error("Expected 1.5, got ", v)
      }
    }
"""

    print run_test(code, test)

