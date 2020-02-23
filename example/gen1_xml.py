# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from lxml import etree

# 创建一个annotion节点
root = etree.Element('root')
# 创建一个子节点folder，一定要指定父节点
child_root_var_str = etree.SubElement(root, 'root_var_str')
child_root_var_str.text = 'Some text'

child_root_var_int = etree.SubElement(root, 'root_var_int')
child_root_var_int.text = '147'

child_root_var_float = etree.SubElement(root, 'root_var_float')
child_root_var_float.text = '5.31'

root_group = etree.SubElement(root, 'group')
group_sub_var_str = etree.SubElement(root_group, 'sub_var_str')
group_sub_var_str.text = 'text in group'
group_sub_var_int = etree.SubElement(root_group, 'sub_var_int')
group_sub_var_int.text = '258'
group_sub_var_float = etree.SubElement(root_group, 'sub_var_float')
group_sub_var_float.text = '9.63'



#
# child31 = etree.SubElement(child3, 'database')
# child31.text = 'VOC'
#
# child4 = etree.SubElement(root, 'size')
# child4.append(etree.Comment('lala1'))
#
# child41 = etree.SubElement(child4, 'width')
# child41.text = '458'
#
# child4.append(etree.Comment('lala2'))
#
# child42 = etree.SubElement(child4, 'height')
# child42.text = '45'
#
# child4.append(etree.Comment('lala3'))
#
# child43 = etree.SubElement(child4, 'height')
# child43.text = '45'
#
# child5 = etree.SubElement(root, 'segmented')
# child5.text = '0'
# # 自定义数据集
# objectlist = [{'xmin': 263, 'ymin': 211, 'xmax': 324, 'ymax': 339},
#               {'xmin': 5, 'ymin': 224, 'xmax': 67, 'ymax': 374}]
#
# for i in objectlist:
#     child6 = etree.SubElement(root, 'object')
#
#     child61 = etree.SubElement(child6, 'name')
#     child61.text = 'face'
#
#     child62 = etree.SubElement(child6, 'pose')
#     child62.text = 'Unspecified'
#
#     child63 = etree.SubElement(child6, 'truncated')
#     child63.text = '0'
#
#     child64 = etree.SubElement(child6, 'difficult')
#     child64.text = '0'
#
#     child65 = etree.SubElement(child6, 'bndbox')
#
#     child651 = etree.SubElement(child65, 'xmin')
#     child651.text = str(i['xmin'])
#
#     child652 = etree.SubElement(child65, 'ymin')
#     child652.text = str(i['ymax'])
#
#     child653 = etree.SubElement(child65, 'xmax')
#     child653.text = str(i['xmax'])
#
#     child654 = etree.SubElement(child65, 'ymax')
#     child654.text = str(i['ymax'])

tree = etree.ElementTree(root)
tree.write('gen1.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')
