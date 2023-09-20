#!/usr/bin/venv python
# coding: utf-8

__author__ = "Igor Loschinin (igor.loschinin@gmail.com)"

import sys
from pathlib import Path

from . import _DIR_UTILS, _DIR_FILES
from .. import Renumf90
from ..settings import RENUMF90
from bpf90tools.utils import transform

import pytest
import shutil


@pytest.fixture
def make_space_preparation(tmp_path) -> Path:
	_dir_renum = tmp_path / "renum_dir"
	_dir_renum.mkdir(parents=True)

	_app = _DIR_UTILS / transform(RENUMF90)
	shutil.copy2(_app, _dir_renum)

	if sys.platform == "win32":
		shutil.copy2(_DIR_UTILS / "libiomp5md.dll", _dir_renum)

	for item in _DIR_FILES.glob("./*"):
		shutil.copy2(
			item, _dir_renum
		)

	return _dir_renum


class TestRenumf90(object):

	@pytest.mark.parametrize(
		"kwargs", [{"app": "renumf90", "fn_par": "param.txt"}]
	)
	def test_renum_successful(
			self, kwargs: dict, make_space_preparation: Path
	) -> None:
		_renum = Renumf90(**kwargs, work_dir=make_space_preparation)

		assert _renum.run()

