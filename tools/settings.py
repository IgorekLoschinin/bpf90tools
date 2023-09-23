#!/usr/bin/env python
# coding: utf-8

__author__ = "Igor Loschinin (igor.loschinin@gmail.com)"

import re

BLUPF90 = 'blupf90'
REMLF90 = 'remlf90'
RENUMF90 = 'renumf90'
AIREMLF90 = 'airemlf90'

RENF90_PAR = "renf90.par"
REMLF90_LOG = "remlf90.log"
AIREMLF90_LOG = "airemlf90.log"
SOLUTIONS = "solutions"
RENADD = re.compile(r"(^renadd[0-9]*.ped\b)")
PARAM_FILE = "param.txt"
