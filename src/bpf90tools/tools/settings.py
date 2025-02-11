#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2025-2026 Igor Loschinin.
# Distributed under the lgplv3 software license, see the accompanying
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.

__author__ = "Igor Loschinin (igor.loschinin@gmail.com)"
__all__ = (
	"BLUPF90",
	"REMLF90",
	"RENUMF90",
	"AIREMLF90",
	"RENF90_PAR",
	"REMLF90_LOG",
	"AIREMLF90_LOG",
	"SOLUTIONS",
	"RENADD",
	"PARAM_FILE",
)

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
