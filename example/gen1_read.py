# -*- coding: utf-8 -*-
from xml_template import *
from collections import OrderedDict


class InsClass:
    def __init__(self):
        pass


root_temp = XmlTemplate('root')
root_temp.params.append(XmlParam(ParamT(str), 'root_var_str', 'abc'))
root_temp.params.append(XmlParam(ParamT(int), 'root_var_int', 123))
root_temp.params.append(XmlParam(ParamT(float), 'root_var_float', 3.21))

root_node = XmlNode(root_temp)

read_ins = XmlTemplate.read_xml(root_node, InsClass, 'gen1.xml')




