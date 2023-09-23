#!/usr/bin/venv python
# coding: utf-8

__author__ = "Igor Loschinin (igor.loschinin@gmail.com)"

import sys
import pytest
import shutil

from pathlib import Path

from . import _DIR_UTILS, _DIR_FILES
from .. import Remlf90
from ..settings import REMLF90, RENF90_PAR
from bpf90tools.utils import transform

_DIR_REML = _DIR_FILES / "common"


@pytest.fixture
def make_space_preparation(tmp_path) -> Path:
	_dir_reml = tmp_path / "reml_dir"
	_dir_reml.mkdir(parents=True)

	_app = _DIR_UTILS / transform(REMLF90)
	shutil.copy2(_app, _dir_reml)

	if sys.platform == "win32":
		shutil.copy2(_DIR_UTILS / "libiomp5md.dll", _dir_reml)

	for item in _DIR_REML.glob("./*"):
		shutil.copy2(item, _dir_reml)

	return _dir_reml


@pytest.fixture
def obj_reml(request, make_space_preparation: Path) -> Remlf90:
	return Remlf90(
		app=transform(REMLF90),
		work_dir=make_space_preparation if request.param is None else request.param,
		fn_par=RENF90_PAR
	)


class TestRemlf90(object):

	@pytest.mark.parametrize("obj_reml", [None], indirect=True)
	def test_reml_successful(
			self, obj_reml: Remlf90, make_space_preparation: Path, tmp_path
	) -> None:

		assert obj_reml.run()
		assert (make_space_preparation / "remlf90.log").exists()
		assert obj_reml.variance is not None

	@pytest.mark.parametrize("obj_reml", ["random/"], indirect=True)
	def test_reml_raise_of_work_dir(self, obj_reml: Remlf90) -> None:

		with pytest.raises(OSError, match="Directory does not exist."):
			obj_reml.run()

	@pytest.mark.parametrize(
		"kwargs", [{"app": transform(REMLF90), "fn_par": "renf90.par1"}]
	)
	def test_reml_raise_config(
			self, kwargs: dict, make_space_preparation: Path
	) -> None:
		_aireml = Remlf90(**kwargs, work_dir=make_space_preparation)

		with pytest.raises(
				OSError, match="File is not found. The first run renum!"
		):
			_aireml.run()

		assert all(list(map(
			lambda x: True if x is None else False,
			_aireml.variance.dict().values()
		)))

	def test_reml_raise_app_exists_os(
			self, make_space_preparation: Path
	) -> None:
		_app = None

		match sys.platform:
			case "linux":
				_app = "remlf90.exe"

			case "win32":
				_app = "remlf90"

		_reml = Remlf90(
			app=_app,
			work_dir=make_space_preparation,
			fn_par="renf90.par"
		)

		with pytest.raises(
				ValueError, match=f"The program being run is not {_app}."
		):
			_reml.run()

	@pytest.mark.parametrize(
		"kwargs", [{"app": transform(REMLF90), "fn_par": "renf90_fail.par"}]
	)
	def test_reml_fail_run_app_empty_log(
			self, kwargs: dict, make_space_preparation: Path
	) -> None:
		shutil.copy2(
			_DIR_FILES / "fail/renf90_fail.par", make_space_preparation
		)

		_reml = Remlf90(**kwargs, work_dir=make_space_preparation)
		_reml.run()

		assert all(list(map(
			lambda x: True if x is None else False,
			_reml.variance.dict().values()
		)))
