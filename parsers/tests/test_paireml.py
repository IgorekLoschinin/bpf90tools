#!/usr/bin/venv python
# coding: utf-8
from pathlib import Path
from .. import PAIReml
from . import _DIR_FILES
from pytest import fixture

_TEST_FILES = Path(_DIR_FILES) / "aireml_log"


@fixture
def parser():
	return PAIReml()


def test_parse_aireml_log_1(parser) -> None:
	file = _TEST_FILES / "airemlf90_2.log"
