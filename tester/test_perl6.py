# -*- coding: utf-8 -*-
# Based on: http://readevalprint.github.com/blog/python-sandbox-with-pypy-part2.html


import shutil, os, tempfile
import subprocess,json, re
import xml.etree.ElementTree as ET

def run_test(code, test):
    try:

        code = code + test_begin + test +test_end
        code = unicode(code)
        tmp_dir = tempfile.mkdtemp()
        tmp_script = open(os.path.join(tmp_dir, "test.t"),'w')
        tmp_script.write(code.encode('utf8'))
        tmp_script.close()
        script_path = os.path.join(tmp_dir, "test.t")
        result = [],""
        out = None
        try:
            out = subprocess.check_output(['prove','-v', '--exec', 'perl6', script_path], stderr=subprocess.STDOUT)
            result = (_success_result(out), 0)
        except subprocess.CalledProcessError, e:
            result = (_error_result(e.output), e.returncode)

        finally:
            shutil.rmtree(tmp_dir)

        return result
    except Exception, e:
        return (json.dumps({
            'successes': [],
            'failures': [],
            'errors': [],
            'stdout': e.message,
            'result': 'ProcessError'
        }),1)


def _error_result(out):
    # La salida de STDOUT estara primero
    # Extraerla y agregarla al json out
    successes = []
    failures = []
    stdout = []
    N = 0  # Number of tests

    for l in out.split('\n'):
        if len(l) > 0:
            if l.startswith('#') or l.startswith('Dubious, test') :
                continue
            if l.startswith('ok'):
                successes.append(l[3:])
                continue
            if l.startswith('not ok'):
                failures.append(l[7:])
                continue
            if l.startswith('1..'):
                break
            stdout.append(l)


    return json.dumps({
        'successes': successes,
        'failures': failures,
        'errors': [],
        'stdout': stdout,
        'result': 'Failure'
    })









def _success_result(out):
    successes = []
    failures = []
    stdout = []
    N = 0 #Number of tests

    for l in out.split('\n'):
        if len(l) > 0:
            if l.startswith('#'):
                continue
            if l.startswith('ok'):
                successes.append(l[3:])
                continue
            if l.startswith('not ok'):
                failures.append(l[7:])
                continue
            if l.startswith('1..'):
                N = int(l[3:])
                break
            stdout.append(l)


    return json.dumps({
        'successes': successes,
        'failures': failures,
        'errors': [],
        'stdout': stdout,
        'result':'Success'
    })




test_begin = u"""
use v6.c;
use Test;      # a Standard module included with Rakudo
"""

test_end = u"""
done-testing;
"""


if __name__ == "__main__":
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

    print run_test(code, test)