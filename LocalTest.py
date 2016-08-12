# -*- coding: utf-8 -*-
__author__ = 'mariosky'

import os
import json


print os.environ['REDIS_HOST']
print os.environ['LANG']

from tester.Redis_Cola import Cola, Task

server = Cola("csharp")

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
    t.get_result('csharp')
    if t.result:
        return t.result
        return json.loads( t.result[0])
    else:
        return "Snif"
tid = put()
print tid

for i in range(500):
    print get(tid)
