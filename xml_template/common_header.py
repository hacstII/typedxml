# -*- coding: utf-8 -*-
# from __future__ import annotations
from typing import Tuple, List, Any, Optional, Union, TypeVar, Generic, Iterable, Dict, Type, ClassVar, Set, Container
from typing_extensions import Literal
import numpy as np
from lxml import etree
from collections import OrderedDict, abc
import warnings


ElementTree = etree._ElementTree
Element = etree._Element

TBool = Union[Tuple[bool], bool]

Label = Union[str, int]
DBool = Union[Dict[Label, bool], bool]
DStr = Union[Dict[Label, str], str]
DAny = Union[Dict[Label, Any], Any]



# T = TypeVar('T')
#
#
# class UdTE:
#     def __getitem__(self, item: T):
#         return Union[Tuple[T], T]
#
#
# ud_te = UdTE()
