__author__ = 'mariosky'
# -*- coding: utf-8 -*-
import shutil
import os
import tempfile
import subprocess
import json
import re

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
            result = (out,0)
        except subprocess.CalledProcessError , e:
            result = (json.dumps({ 'successes':[],'failures':[], 'errors': e.output.split('\n'), 'stdout': "", 'result': "Failure"}),e.returncode)
            return result

        #COMPILE Test
        try:
            out = subprocess.check_output(['javac','-cp','%s:/usr/share/java/junit.jar' % tmp_dir, os.path.join(tmp_dir, "%sTest.java" % java_class)], stderr=subprocess.STDOUT)
            result = (out,0)
        except subprocess.CalledProcessError , e:
            result = (json.dumps({ 'successes':[],'failures':[], 'errors': e.output.split('\n'), 'stdout': "", 'result': "Failure"}),e.returncode)
            return result


        #TEST
        try:
            out = subprocess.check_output(['java','-cp', '%s:/usr/share/java/junit.jar' % tmp_dir ,'org.junit.runner.JUnitCore', "%sTest" % java_class], stderr=subprocess.STDOUT)
            result = (process_out_as_json(out),0)
        except subprocess.CalledProcessError , e:
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





test =r"""//CalculatorTest
import static org.junit.Assert.assertEquals;
import org.junit.Test;

public class CalculatorTest {
  @Test
  public void evaluatesExpression() {
    System.out.println("Hello, World");
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


output="""JUnit version 4.11
.Hello, World
E
Time: 0.014
There was 1 failure:
1) evaluatesExpression(CalculatorTest)
java.lang.AssertionError: expected:<6> but was:<-6>
	at org.junit.Assert.fail(Assert.java:88)
	at org.junit.Assert.failNotEquals(Assert.java:743)
	at org.junit.Assert.assertEquals(Assert.java:118)
	at org.junit.Assert.assertEquals(Assert.java:555)
	at org.junit.Assert.assertEquals(Assert.java:542)
	at CalculatorTest.evaluatesExpression(CalculatorTest.java:11)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:57)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:606)
	at org.junit.runners.model.FrameworkMethod$1.runReflectiveCall(FrameworkMethod.java:47)
	at org.junit.internal.runners.model.ReflectiveCallable.run(ReflectiveCallable.java:12)
	at org.junit.runners.model.FrameworkMethod.invokeExplosively(FrameworkMethod.java:44)
	at org.junit.internal.runners.statements.InvokeMethod.evaluate(InvokeMethod.java:17)
	at org.junit.runners.ParentRunner.runLeaf(ParentRunner.java:271)
	at org.junit.runners.BlockJUnit4ClassRunner.runChild(BlockJUnit4ClassRunner.java:70)
	at org.junit.runners.BlockJUnit4ClassRunner.runChild(BlockJUnit4ClassRunner.java:50)
	at org.junit.runners.ParentRunner$3.run(ParentRunner.java:238)
	at org.junit.runners.ParentRunner$1.schedule(ParentRunner.java:63)
	at org.junit.runners.ParentRunner.runChildren(ParentRunner.java:236)
	at org.junit.runners.ParentRunner.access$000(ParentRunner.java:53)
	at org.junit.runners.ParentRunner$2.evaluate(ParentRunner.java:229)
	at org.junit.runners.ParentRunner.run(ParentRunner.java:309)
	at org.junit.runners.Suite.runChild(Suite.java:127)
	at org.junit.runners.Suite.runChild(Suite.java:26)
	at org.junit.runners.ParentRunner$3.run(ParentRunner.java:238)
	at org.junit.runners.ParentRunner$1.schedule(ParentRunner.java:63)
	at org.junit.runners.ParentRunner.runChildren(ParentRunner.java:236)
	at org.junit.runners.ParentRunner.access$000(ParentRunner.java:53)
	at org.junit.runners.ParentRunner$2.evaluate(ParentRunner.java:229)
	at org.junit.runners.ParentRunner.run(ParentRunner.java:309)
	at org.junit.runner.JUnitCore.run(JUnitCore.java:160)
	at org.junit.runner.JUnitCore.run(JUnitCore.java:138)
	at org.junit.runner.JUnitCore.run(JUnitCore.java:117)
	at org.junit.runner.JUnitCore.runMain(JUnitCore.java:96)
	at org.junit.runner.JUnitCore.runMainAndExit(JUnitCore.java:47)
	at org.junit.runner.JUnitCore.main(JUnitCore.java:40)

FAILURES!!!
Tests run: 1,  Failures: 1"""

