#!/usr/bin/venv python
# coding: utf-8
from pathlib import Path
from pytest import fixture
from deepdiff import DeepDiff

from .. import PParams
from . import _DIR_FILES


_TEST_FILES = Path(_DIR_FILES) / "pparam_f"


@fixture
def parser():
	return PParams()


def test_parse_aireml_log_1(parser) -> None:
	# file = _TEST_FILES / "param1.txt"

	parser.parse_file(file)

	f = parser.params

	print(f)