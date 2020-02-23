# -*- coding: utf-8 -*-
from xml_template import *
from collections import OrderedDict


class InsClass:
    def __init__(self):
        self.root_var_str = ''
        self.root_var_int = 0
        self.root_var_float = 0.0
        self.group = Group()


class Group:
    def __init__(self):
        self.sub_var_str = ''
        self.sub_var_int = 0
        self.sub_var_float = 0.0


group_temp =XmlTemplate('Group')
group_temp.params.append(XmlParam(ParamT(str), 'sub_var_str', 'def'))
group_temp.params.append(XmlParam(ParamT(int), 'sub_var_int', 456))
group_temp.params.append(XmlParam(ParamT(float), 'sub_var_float', 6.54))

root_temp = XmlTemplate('root')
root_temp.params.append(XmlParam(ParamT(str), 'root_var_str', 'abc'))
root_temp.params.append(XmlParam(ParamT(int), 'root_var_int', 123))
root_temp.params.append(XmlParam(ParamT(float), 'root_var_float', 3.21))
root_temp.params.append(XmlNode(group_temp))
root_temp.params.append(XmlNodeDummy('Group2'))

group_temp =XmlTemplate('Group2')
group_temp.params.append(XmlParam(ParamT(str), 'sub2_var_str', 'def'))
group_temp.params.append(XmlParam(ParamT(int), 'sub2_var_int', 456))
group_temp.params.append(XmlParam(ParamT(float), 'sub2_var_float', 6.54))

root_node = XmlNode(root_temp)


read_ins = XmlTemplate.read_xml(root_node, InsClass, 'gen2.xml')
ins_dict = OrderedDict()
read_ins2 = XmlTemplate.read_xml(root_node, InsClass, 'gen2.xml', ins_dict)




