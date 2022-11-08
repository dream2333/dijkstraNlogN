#!/usr/bin/env python3


class Command:
    """
    The decorator can turn a function or method into a command line input program and add a callback function to it

    types :
        The data type or type conversion function corresponding to the command line argument
    call_back :
        Callback function executed after each command line is executed
    end_flag :
        String representing the end of the command run
    """

    # Split the input string and parse the parameters
    def __init__(self, *types, call_back, end_flag):
        self.func = None
        self.types = types
        self.call_back = call_back
        self.end_flag = end_flag

    @staticmethod
    def space_sep_list(str):
        return str.split(" ")

    @staticmethod
    def comma_sep_list(str):
        return str.split(",")

    # Decorators for turning functions into command line commands

    def __call__(self, func):
        def inner(*args,**kw):
            while True:
                typed_params = []
                cmd_line = input()
                # Split command line commands into list items and convert the type of parameters
                paras = self.space_sep_list(cmd_line)
                if len(paras) == 1 and paras[0] == self.end_flag:
                    return
                for index, arg in enumerate(paras):
                    typed_params.append(self.types[index](paras[index]))
                # Run the wrapped function
                result = func(*typed_params)
                if self.call_back != None:
                    self.call_back(result)
        return inner

if __name__ == "__main__":

    @Command(str, int, Command.comma_sep_list, call_back=print, end_flag="STATELINK")
    def test(str_field, int_field, list_field):
        return (str_field, int_field, list_field)

    i = Command.test()
