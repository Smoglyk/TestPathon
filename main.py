# This is a sample Python script.
import dis
import inspect
from types import FunctionType


from Myjson import  JsonFormat
import json
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class Student:

    def __init__(self):
        self.fruit = "Apple"


class Test:
    argument = "NaSvyzi"

    def __init__(self):
        self.fraction = -0.00000001201212
        self.age = 18
        self.answer = True
        self.name = "Jack"
        self.sex = "man"
        self.list = ["ada", 213, True]
        self.dict = {"City": Student(), "Street": "A.Bachilo"}

def print_hi(name, solo = 15):

    x = 15
    g = 13

    list = (x, g)

    for i in list:
        print(i)
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    print(dict(inspect.getmembers(print_hi.__code__)))
    pidaras = JsonFormat()

    pidaras.make_dict_function(print_hi)

    '''''
    s = Test.__dict__
    for i in s:
        print(s[i])
        print(type(s[i]))

    m = JsonFormat()
    str = m.dumps(Test())
    print(str)

    with open("my_file.json", "w") as file:
        m.dump(Test(), file)

    dict_loads = m.loads(str)
    print("Loads")
    print(dict_loads)

    with open("my_file.json", "r") as file:
        dict_load = dict2 = m.load(file)
        print("Load")
        print(dict_load)
    '''

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
