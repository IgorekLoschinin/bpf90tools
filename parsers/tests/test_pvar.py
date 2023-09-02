#!/usr/bin/venv python
# coding: utf-8

from pytest import fixture, raises

from .. import PVar
from . import _DIR_FILES


@fixture
def parser():
	return PVar()


def test_file_no_exists(parser):
	file_no_exists = _DIR_FILES / "var_log/_file.txt"

	with raises(
			OSError,
			match=f"The path - {file_no_exists.stem}, passed is not a file!"
	):
		parser.parse_file(file_no_exists)


def test_no_var_log(parser) -> None:
	file = _DIR_FILES / "var_log/no_file.txt"

	assert parser.parse_file(file)

	assert all([
		True if item is None
		else False
		for item in parser.values.dict().values()
	])


def test_aireml_log_1(parser) -> None:
	file = _DIR_FILES / "var_log/airemlf90_1.log"

	assert parser.parse_file(file)

	assert None not in parser.values.dict().values()
	assert parser.values.varE == 0
	assert parser.values.varG == 0
	assert parser.values.heritability == 0


def test_aireml_log_2(parser) -> None:
	file = _DIR_FILES / "var_log/airemlf90_2.log"

	assert parser.parse_file(file)

	assert all([
		True if parser.values.dict()[item] > 0.0
		else False
		for item in filter(
			lambda x: parser.values.dict()[x] if x != "heritability" else None,
			parser.values.dict().keys()
		)
	])


def test_aireml_log_3(parser) -> None:
	file = _DIR_FILES / "var_log/airemlf90_3.log"

	assert parser.parse_file(file)

	assert all([
		True if item is None
		else False
		for item in parser.values.dict().values()
	])


def test_reml_log_1(parser) -> None:
	file = _DIR_FILES / "var_log/remlf90_1.log"

	assert parser.parse_file(file)

	assert None not in parser.values.dict().values()
	assert parser.values.varE == 0
	assert parser.values.varG == 0
	assert parser.values.heritability == 0


def test_reml_log_2(parser) -> None:
	file = _DIR_FILES / "var_log/remlf90_2.log"

	assert parser.parse_file(file)

	assert all([
		True if parser.values.dict()[item] > 0.0
		else False
		for item in filter(
			lambda x: parser.values.dict()[x] if x != "heritability" else None,
			parser.values.dict().keys()
		)
	])


def test_reml_log_3(parser) -> None:
	file = _DIR_FILES / "var_log/remlf90_3.log"

	assert parser.parse_file(file)

	assert all([
		True if item is None
		else False
		for item in parser.values.dict().values()
	])
