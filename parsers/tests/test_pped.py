#!/usr/bin/env python
# coding: utf-8
from pathlib import Path

from . import _DIR_FILES
from .. import PPed

import pytest

_FILES_PED = Path(_DIR_FILES) / "renadd_f"


@pytest.fixture
def obj_renadd():
	return PPed()


def test_not_file_renadd(obj_renadd) -> None:
	_file = _FILES_PED / "renaddksjhf.txt"

	with pytest.raises(OSError):
		obj_renadd.parse_file(_file)

	assert obj_renadd.values is None


def test_true_renadd1(obj_renadd) -> None:
	_file = _FILES_PED / "renadd04_1.ped"

	assert obj_renadd.parse_file(_file)
	assert obj_renadd.values is not None and ~obj_renadd.values.empty


def test_true_renadd2(obj_renadd) -> None:
	_file = _FILES_PED / "renadd04_2.ped"

	assert obj_renadd.parse_file(_file)
	assert obj_renadd.values is not None and ~obj_renadd.values.empty
