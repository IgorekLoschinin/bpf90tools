#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2025-2026 Igor Loschinin.
# Distributed under the lgplv3 software license, see the accompanying
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.

__author__ = "Igor Loschinin (igor.loschinin@gmail.com)"

import pytest

from bpf90tools.src.bpf90tools.parsers import PSolution
from . import _DIR_FILES


@pytest.fixture
def obj_sol():
	return PSolution()


def test_not_sol_file(obj_sol):
	_file = _DIR_FILES / "sol_f/solutions123"

	with pytest.raises(OSError):
		obj_sol.parse_file(_file)


def test_parser_sol11(obj_sol) -> None:
	_file = _DIR_FILES / "sol_f/solutions1"

	assert obj_sol.parse_file(_file)
	assert obj_sol.solutions is not None and not obj_sol.solutions.empty
	assert (obj_sol.solutions.columns == ["EBV", "SE", "level"]).all()


def test_parser_sol12(obj_sol) -> None:
	_file = _DIR_FILES / "sol_f/solutions1"

	obj_sol._varg = 1
	assert obj_sol.parse_file(_file)
	assert obj_sol.solutions is not None and not obj_sol.solutions.empty
	assert (obj_sol.solutions.columns == ["EBV", "REL", "level"]).all()


def test_parser_sol13(obj_sol) -> None:
	_file = _DIR_FILES / "sol_f/solutions1"

	obj_sol._varg = 0

	with pytest.raises(ZeroDivisionError):
		obj_sol.parse_file(_file)


def test_parser_sol2(obj_sol) -> None:
	_file = _DIR_FILES / "sol_f/solutions2"

	assert obj_sol.parse_file(_file)
	assert obj_sol.solutions is not None and not obj_sol.solutions.empty
	assert (obj_sol.solutions.columns == ["EBV", "level"]).all()


def test_parser_sol3(obj_sol) -> None:
	_file = _DIR_FILES / "sol_f/solutions3"

	assert obj_sol.parse_file(_file)
	assert obj_sol.solutions is not None and obj_sol.solutions.empty


def test_parser_sol4(obj_sol) -> None:
	_file = _DIR_FILES / "sol_f/solutions4"

	with pytest.raises(Exception):
		obj_sol.parse_file(_file)


def test_parser_sol5(obj_sol) -> None:
	_file = _DIR_FILES / "sol_f/solutions5"

	with pytest.raises(Exception):
		obj_sol.parse_file(_file)
