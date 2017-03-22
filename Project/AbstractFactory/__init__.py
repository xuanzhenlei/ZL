#!/usr/bin/python  
  
  
class Pizza:  
    name = ""  
    dough = None  
    sauce = None  
    cheese = None  
    clam = None  
  
    def prepare(self):  
        pass  
  
    def bake(self):  
        print "Bake for 25 minutes at 350."  
  
    def cut(self):  
        print "Cutting into diagonal slices."  
  
    def box(self):  
        print "Put into official box."  
  
    def get_name(self):  
        return self.name  
  
    def set_name(self, name):  
        self.name = name  
  
    def to_string(self):  
        string = "%s:\n" % self.name   
        string += "    Dough: %s\n" % self.dough.to_string() if self.dough else ""  
        string += "    Sauce: %s\n" % self.sauce.to_string() if self.sauce else ""  
        string += "    Cheese: %s\n" % self.cheese.to_string() if self.cheese else ""  
        string += "    Clam: %s\n" % self.clam.to_string() if self.clam else ""  
        return string  
  
  
class CheesePizza(Pizza):  
    def __init__(self, ingredient_factory):  
        self.ingredient_factory = ingredient_factory  
  
    def prepare(self):  
        print "Preparing: %s" % self.name  
        self.dough = self.ingredient_factory.create_dough()  
        self.sauce = self.ingredient_factory.create_sauce()  
        self.cheese = self.ingredient_factory.create_cheese()  
  
  
class ClamPizza(Pizza):  
    def __init__(self, ingredient_factory):  
        self.ingredient_factory = ingredient_factory  
  
    def prepare(self):  
        print "Preparing: %s" % self.name  
        self.dough = self.ingredient_factory.create_dough()  
        self.sauce = self.ingredient_factory.create_sauce()  
        self.clam = self.ingredient_factory.create_clam()  
  
  
  
class PizzaStore:  
    def order_pizza(self, pizza_type):  
        self.pizza = self.create_pizza(pizza_type)  
        self.pizza.prepare()  
        self.pizza.bake()  
        self.pizza.cut()  
        self.pizza.box()  
        return self.pizza  
  
    def create_pizza(self, pizza_type):  
        pass  
  
  
class NYPizzaStore(PizzaStore):  
    def create_pizza(self, pizza_type):  
        ingredient_factory = NYPizzaIngredientFactory()  
  
        if pizza_type == "cheese":  
            pizza = CheesePizza(ingredient_factory)  
            pizza.set_name("New York Style Cheese Pizza")  
        elif pizza_type == "clam":  
            pizza = ClamPizza(ingredient_factory)  
            pizza.set_name("New York Style Clam Pizza")  
        else:  
            pizza = None  
  
        return pizza  
  
  
class ChicagoPizzaStore(PizzaStore):  
     def create_pizza(self, pizza_type):  
        ingredient_factory = ChicagoPizzaIngredientFactory()  
  
        if pizza_type == "cheese":  
            pizza = CheesePizza(ingredient_factory)  
            pizza.set_name("Chicago Style Cheese Pizza")  
        elif pizza_type == "clam":  
            pizza = ClamPizza(ingredient_factory)  
            pizza.set_name("Chicago Style Clam Pizza")  
        else:  
            pizza = None  
  
        return pizza  
  
  
class PizzaIngredientFactory:  
    def create_dough(self):  
        pass  
  
    def create_sauce(self):  
        pass  
  
    def create_cheese(self):  
        pass  
  
    def create_clam(self):  
        pass  
  
  
class NYPizzaIngredientFactory(PizzaIngredientFactory):  
    def create_dough(self):  
        return ThinDough()  
  
    def create_sauce(self):  
        return MarinaraSauce()  
  
    def create_cheese(self):  
        return FreshCheese()  
  
    def create_clam(self):  
        return FreshClam()  
  
  
class ChicagoPizzaIngredientFactory(PizzaIngredientFactory):  
    def create_dough(self):  
        return ThickDough()  
  
    def create_sauce(self):  
        return MushroomSauce()  
  
    def create_cheese(self):  
        return BlueCheese()  
  
    def create_clam(self):  
        return FrozenClam()  
  
  
class Dough:  
    def to_string(self):  
        pass  
  
class ThinDough(Dough):  
    def to_string(self):  
        return "Thin Dough"  
  
class ThickDough(Dough):  
    def to_string(self):  
        return "Thick Dough"  
  
class Sauce:  
    def to_string(self):  
        pass  
  
class MarinaraSauce(Sauce):  
    def to_string(self):  
        return "Marinara Sauce"  
  
class MushroomSauce(Sauce):  
    def to_string(self):  
        return "Mushroom Sauce"  
  
class Cheese:  
    def to_string(self):  
        pass  
  
class FreshCheese(Cheese):  
    def to_string(self):  
        return "Fresh Cheese"  
  
class BlueCheese(Cheese):  
    def to_string(self):  
        return "Blue Cheese"  
  
class Clam:  
    def to_string(self):  
        pass  
  
class FreshClam(Clam):  
    def to_string(self):  
        return "Fresh Clam"  
  
class FrozenClam(Clam):  
    def to_string(self):  
        return "Frozen Clam"  
  
  
  
if __name__ == "__main__":  
    ny_store = NYPizzaStore()  
    chicago_store = ChicagoPizzaStore()  
  
    pizza = ny_store.order_pizza("cheese")  
    print pizza.to_string()  
    print "Mike ordered a %s" % pizza.get_name()  
    print   
  
    pizza = chicago_store.order_pizza("clam")  
    print pizza.to_string()  
    print "John ordered a %s" % pizza.get_name()  
    print  