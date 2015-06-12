__author__ = 'mariosky'
# -*- coding: utf-8 -*-
import shutil
import os
import tempfile
import subprocess
import json


def run_test(code, test, type=None):
    try:
        code = """using NUnit.Framework;
        """ + code + test
        code = unicode(code)
        tmp_dir = tempfile.mkdtemp()
        tmp_script = open(os.path.join(tmp_dir, "ProgramTest.cs"),'w')
        tmp_script.write(code.encode('utf8'))
        tmp_script.close()
        result = [],""
        try:
            compile(tmp_dir)
            result = run_test(tmp_dir)
        except subprocess.CalledProcessError , e:
            result =  (e.output, e.returncode)
        finally:
            shutil.rmtree(tmp_dir)
        return result
    except Exception, e:
        return ["Error, could not evaluate"], e

def compile(tmp_dir ):
    result = None
    try:
        out = subprocess.check_output(['mcs',os.path.join(tmp_dir, "ProgramTest.cs"),  '/pkg:nunit',  '-target:library'], stderr=subprocess.STDOUT)
        result = (out,0)
    except subprocess.CalledProcessError , e:
        result =  (e.output, e.returncode)
    finally:
        return result

def run_test(tmp_dir):
    result = None
    try:
        out = subprocess.check_output(['nunit-console','-nologo', '-nodots',os.path.join(tmp_dir, "ProgramTest.dll")], stderr=subprocess.STDOUT)
        result = (out,0)
    except subprocess.CalledProcessError , e:
        result =  (e.output, e.returncode)
    finally:
        return result


code = """
using System;
public class Product
{
        public int code;
        public string desc;

        public Product(int c, string d)
        {
        code=c;
        desc=d;
        }

}"""



test= u"""[TestFixture]
public class ProductTest
{

    [Test, Description("Prueba del Constructor")]
    public void Constructor()
    {
        Product p = new Product(1,"hola");
        Console.WriteLine(p.desc);
        Console.WriteLine("YES!");


        // Constraint Syntax
        Assert.AreEqual(p.code,1);

    }

    [Test, Description("Public Descripción")]
    public void Descripcion()
    {
        Product p = new Product(1,"hola");
        // Constraint Syntax
        Assert.AreEqual(p.desc,"hola");

    }
}"""


r = run_test(code, test)
for l in r[0].split('\n'):
    print l