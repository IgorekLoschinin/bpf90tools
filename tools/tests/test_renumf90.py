#!/usr/bin/venv python
# coding: utf-8

__author__ = "Igor Loschinin (igor.loschinin@gmail.com)"

from pathlib import Path

from . import _DIR_UTILS
from .. import Renumf90
from ..settings import RENUMF90
from bpf90tools.utils import transform

import pytest


@pytest.fixture
def make_space_preparation(tmp_path) -> Path:
	_dir_renum = tmp_path / "renum_dir"
	_dir_renum.mkdir()

	_file = _dir_renum / transform(RENUMF90)

	return _dir_renum


class TestRenumf90(object):

	@pytest.mark.parametrize(
		"kwargs",
		[
			{
				"app": "renumf90",
				"work_dir": Path("/home/igorek/Документы/DEVPERSONAL"
								 "/PROJECTS/ebvprojects/devTools/fortest"),
				"fn_par": "renum.animal.1.txt"
			}
		]
	)
	def test_renum_successful(self, kwargs: dict) -> None:
		_renum = Renumf90(**kwargs)
		_renum.run()

