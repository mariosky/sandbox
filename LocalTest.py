# -*- coding: utf-8 -*-
__author__ = 'mariosky'

import os
import json


print os.environ['REDIS_HOST']
print os.environ['LANG']

from tester.Redis_Cola import Cola, Task

server = Cola("python")

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
        Assert.AreEqual(p.code,-1);

    }

    [Test, Description("Public Descripción")]
    public void Descripcion()
    {
        Product p = new Product(1,"hola");
        // Constraint Syntax
        Assert.AreEqual(p.desc,"hola");

    }
}"""



def put():
    task = {"id": None, "method": "exec", "params": {"code": code, "test": test}}
    print task
    task_id = server.enqueue(**task)
    return task_id


def get(t_id):
    t = Task(id=t_id)
    t.get_result('python')
    if t.result:
        return t.result
        return json.loads( t.result[0])
    else:
        return "Snif"
tid = put()
print tid
for i in range(50):
    print get(tid)


#('{"successes": ["test_negativos (__main__.Test)", "test_suma_positivos (__main__.Test)"], "failures": [], "errors": [], "result": "Success", "stdout": ""}', 0)

# import xml.etree.ElementTree as ET
# tree = ET.parse('tester/TestResult.xml')
# a = open('out.txt')
# r = {
#     'successes':[ e.attrib['name'] for e in  tree.findall(".//test-case[@result='Success']")],
#     'failures':[ e.attrib['name'] for e in  tree.findall(".//test-case[@result='Failure']")],
#     'errors': [],
#     'stdout': a.read(),
#     'result': tree.findall("test-suite")[0].attrib['result']
#     }
#
# print json.dumps(r)