#!/usr/bin/venv python
# coding: utf-8
from pathlib import Path
from .. import PParams
from . import _DIR_FILES
from pytest import fixture

_TEST_FILES = Path(_DIR_FILES) / "pparam_f"


@fixture
def parser():
	return PParams()


def test_parse_aireml_log_1(parser) -> None:
	# file = _TEST_FILES / "param1.txt"

	file = "/home/igorek/Документы/DEVPERSONAL/PROJECTS/ebvprojects/devTools/bpf90tools/parsers/tests/dir_f/pparam_f/param1.txt"
	parser.parse_file(file)

	f = parser.params

	print()