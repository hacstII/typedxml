# -*- coding: utf-8 -*-
from __future__ import annotations
from .common_header import *

# TODO adding program function
# TODO adding label function


def get_unique_mark(con: Container[str], expected_str: str) -> Tuple[str, int]:
    if expected_str not in con:
        return expected_str, 0
    else:
        now_ind = 1
        while True:
            try_str = expected_str + '_' + str(now_ind)
            if try_str not in con:
                return try_str, now_ind
            else:
                now_ind += 1


def camel_to_snake(name: str) -> str:
    """CamelCase to snake_case

    refereed from https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case

    Args:
        name (str): [description]

    Returns:
        str: [description]
    """
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def mix_label_to_str(mix_label: MLabel) -> str:
    if isinstance(mix_label, str):
        return mix_label
    else:
        label_int = int(mix_label)
        return "label_"+str(label_int)


def mixdict_to_strdict(mix_dict_or_value: Union[Dict[MLabel, T], T]) -> Union[Dict[str, T], T]:
    if isinstance(mix_dict_or_value, dict):
        new_dict: Dict[str, T] = OrderedDict()
        for key in mix_dict_or_value:
            labelstr: str = mix_label_to_str(key)
            if labelstr in new_dict:
                raise
            new_dict[labelstr] = mix_dict_or_value[key]
        ret_value: Union[Dict[str, T], T] = new_dict
    else:
        ret_value = mix_dict_or_value
    return ret_value


def get_dictvalue_result(dictvalue: Union[Dict[str, T], T], mix_label: MLabel = 0) -> T:
    # DEFLABEL processing label is not included
    labelstr: str = mix_label_to_str(mix_label)
    if isinstance(dictvalue, dict):
        ret_val: T = dictvalue[labelstr]
    else:
        ret_val = dictvalue
    return ret_val



def is_read_from_tbool(tbool: TBool, prog_cind: CInt) -> bool:
    if isinstance(tbool, tuple):
        if isinstance(prog_cind, abc.Collection):
            any_val: bool = False
            for ind in prog_cind:
                if tbool[ind]:
                    any_val = True
                    break
            ret_bool: bool = any_val

        else:
            # prog_cind is int
            if prog_cind == -1:
                ret_bool = True
            else:
                ret_bool = tbool[prog_cind]
    else:
        # tbool is bool
        ret_bool = tbool
    return ret_bool


class EmptyClass:
    pass


class Self:
    def __init__(self):
        pass


class Eval:
    def __init__(self):
        pass


class ParseType:
    is_eval: bool
    is_multi: bool
    multi_type: Optional[type]  # Optional[Literal[list, tuple]]
    iter_type: Optional[type]  # Optional[Literal[list, tuple]]
    is_ndarray: bool
    is_string: bool
    final_type: Optional[type]
    """ParamT._final_number_types"""
    __slots__ = ['is_eval', 'is_multi', 'multi_type', 'iter_type', 'is_ndarray', 'is_string', 'final_type']

    def __init__(self):
        self.is_eval = False
        self.is_multi = False
        self.multi_type = None
        self.iter_type = None
        self.is_ndarray = False
        self.is_string = False
        self.final_type = None


class XmlTemplate:
    _current_scope: ClassVar[str] = 'default_scope'
    # _dict_of_scope: ClassVar[Dict, Dict] = OrderedDict()
    # _dict_of_templates: ClassVar[Dict[str, XmlTemplate]] = OrderedDict()
    _dict_of_scope: ClassVar[Dict[str, Dict[str, XmlTemplate]]]
    _dict_of_templates: ClassVar[Dict[str, XmlTemplate]]

    def __init__(self, name: str):
        # TODO adding optional paramters
        self.name = name  # The default name for this in xml file's node, The generated class name
        self.labels: Tuple[str, ...] = (mix_label_to_str(0),)
        self.params: List[Union[XmlParam, XmlNode, XmlNodeDummy]] = []
        self.special_class = None
        self.comment = ''
        self.mark = name
        '''unique str label of this template. So that XmlNode can ref
        by XmlNode with string. Typically same with name
        '''
        self._already_set_ulabel = True
        ''' indicate whether ulabel has already been set
        '''
        self._add_template_dict(self.mark, self)
        self._already_avatar = False
        ''' if it's params and related childrens already has no XmlNodeDummy
        '''

    def dummy_to_avatar(self) -> None:
        if self._already_avatar:
            return
        for ind, member in enumerate(self.params):
            if isinstance(member, XmlNodeDummy):
                xmlnode = member.avatar()
                xmlnode.xml_template.dummy_to_avatar()
                self.params[ind] = xmlnode
            if isinstance(member, XmlNode):
                member.xml_template.dummy_to_avatar()
        self._already_avatar = True
        return

    def check_avatar(self) -> bool:
        if not self._already_avatar:
            return False
        else:
            for ind, member in enumerate(self.params):
                if isinstance(member, XmlNodeDummy):
                    raise
                if isinstance(member, XmlNode):
                    if not member.xml_template.check_avatar():
                        raise
            return True

    @classmethod
    def _add_template_dict(cls, key: str, value: XmlTemplate):
        # TODO check key already exists
        cls._dict_of_templates[key] = value

    @classmethod
    def get_template_dict_value(cls, key: str) -> Optional[XmlTemplate]:
        return cls._dict_of_templates.get(key, None)

    @classmethod
    def read_xml(cls, xmlnode: XmlNode, param_class: Optional[type], xml_path,
                 param_ins_dict: Optional[Dict[str, Any]] = None, param_ins=None, prog_ind=-1):
        XmlNode.reset_set_ins_mark()
        et: ElementTree = etree.parse(xml_path)
        node_root: Element = et.getroot()

        # param_ins_dict: Dict[str, object]  # Dict of all instance of parameter class
        # key: string of unique name of instances, i.e., value: reference of these instances
        if param_ins_dict is None:
            param_ins_dict = OrderedDict()

        if param_class is None:
            param_class_nn: type = EmptyClass  # param_class not None
        else:
            param_class_nn = param_class

        if param_ins is None:
            param_ins = param_class_nn()
        if not isinstance(param_ins, param_class_nn):
            raise

        xmlnode.xml_template.dummy_to_avatar()
        xmlnode.xml_template.check_avatar()
        xmlnode.read_xml_element(node_root, param_ins, param_ins_dict, '', prog_cind=prog_ind)
        return param_ins

    @classmethod
    def generate_parameter_file(cls, filename: str):
        # TODO 0327
        pass

    @classmethod
    def get_scope(cls) -> str:
        return cls._current_scope

    @classmethod
    def add_scope(cls, scope: str):
        if scope in cls._dict_of_scope:
            raise
        cls._dict_of_scope[scope] = OrderedDict()
        cls.set_scope(scope)

    @classmethod
    def set_scope(cls, scope: str):
        if scope not in cls._dict_of_scope:
            raise
        cls._current_scope = scope
        cls._dict_of_templates = cls._dict_of_scope[cls._current_scope]

    @classmethod
    def _init_cls(cls):
        cls._dict_of_scope = OrderedDict()
        cls._dict_of_templates = OrderedDict()
        cls._dict_of_scope[cls._current_scope] = cls._dict_of_templates


def _gcf_header() -> List[str]:
    ret_list: List[str] = ['# -*- coding: utf-8 -*-\n']
    return ret_list


def _gcf_emptylines(line_num: int) -> List[str]:
    ret_list: List[str] = ['\n' * line_num]
    return ret_list


class ParamT:
    _final_number_types: Tuple[type, ...] = (int, float, complex, bool, np.int64, np.float64, np.bool8, np.complex128,)
    _string_types: Tuple[type, ...] = (str, )
    _array_types: Tuple[type, ...] = (np.ndarray,)
    _list_types: Tuple[type, ...] = (list, tuple, )
    _eval_types: Tuple[Literal['eval'], ...] = ('eval', )
    _multi_types: Tuple[Literal['multilist', 'multituple'], ...] = ('multilist', 'multituple', )

    def __init__(self, *args: Union[str, type]):
        self.type = args
        # self.final_type = self.type[-1]
        self.parse_type = self.get_parse_type()

        # TODO check valid of args

    @classmethod
    def convert_value(cls, value_in):
        # TODO convert value to self.type
        return value_in

    def read_one_line(self, data_node: Element):
        read_str_raw = data_node.text
        assert read_str_raw is not None
        read_str: str = str(read_str_raw)
        if self.parse_type.is_string:
            # if is_string
            if self.parse_type.is_eval:
                return str(eval(read_str))
            else:
                return read_str
        elif self.parse_type.is_eval:
            # is not is_string, so finot type shouldn't be None
            assert self.parse_type.final_type is not None
            eval_result = eval(read_str)
            if self.parse_type.is_ndarray:
                temp_arr = np.array(eval_result, dtype=self.parse_type.final_type)
                return np.atleast_1d(temp_arr)
            elif self.parse_type.iter_type is not None:
                if isinstance(eval_result, abc.Iterable):
                    ret_list = [self.parse_type.final_type(number) for number in eval_result]
                else:
                    ret_list = [self.parse_type.final_type(eval_result)]
                return self.parse_type.iter_type(ret_list)
            else:
                return self.parse_type.final_type(eval_result)
        else:
            # is not is_string, so finot type shouldn't be None
            assert self.parse_type.final_type is not None
            # strip '[]', '()'
            strip_str = read_str.strip()
            further_strip = False
            stard_ind = 0
            end_ind = len(strip_str)
            if strip_str[0] in ('[', '('):
                further_strip = True
                stard_ind += 1
            if strip_str[-1] in (')', ']'):
                further_strip = True
                end_ind -= 1
            if further_strip:
                strip_str = strip_str[stard_ind:end_ind]

            # read as ndarray, no matter list, tuple, ndarray, or scale
            read_arr = np.fromstring(strip_str, dtype=self.parse_type.final_type, sep=' ')
            for sep in (',', ';', '\t'):
                read_arr_other = np.fromstring(strip_str, dtype=self.parse_type.final_type, sep=sep)
                if read_arr_other.size > read_arr.size:
                    read_arr = read_arr_other

            if self.parse_type.is_ndarray:
                return read_arr
            elif self.parse_type.iter_type is not None:
                return self.parse_type.iter_type(self.parse_type.final_type(ele) for ele in read_arr)
            else:
                return self.parse_type.final_type(read_arr[0])

    def get_value(self, parent_node: Element, element_name: str) -> Any:
        ele_list: List[Element] = parent_node.findall(element_name)
        if self.parse_type.is_multi:
            if self.parse_type.multi_type is None:
                raise TypedxmlException("read multi target name nodes but self.parse_type.multi_type is None")
            return self.parse_type.multi_type(self.read_one_line(ele) for ele in ele_list)
        else:
            if len(ele_list) == 0:
                return None
            elif len(ele_list) == 1:
                return self.read_one_line(ele_list[0])
            else:
                raise
        # if len(ele_list) == 0:
        #     return None
        # elif self.parse_type.is_multi:
        #     if self.parse_type.multi_type is None:
        #         raise TypedxmlException("read multi target name nodes but self.parse_type.multi_type is None")
        #     return self.parse_type.multi_type(self.read_one_line(ele) for ele in ele_list)
        # elif len(ele_list) == 1:
        #     return self.read_one_line(ele_list[0])
        # else:
        #     raise
        # #
        # #
        # #
        # # ele_new: Optional[Element] = parent_node.find(element_name)
        # # if ele_new is None:
        # #     return None
        # # ret_value = self.final_type(ele_new.text)
        # # return ret_value

    def get_parse_type(self) -> ParseType:
        parse_type = ParseType()
        type_list = list(self.type)
        if len(type_list) == 0:
            raise
        read_ind = 0
        if type_list[read_ind] in self._eval_types:
            parse_type.is_eval = True
            read_ind += 1
        if type_list[read_ind] in self._multi_types:
            parse_type.is_multi = True
            if type_list[read_ind] is 'multilist':
                parse_type.multi_type = list
            elif type_list[read_ind] is 'multituple':
                parse_type.multi_type = tuple
            else:
                raise
            read_ind += 1
        if type_list[read_ind] in self._list_types:
            read_type: type = type_list[read_ind]  # type: ignore
            parse_type.iter_type = read_type
            read_ind += 1
        elif type_list[read_ind] in self._array_types:
            parse_type.is_ndarray = True
            read_ind += 1
        if read_ind != len(type_list) - 1:
            raise
        if type_list[read_ind] in self._string_types:
            parse_type.is_string = True
        elif type_list[read_ind] in self._final_number_types:
            read_type = type_list[read_ind]  # type: ignore
            parse_type.final_type = read_type
        else:
            raise
        return parse_type

    def get_copy_val(self, ori_val: Any) -> Any:
        # TODO consider return the copy of the result
        pass


class XmlParam:
    param_type: ParamT
    xml_name: str
    var_name: str
    is_read: TBool
    can_default: DBool
    default_value: DAny
    comment: DStr

    def __init__(self, param_type: ParamT, xml_name: str, default_value: Optional[IDAny] = None, var_name: Optional[str] = None,
                 is_read: TBool = True, can_default: IDBool = True, comment: Optional[IDStr] = None):
        self.param_type = param_type
        self.xml_name = xml_name  # element name in xml
        if var_name is None:  # variable name in parameter class
            self.var_name = xml_name
        else:
            self.var_name = var_name
        self.is_read = is_read
        self.can_default = mixdict_to_strdict(can_default)

        self.default_value = self.convert_default_value(default_value)
        if comment is None:
            self.comment = ''
        else:
            self.comment = mixdict_to_strdict(comment)

    def convert_default_value(self, default_value: Optional[IDAny]) -> DAny:
        if default_value is None:
            return self.param_type.convert_value(None)
        else:
            dict_or_value: DAny = mixdict_to_strdict(default_value)
            if dict_or_value is dict:
                for key in dict_or_value:
                    dict_or_value[key] = self.param_type.convert_value(dict_or_value[key])
                ret_value: DAny = dict_or_value
            else:
                ret_value = self.param_type.convert_value(dict_or_value)
            return ret_value

    def read_xml(self, element: Optional[Element], param_ins: object, mix_label: MLabel, prog_cind: CInt = -1):
        # DEFLABEL processing label is not included
        if self.get_is_read(prog_cind):
            if element is None:
                if self.get_can_default(mix_label):
                    read_value = self.get_default_value(mix_label)
                else:
                    raise
            else:
                read_value = self.param_type.get_value(element, self.xml_name)
            if read_value is not None:
                # TODO check has that property
                set_value = read_value
                param_ins.__setattr__(self.var_name, read_value)
            else:
                if self.get_can_default(mix_label):
                    set_value = self.get_default_value(mix_label)
                    param_ins.__setattr__(self.var_name, set_value)
                else:
                    raise
            return set_value
        else:
            return None

    def get_is_read(self, prog_cind: CInt = -1) -> bool:
        ret_bool: bool = is_read_from_tbool(self.is_read, prog_cind)
        return ret_bool

    def get_can_default(self, mix_label: MLabel = 0) -> bool:
        # DEFLABEL processing label is not included
        ret_bool: bool = get_dictvalue_result(self.can_default, mix_label)
        return ret_bool

    def get_default_value(self, mix_label: MLabel = 0) -> Any:
        # TODO consider return the copy of the result
        # DEFLABEL processing label is not included
        ret_val: Any = get_dictvalue_result(self.default_value, mix_label)
        return ret_val

    def get_comment(self, mix_label: MLabel = 0) -> str:
        ret_str: str = get_dictvalue_result(self.comment, mix_label)
        return ret_str


class XmlNodeDummy:
    """used to postpone initialization of XmlNode
    """
    def __init__(self, xml_template_mark: str, node_name=None, var_name=None,
                 label_index: Union[MLabel, Dict[MLabel, MLabel], Self] = 0,
                 is_read: TBool = True, can_default: IDBool = True, comment: Optional[str] = None):
        self.xml_template_mark = xml_template_mark
        self.node_name = node_name
        self.var_name = var_name
        self.label_index = label_index
        self.is_read = is_read
        self.can_default = can_default
        self.comment = comment

    def avatar(self) -> XmlNode:
        xml_template = XmlTemplate.get_template_dict_value(self.xml_template_mark)
        if xml_template is None:
            raise
        else:
            return XmlNode(xml_template, self.node_name, self.var_name, self.label_index, self.is_read,
                           self.can_default, self.comment)

# TODO


class XmlNode:
    _set_ins_mark: ClassVar[Set[str]] = set()  # set of instance of name
    xml_template: XmlTemplate
    node_name: str
    var_name: str
    label_index: Union[str, Dict[str, str], Self]
    is_read: TBool
    can_default: DBool
    comment: Optional[DStr]

    def __init__(self, xml_template: XmlTemplate, node_name: Optional[str] = None, var_name: Optional[str] = None,
                 label_index: Union[MLabel, Dict[MLabel, MLabel], Self] = 0,
                 is_read: TBool = True, can_default: IDBool = True, comment: Optional[IDStr] = None):

        self.xml_template: XmlTemplate = xml_template
        if node_name is None:
            self.node_name: str = xml_template.name
        else:
            self.node_name = node_name
            '''
            node_name: The node name in XML
            '''

        if var_name is None:
            self.var_name: str = camel_to_snake(self.node_name)
        else:
            self.var_name = var_name
            '''
            the name of the variable in Parent Template definition, default is the lower case of the
            '''

        if isinstance(label_index, dict):
            label_dict: Dict[str, str] = OrderedDict()
            for key in label_index:
                label_dict[mix_label_to_str(key)] = mix_label_to_str(label_index[key])
            # if label_index is  dict, it should be Dict[str, Label]. if it is Dict[int, Label], int will convert to
            # 'label_$int$
            label_index_real: Union[str, Dict[str, str], Self] = label_dict
        elif isinstance(label_index, Self):
            label_index_real = label_index
        else:
            # label_index is MLabel
            label_index_real = mix_label_to_str(label_index)
        self.label_index = label_index_real
        '''
        The label_index of self.typedxml to realized
        str or int or Self or Dict, if is int, the corresponding string is self.typedxml.labels[int]
        '''
        # one type, two xml node; only one value

        self.is_read = is_read  # one config, two prog; can be Tuple[bool] or [bool]

        self.can_default = mixdict_to_strdict(can_default)
        if comment is None:
            self.comment = None
        else:
            self.comment = mixdict_to_strdict(comment)
        # self.ulabel = ulabel

    def read_xml_element(self, element: Optional[Element], param_ins, param_ins_dict: Dict, upper_ins_mark: str,
                         upper_template_label: Optional[str] = None, prog_cind: CInt = -1) -> bool:
        """
        Set value to param_ins by reading Element,
        set the node_label of the param_ins and save the node_label to _set_ins_name and adds the relation
        to param_ins_dict

        change the value of param_ins

        :param element:
        :param param_ins:
        :param param_ins_dict:
        :param upper_template_label: the "labelstr" of the parent instance of XmlNode.(Parent template)
        :param upper_ins_mark:
        :param prog_cind:
        :return:
        """
        real_template_label: str = self.get_real_template_label(upper_template_label)

        if element is None:
            if not self.get_can_default(real_template_label):
                raise
        else:
            if element.tag != self.node_name:
                raise

        if len(upper_ins_mark) == 0:
            expected_ins_mark = self.node_name
        else:
            expected_ins_mark = upper_ins_mark + '->' + self.node_name
        ins_mark, running_ind = get_unique_mark(self._set_ins_mark, expected_ins_mark)
        if running_ind > 0:
            warnings.warn('running_ind > 0, running_ind = {}'.format(running_ind))

        if self.get_is_read(prog_cind):  # As this should be checked before read_xml_element, it must be true
            param_ins.__setattr__('_parent_ins_mark', upper_ins_mark)
            param_ins.__setattr__('_ins_mark', ins_mark)
            self.add_set_ins_mark(ins_mark)
            if ins_mark not in param_ins_dict:
                param_ins_dict[ins_mark] = param_ins
            else:
                raise

            member: Union[XmlParam, XmlNode, XmlNodeDummy]
            for member in self.xml_template.params:
                if isinstance(member, XmlParam):
                    member.read_xml(element, param_ins, real_template_label, prog_cind)
                elif isinstance(member, XmlNode):
                    if member.get_is_read(prog_cind):
                        if member.var_name not in param_ins.__dir__():
                            param_ins.__setattr__(member.var_name, EmptyClass())
                        param_ins_child = param_ins.__getattribute__(member.var_name)
                        if element is None:
                            element_child = None
                        else:
                            element_list = element.findall(member.node_name)
                            if len(element_list) == 0:
                                element_child = None
                            elif len(element_list) == 1:
                                element_child = element_list[0]
                            else:
                                raise
                        member.read_xml_element(element_child, param_ins_child, param_ins_dict, ins_mark,
                                                upper_template_label=real_template_label, prog_cind=prog_cind)
                elif isinstance(member, XmlNodeDummy):
                    raise
                else:
                    raise
        else:
            raise
        return param_ins

    def get_real_template_label(self, upper_template_label: Optional[str] = None) -> str:
        # DEFLABEL processing label is not included. Now if self.label_index is dict, None will results error
        # get the real string label of this node
        if isinstance(self.label_index, dict):
            if upper_template_label is None:
                raise
            ret_str: str = self.label_index[upper_template_label]
        elif isinstance(self.label_index, Self):
            if upper_template_label is None:
                raise
            ret_str = upper_template_label
        else:
            ret_str = self.label_index
        return ret_str

    def get_is_read(self, prog_cind: CInt = -1) -> bool:
        ret_bool: bool = is_read_from_tbool(self.is_read, prog_cind)
        return ret_bool
        # if prog_ind < 0:
        #     return True
        # if isinstance(self.is_read, tuple):
        #     return self.is_read[prog_ind]
        # else:
        #     return self.is_read

    # def get_node_name(self, label_index: MLabel = 0) -> str:
    #     if isinstance(self.node_name, dict):
    #         pass
    #     else:
    #         return self.node_name

    def get_can_default(self, mix_label: MLabel = 0) -> bool:
        # DEFLABEL processing label is not included
        ret_bool: bool = get_dictvalue_result(self.can_default, mix_label)
        return ret_bool
    # def get_can_default(self, label: Optional[MLabel] = None) -> bool:
    #     if label is None:
    #         label_cal: MLabel = 0
    #     else:
    #         label_cal = label
        # if isinstance(self.)
        # label_str: str = get_expected_labelstr(label_cal)
        # TODO
        # if isinstance(self.can_default, dict):
        #     tuple_or_value = self.can_default[label_index]
        # else:
        #     tuple_or_value = self.can_default
        # if isinstance(tuple_or_value, tuple):
        #     ret_value = tuple_or_value[prog_ind]
        # else:
        #     ret_value = tuple_or_value
        # return self.can_default

    @classmethod
    def reset_set_ins_mark(cls):
        cls._set_ins_mark.clear()

    @classmethod
    def add_set_ins_mark(cls, ins_mark: str):
        cls._set_ins_mark.add(ins_mark)

    def refresh(self):
        # TODO if xml_template is still string, refresh
        pass














