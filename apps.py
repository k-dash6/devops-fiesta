import sys
import os
import eel
import random


def req_path():
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, 'req.txt')


@eel.expose
def convert_value_py(ingredients):
    result = cocktails.get_receipts(ingredients)
    if not result:
        return "Не нашлось коктейля с выбранными ингредиентами :с"
    s = ""
    for i in result:
        s += i[0].create_str(i[1])
    return s


@eel.expose
def decorator_for_random_cocktail():
    return cocktails.get_random_receipt().create_str([])


def create_cocktails():
    global cocktails
    cocktails = Cocktails()


class Cocktails:

    def __init__(self):
        self.cocktails = []
        self.read()

    class Cocktail:
        def __init__(self, name, components, receipt, ingredients):
            self.name = name
            self.components = components
            self.receipt = receipt
            self.ingredients = ingredients

        def create_str(self, insufficient):
            s = '<span style="font-size: 22px">' + self.name + '</span>' + '<br>'
            s += '<div style="margin-left: 50px;">'
            for i in self.components:
                if i.split()[0].lower() in insufficient:
                    s += '<span style=" color:#b3d4fd;">' + i + '</span>' + '<br>'
                else:
                    s += '<span style=" ">' + i + '</span>' + '<br>'
            s += '</div>'
            s += '<span style="font-size: 20px">Рецепт</span><br>' + \
                 '<span style="">' + self.receipt + '</span>' + '<br><br>'
            return s

    def read(self):
        file_path = req_path()
        with open(file_path, 'r', encoding='utf-8') as file:
            while True:
                line = file.readline()
                if not line:
                    break
                name = line.strip('\n')
                components = []
                ingredients = set()
                for i in range(int(file.readline())):
                    components.append(file.readline().strip('\n'))
                    ingredients.add(components[i].split()[0].lower())
                receipt = file.readline().strip('\n')
                self.cocktails.append(self.Cocktail(name, components, receipt, ingredients))

    def get_receipts(self, ingredients):
        if type(ingredients) != list:
            return None
        for i in ingredients:
            if type(i) != str:
                return None
        receipts = []
        for cocktail in self.cocktails:
            insufficient = cocktail.ingredients - set(ingredients)
            if len(cocktail.ingredients) - len(insufficient) > 1:
                receipts.append([cocktail, insufficient])
        receipts.sort(key=lambda x: len(x[1]))
        return receipts

    def get_random_receipt(self):
        return self.cocktails[random.randint(0, len(self.cocktails)) - 1]
