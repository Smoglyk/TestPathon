from GeneralInterface import AbstractFormat
import inspect
import json
import re



class JsonFormat(AbstractFormat):

    def __init__(self):
        pass


    def dumps(self, obj):
        json_str = "{"

        if not(inspect.isfunction(obj)):
            fields = obj

            if not(isinstance(obj, (tuple, dict))):
                fields = obj.__dict__

            for key in fields.keys():
                data_str = f", \"{str(key)}\"" + ": "

                if isinstance(fields[key], bool):

                    if fields[key] == True:
                        data_str = data_str + "true"
                    else:
                        data_str = data_str + "false"

                elif isinstance(fields[key], (int, float)):
                    data_str = data_str + f"{fields[key]}"

                elif isinstance(fields[key], str): #Делаем отделюну проверку на тип у строки, т.к. строке в json необходимы ""
                    data_str = data_str + f"\"{fields[key]}\""

                elif isinstance(fields[key], (tuple, dict)):
                    data_str = data_str + f"{self.dumps(fields[key])}"

                elif isinstance(fields[key], (list, set)):
                    current_str = "["

                    for element in fields[key]:
                        current_str = current_str + ", "

                        if isinstance(element, bool):

                            if element == True:
                                current_str = current_str + "true"
                            else:
                                current_str = current_str + "false"

                        elif isinstance(element, (int, float)):
                            current_str = current_str + str(element)

                        elif isinstance(element, str):
                            current_str = current_str + f"\"{element}\""

                        else:
                            current_str = current_str + f"{self.dumps(element)}"


                    current_str = current_str[:1] + current_str[3:] + "]"
                    data_str = data_str + current_str

                elif fields[key] is None:
                    data_str = data_str + "null"

                else:
                    data_str = data_str + self.dumps(fields[key])

                json_str = json_str + data_str

        json_str = json_str[:1] + json_str[3:] + "}"

        return  json_str



    def dump(self, obj, my_file):
        str_json = self.dumps(obj)

        try:
            my_file.write(str_json)
        except IOError:

            return 0

        return 1


    def load(self, my_file):
        dict_result = {}

        try:
            str_json = my_file.read()
            dict_result = self.loads(str_json)
        except IOError:

            return None

        return dict_result


    def loads(self,str_json):
        my_str_json = str_json[1:len(str_json) - 1]
        str_items = self.find_items_jsonstr(my_str_json)
        result_dict = self.make_dict_json(str_items)

        return result_dict


    def find_items_jsonstr(self, my_str_json):
        str_items = []
        str_item = ""
        stack_brakets = []
        stack_squre_brakets = []

        for i in range(len(my_str_json)):

            if my_str_json[i] == "{":
                stack_brakets.append("{")

            if my_str_json[i] == "}":
                stack_brakets.pop()

            if my_str_json[i] == "[":
                stack_squre_brakets.append("[")

            if my_str_json[i] == "]":
                stack_squre_brakets.pop()

            if my_str_json[i] == "," and not(len(stack_brakets)) and not(len(stack_squre_brakets)):
                str_items.append(str_item)
                str_item = ""
                continue

            str_item += my_str_json[i]

        str_items.append(str_item)

        return str_items


    def make_dict_json(self,my_str_items):
        my_dict = {}
        my_str_items[0] = " " + my_str_items[0]# добавляем пробел в начало превого будующего ключа, чтобы корректно обрезать его в дальнейшем вместе с остальными ключами

        for item in my_str_items:
            key_value = item.split(": ", 1)  # получаем ключ значения из нашего списка items(строк)
            key_value[0] = key_value[0][2:len(key_value[0]) - 1]  # преобразуем наш ключ, чтобы записать его в словарь без кавычек json
            key_value[1] = self.check_type_json(key_value[1])  # определяем тип значения json строки

            my_dict[key_value[0]] = key_value[1]

        return my_dict


    def check_type_json(self, my_value):

         if my_value[0] == '"':
             my_value = my_value[1:len(my_value) - 1]

             return my_value

         if my_value[0] == "t":

             return True

         if my_value[0] == "f":

             return False

         if my_value[0] == "[":
             my_list = []
             my_value = my_value[1:len(my_value)-1]
             my_str = ""

             for i in range(len(my_value)):

                 if my_value[i] == ',':

                     if my_str[0] == " ":
                         my_str = my_str[1:len(my_str)]

                     result = self.check_type_json(my_str)
                     my_list.append(result)
                     my_str = ""
                     continue

                 my_str += my_value[i]

             if my_str[0] == " ":
                 my_str = my_str[1:len(my_str)]
             my_list.append(self.check_type_json(my_str))

             return my_list

         if my_value[0] == "{":

             return self.loads(my_value)

         for i in range(len(my_value)):

             if my_value[i] == ".":

                 return float(my_value)

         return int(my_value)

    def make_dict_function(self, fun):
        attributes = dict(inspect.getmembers(fun))
        attributes_code = dict(inspect.getmembers(attributes['__code__']))
        result_code = {}
        result_globals = {}

        for key in attributes_code.keys():

            if key[0] != "_" and key != "replace":
                if not(isinstance(attributes_code[key], (int, float))) and len(attributes_code[key]) == 0:
                    result_code[key] = None
                else:
                    result_code[key] = attributes_code[key]


        return  {"__code__" : result_code, "__globals__" : result_globals,  "__name__" : attributes['__name__'], "__defult__" : attributes['__defualts__']}
