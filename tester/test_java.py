__author__ = 'mariosky'
# -*- coding: utf-8 -*-
import shutil
import os
import tempfile
import subprocess
import json


def run_test(code, test, type=None):
    try:
        java_class = test[2:test.index('\n')-len('Test')]
        code = unicode(code)
        test = unicode(test)


        tmp_dir = tempfile.mkdtemp()
        print tmp_dir
        tmp_program = open(os.path.join(tmp_dir, "%s.java" % java_class ),'w')
        tmp_program.write(code.encode('utf8'))
        tmp_program.close()
        result = [],0


        tmp_test = open(os.path.join(tmp_dir, "%sTest.java" % java_class ),'w')
        tmp_test.write(test.encode('utf8'))
        tmp_test.close()



        #COMPILE Program
        try:
            out = subprocess.check_output(['javac',os.path.join(tmp_dir,"%s.java" % java_class)], stderr=subprocess.STDOUT)
            print 'Compile',result
            result = (out,0)
        except subprocess.CalledProcessError , e:
            result = (json.dumps({ 'successes':[],'failures':[], 'errors': e.output.split('\n'), 'stdout': "", 'result': "Failure"}),e.returncode)
            return result

        #COMPILE Test
        try:
            out = subprocess.check_output(['javac','-cp','%s:/usr/share/java/junit4.jar' % tmp_dir, os.path.join(tmp_dir, "%sTest.java" % java_class)], stderr=subprocess.STDOUT)
            result = (out,0)
            print 'Compile Test',result
        except subprocess.CalledProcessError , e:
            result = (json.dumps({ 'successes':[],'failures':[], 'errors': e.output.split('\n'), 'stdout': "", 'result': "Failure"}),e.returncode)
            print e
            return result


        #TEST
        try:
            out = subprocess.check_output(['java','-cp', '%s:/usr/share/java/junit4.jar' % tmp_dir ,'org.junit.runner.JUnitCore',os.path.join(tmp_dir, "%sTest" % java_class)], stderr=subprocess.STDOUT)
            result = (out,0)
            print 'Test Out',out
        except subprocess.CalledProcessError , e:
            result =  (result, e.returncode)
            print e
        finally:
            shutil.rmtree(tmp_dir)

        return result
    except Exception, e:
        return ["Error, could not evaluate"], e





test =r"""//CalculatorTest
import static org.junit.Assert.assertEquals;
import org.junit.Test;

public class CalculatorTest {
  @Test
  public void evaluatesExpression() {
    Calculator calculator = new Calculator();
    int sum = calculator.evaluate("1+2+3");
    assertEquals(6, sum);
  }
}"""


code =r"""
public class Calculator {
  public int evaluate(String expression) {
    int sum = 0;
    for (String summand: expression.split("\\+"))
      sum += Integer.valueOf(summand);
    return sum;
  }
}"""

print run_test(code,test)