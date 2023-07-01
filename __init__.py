#!/usr/bin/env python
# coding: utf-8

from .params import Params
from .blupf90 import Blupf90
from .airemlf90 import AIremlf90
from .remlf90 import Remlf90
from .renumf90 import Renumf90
from bpf90tools.parsers.keyword import Keyword

BLUPF90 = 'blupf90'
REMLF90 = 'remlf90'
RENUMF90 = 'renumf90'
AIREMlF90 = 'airemlf90'

RENF90_PAR = "renf90.par"
REMLF90_LOG = "remlf90.log"
AIREML_LOG = "airemlf90.log"
PARAM_FILE = "param.txt"

__all__ = [
	'Params',
	'Blupf90',
	'AIremlf90',
	'Remlf90',
	'Renumf90',
	'BLUPF90',
	'REMLF90',
	'RENUMF90',
	'AIREMlF90',
	'RENF90_PAR',
	'REMLF90_LOG',
	'AIREML_LOG',
	'PARAM_FILE'
]
