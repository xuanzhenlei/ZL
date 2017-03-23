#!/usr/bin/python
#-*- coding:utf-8 -*-

class Animal(object):
    def run(self):
        return 'Animal is running...'
class Dog(Animal):
    def run(self):
        return 'Dog is running...'
class Cat(Animal):
    def run(self):
        return 'Cat is running...'
dog=Dog()
cat=Cat()
print dog.run()
print cat.run()

dir('dog')