# Based on: http://readevalprint.github.com/blog/python-sandbox-with-pypy-part2.html


import shutil, os, tempfile
import subprocess



def exec_sandbox(code, test):
    try:
        code = code + test
        tmp_dir = tempfile.mkdtemp()
        tmp_script = open(os.path.join(tmp_dir, "script.py"),'w')
        tmp_script.write(code)
        tmp_script.close()
        script_path = os.path.join(tmp_dir, "script.py")
        result = [],""
        try:
            out = subprocess.check_output(['python',script_path], stderr=subprocess.STDOUT)
            result = (output_as_list(out),0)

        except subprocess.CalledProcessError , e:
            result = output_as_list(e.output), e.returncode

        finally:
            shutil.rmtree(tmp_dir)
        return result
    except Exception, e:
        return ['Error, could not evaluate'], e

def output_as_list(test_output):
    res = []
    if not test_output:
        return res

    for l in test_output.split('\n'):
        if len(l)>0  and l[:3] != '===' and l[:3] != '---' and 'Traceback' not in l and l[:2] != '  ':
            res.append(l)
    return res



code = '''
def foo():
    print 'hello world!'


def solution(nums):
    if nums > 0 :
        nums.sort()
        return [1,2]
        #return nums

    else:
        return [1]


def hang():
    while True:
        pass
'''

test = '''
import sys
import unittest

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
test_result = unittest.TextTestRunner(descriptions=False, verbosity=0, stream=sys.stderr).run(suite)
'''
if __name__ == '__main__':
    out = exec_sandbox(code,test)
    print out



