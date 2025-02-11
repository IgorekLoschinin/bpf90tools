#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2025-2026 Igor Loschinin.
# Distributed under the lgplv3 software license, see the accompanying
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.

__author__ = "Igor Loschinin (igor.loschinin@gmail.com)"

import pytest

from bpf90tools.src.bpf90tools.parsers import PPed
from . import _DIR_FILES


@pytest.fixture
def obj_renadd():
	return PPed()


def test_not_file_renadd(obj_renadd) -> None:
	_file = _DIR_FILES / "renadd_f/renaddksjhf.txt"

	with pytest.raises(OSError):
		obj_renadd.parse_file(_file)

	assert obj_renadd.values is None


def test_true_renadd1(obj_renadd) -> None:
	_file = _DIR_FILES / "renadd_f/renadd04_1.ped"

	assert obj_renadd.parse_file(_file)
	assert obj_renadd.values is not None and not obj_renadd.values.empty


def test_true_renadd2(obj_renadd) -> None:
	_file = _DIR_FILES / "renadd_f/renadd04_2.ped"

	assert obj_renadd.parse_file(_file)
	assert obj_renadd.values is not None and not obj_renadd.values.empty
