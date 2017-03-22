#!/usr/bin/python
#-*- coding:utf-8 -*-

import random


class PetShop:

  """宠物商店"""

  def __init__(self, animal_factory=None):

    """宠物工厂是我们的抽象工厂。我们可以随意设置。"""
    self.pet_factory = animal_factory

  def show_pet(self):

    """使用抽象工厂创建并显示一个宠物"""

    pet = self.pet_factory.get_pet()
    print("我们有一个可爱的 {}".format(pet))
    print("它说 {}".format(pet.speak()))
    print("我们还有 {}".format(self.pet_factory.get_food()))


# 工厂生产的事物

class Dog:

  def speak(self):
    return "汪"

  def __str__(self):
    return "Dog"


class Cat:

  def speak(self):
    return "喵"

  def __str__(self):
    return "Cat"


# Factory classes

class DogFactory:

  def get_pet(self):
    return Dog()

  def get_food(self):
    return "狗食"


class CatFactory:

  def get_pet(self):
    return Cat()

  def get_food(self):
    return "猫粮"


# 随机创建合适的工厂
def get_factory():
  """让我们动起来！"""
  return random.choice([DogFactory, CatFactory])()


# 多个工厂显示宠物
if __name__ == "__main__":
  for i in range(4):
    shop = PetShop(get_factory())
    shop.show_pet()
    print("=" * 20)