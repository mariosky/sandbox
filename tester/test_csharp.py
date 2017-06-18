# -*- coding: utf-8 -*-
import shutil
import os
import tempfile
import subprocess
import json


def run_test(code, test):
    try:
        code = """using NUnit.Framework;
        """ + code + test
        code = unicode(code)
        tmp_dir = tempfile.mkdtemp()
        tmp_script = open(os.path.join(tmp_dir, "ProgramTest.cs"),'w')
        tmp_script.write(code.encode('utf8'))
        tmp_script.close()
        result = [],0

        #COMPILE
        try:
            out = subprocess.check_output(['mcs',os.path.join(tmp_dir, "ProgramTest.cs"),  '-r:/home/nunit.framework.dll',  '-target:library'], stderr=subprocess.STDOUT)
            print out
            result = (out,0)
        except subprocess.CalledProcessError , e:
            print e
            result = (json.dumps({ 'successes':[],'failures':[], 'errors': e.output.split('\n'), 'stdout': "", 'result': "Failure"}),e.returncode)
            return result

        #TEST
        try:
            out = subprocess.check_output(['nunit-console','-nologo', '-nodots','-output=out.txt',os.path.join(tmp_dir, "ProgramTest.dll")], stderr=subprocess.STDOUT)
            print out
            result = (_result(),0)
        except subprocess.CalledProcessError , e:
            result = ["Error, could not evaluate"], e
        finally:
            shutil.rmtree(tmp_dir)

        return result
    except Exception, e:
        return ["Error, could not evaluate"], e


def _result():
    import xml.etree.ElementTree as ET
    tree = ET.parse('TestResult.xml')
    a = open('out.txt')
    r = {
        'successes': [e.attrib['description']   for e in  tree.findall(".//test-case[@result='Success']")],
        'failures': [e.attrib['description'] for e in  tree.findall(".//test-case[@result='Failure']")],
        'errors': [],
        'stdout': a.read(),
        'result': tree.findall("test-suite")[0].attrib['result']
    }

    return json.dumps(r)

if __name__ == "__main__":

    code = u"""using System.IO;
    using System;
    public class Product
    {
            public int  code;
            public string  desc;
    
            public Product(int c, string d)
            {
            code=c;
            desc=d;
            }
    
            public void Print()
            {
            Console.WriteLine("Producto {0}: {1}", code,desc);
            }
    
    }"""



    test= u"""[TestFixture]
    public class ProductTest
    {
    
        [Test, Description("Prueba del Constructor")]
        public void Constructor()
        {
            Product p = new Product(1,"hola");
            // Constraint Syntax
            Assert.AreEqual(p.code,1);
        }
    
    
        [Test, Description("Imprimir la Descripción")]
        public void PrintTest()
        {
            Product p = new Product(1,"hola");
            p.Print();
    
            using (StringWriter sw = new StringWriter())
            {
                Console.SetOut(sw);
    
    
                p.Print();
    
            string expected = "Producto 1: hola";
            StringAssert.StartsWith(expected, sw.ToString());
    
    
            }
    
        }
    }"""

    print run_test(code,test)