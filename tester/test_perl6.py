# -*- coding: utf-8 -*-
# Based on: http://readevalprint.github.com/blog/python-sandbox-with-pypy-part2.html


import shutil, os, tempfile
import subprocess,json, re


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
            result = (_result(out), 0)
        except subprocess.CalledProcessError, e:
            result = (_result(e.output), 0)

        finally:
            #shutil.rmtree(tmp_dir)
            pass

        return result
    except Exception, e:
        return ["Error, could not evaluate"], e

def _result(out):
    xml_JUNit = []
    ## Clean ouput

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

        if len(l) == 0 and compile_error:
            r = {
                'successes': [],
                'failures': [],
                'errors': errors,
                'stdout': '\n'.join(errors),
                'result': []
            }

            return json.dumps(r)





    import xml.etree.ElementTree as ET
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
        'failures': failures,
        'errors': [],
        'stdout': '\n'.join(stdout)   ,
        'result': [(e.attrib['failures'])  for e in  tree.findall("testsuite")]
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
    is add(6,-1),         5, 'Suma dos enteros';
    """

    print run_test(code, test)