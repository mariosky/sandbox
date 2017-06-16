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
            out = subprocess.check_output(['prove', '--QUIET', '--exec', 'perl6', '--formatter', 'TAP::Formatter::JUnit', script_path], stderr=subprocess.STDOUT)
            result = (_success_result(out), 0)
        except subprocess.CalledProcessError, e:
            result = (_error_result(e.output), 0)

        finally:
            shutil.rmtree(tmp_dir)


        return result
    except Exception, e:
        return json.dumps({
            'successes': [],
            'failures': [],
            'errors': [],
            'stdout': e.message,
            'result': 'ProcessError'
        })


def _error_result(out):
    xml_JUNit = []
    compile_error = False
    errors = []
    for l in out.split('\n'):
        if len(l) > 0:
            if l.startswith('#'):
                continue
            if l.startswith('perl:'):
                continue
            if 'SORRY!' in l:
                compile_error = True
                errors.append("Error while compiling")
                continue
            if compile_error:
                errors.append(l)
                continue

            xml_JUNit.append(l)
        #Return Compile Error
        if len(l) == 0 and compile_error:
            r = {
                'successes': [],
                'failures': [],
                'errors': errors,
                'stdout': '\n'.join(errors),
                'result': []}
            return json.dumps(r)

    doc = '\n'.join(xml_JUNit)
    try:
        tree = ET.fromstring(doc)
    except ET.ParseError, e:

    # Process error
        return json.dumps({
                'successes': [],
                'failures': [],
                'errors': [],
                'stdout': out,
                'result': 'ProcessError'
            })

    #Return Unit test Error
    system_out = [e.text for e in tree.findall(".//system-out")]
    successes = []
    failures = []
    stdout = []

    if system_out:
        for l in system_out[0].split('\n'):
            if len(l) > 0:
                if l.startswith('not ok'):
                    failures.append(l)
                    continue
                if l.startswith('ok'):
                    successes.append(l)
                    continue
                stdout.append(l)


    return json.dumps({
        'successes': [],
        'failures': [e.attrib['message'] for e in  tree.findall(".//failure")],
        'errors': [],
        'stdout': '\n'.join(stdout) ,
        'result': 'Failure'
    })








def _success_result(out):
    xml_JUNit = []
    ## Clean ouput
    for l in out.split('\n'):
        if len(l) > 0:
            if l.startswith('#'):
                continue
            if l.startswith('perl:'):
                continue

            xml_JUNit.append(l)


    doc = '\n'.join(xml_JUNit)
    tree = ET.fromstring(doc)

    system_out = [e.text for e in tree.findall(".//system-out")]
    successes =[]
    failures =[]
    stdout = []

    if system_out:
        for l in system_out[0].split('\n'):
            if len(l) > 0:
                if l.startswith('not ok'):
                    failures.append(l)
                    continue
                if l.startswith('ok'):
                    successes.append(l)
                    continue
                stdout.append(l)



    r = {
        'successes': successes,
        'failures': [],
        'errors': [],
        'stdout': '\n'.join(stdout)   ,
        'result': 'Success'
    }

    return json.dumps(r)

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
    is add(6,-1),         2, 'Suma dos enteros error';
    """

    print run_test(code, test)