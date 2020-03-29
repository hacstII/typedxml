# -*- coding: utf-8 -*-
# from __future__ import annotations
from typing import Tuple, List, Any, Optional, Union, TypeVar, Generic, Iterable, Dict, Type, ClassVar, Set, Container, Collection
from typing_extensions import Literal
import numpy as np
from lxml import etree
from collections import OrderedDict, abc
import warnings
import re


ElementTree = etree._ElementTree
Element = etree._Element

TBool = Union[Tuple[bool], bool]
T = TypeVar('T')

MLabel = Union[str, int]
IDBool = Union[Dict[MLabel, bool], bool]
IDStr = Union[Dict[MLabel, str], str]
IDAny = Union[Dict[MLabel, Any], Any]

DBool = Union[Dict[str, bool], bool]
DStr = Union[Dict[str, str], str]
DAny = Union[Dict[str, Any], Any]

CInt = Union[Collection[int], int]



class TypedxmlException(Exception):
    pass


# T = TypeVar('T')
#
#
# class UdTE:
#     def __getitem__(self, item: T):
#         return Union[Tuple[T], T]
#
#
# ud_te = UdTE()
