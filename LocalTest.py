# -*- coding: utf-8 -*-
__author__ = 'mariosky'

import os

print os.environ['REDIS_HOST']
print os.environ['APP_NAME']
print os.environ['LANG']

from tester.Redis_Cola import Cola, Task, Worker

server = Cola("C#")

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





task = {"id": None, "method": "exec", "params": {"code": code, "test": test}}
task_id = server.enqueue(**task)

print task_id

