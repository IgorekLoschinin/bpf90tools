#!/usr/bin/venv python
# coding: utf-8
from pathlib import Path
from pytest import fixture

from .. import PVar
from . import _DIR_FILES


_TEST_FILES = Path(_DIR_FILES) / "aireml_log"


@fixture
def parser():
	return PVar()


def test_parse_aireml_log_1(parser) -> None:
	file = _TEST_FILES / "airemlf90_2.log"
