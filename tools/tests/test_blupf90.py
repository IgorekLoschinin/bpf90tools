#!/usr/bin/venv python
# coding: utf-8

__author__ = "Igor Loschinin (igor.loschinin@gmail.com)"

import sys
import pytest
import shutil

from pathlib import Path

from . import _DIR_UTILS, _DIR_FILES
from .. import Blupf90
from ..settings import BLUPF90, RENF90_PAR
from bpf90tools.utils import transform

_DIR_BLUP = _DIR_FILES / "common"


@pytest.fixture
def make_space_preparation(tmp_path) -> Path:
	_dir_blup = tmp_path / "blup_dir"
	_dir_blup.mkdir(parents=True)

	_app = _DIR_UTILS / transform(BLUPF90)
	shutil.copy2(_app, _dir_blup)

	if sys.platform == "win32":
		shutil.copy2(_DIR_UTILS / "libiomp5md.dll", _dir_blup)

	for item in _DIR_BLUP.glob("./*"):
		shutil.copy2(item, _dir_blup)

	return _dir_blup


@pytest.fixture
def obj_blup(request, make_space_preparation: Path) -> Blupf90:
	return Blupf90(
		app=transform(BLUPF90),
		work_dir=make_space_preparation if request.param is None else request.param
	)


class TestBlupf90(object):

	@pytest.mark.parametrize("obj_blup", [None], indirect=True)
	def test_blup_successful(
			self, obj_blup: Blupf90, make_space_preparation: Path, tmp_path
	) -> None:
		assert obj_blup.run()
		assert (make_space_preparation / "solutions").exists()
		assert obj_blup.evaluation is not None
		assert not obj_blup.evaluation.empty

	@pytest.mark.parametrize("obj_blup", ["random/"], indirect=True)
	def test_blup_raise_of_work_dir(self, obj_blup: Blupf90) -> None:

		with pytest.raises(OSError, match="Directory does not exist."):
			obj_blup.run()

	@pytest.mark.parametrize(
		"kwargs", [{"app": transform(BLUPF90), "fn_par": "renf90.par1"}]
	)
	def test_blup_raise_config(
			self, kwargs: dict, make_space_preparation: Path
	) -> None:
		_blup = Blupf90(**kwargs, work_dir=make_space_preparation)

		with pytest.raises(
				OSError,
				match=f"{RENF90_PAR} file is not found. Run renumf90."
		):
			_blup.run()

		assert not (make_space_preparation / "solutions").exists()
		assert _blup.evaluation is None

	def test_blup_raise_app_os(self, make_space_preparation: Path) -> None:
		_app = None

		match sys.platform:
			case "linux":
				_app = "blupf90.exe"

			case "win32":
				_app = "blupf90"

		_blup = Blupf90(
			app=_app,
			work_dir=make_space_preparation,
			fn_par="renf90.par"
		)

		with pytest.raises(
				ValueError, match=f"The program being run is not {_app}."
		):
			_blup.run()

	@pytest.mark.parametrize(
		"kwargs", [{"app": transform(BLUPF90), "fn_par": "renf90_fail.par"}]
	)
	def test_blup_fail_run_app_exists_solutions(
			self, kwargs: dict, make_space_preparation: Path
	) -> None:
		shutil.copy2(
			_DIR_FILES / "fail/renf90_fail.par", make_space_preparation
		)

		_blup = Blupf90(**kwargs, work_dir=make_space_preparation)
		with pytest.raises(OSError, match="solutions file is not found."):
			_blup.run()

		assert not (make_space_preparation / "solutions").exists()
		assert _blup.evaluation is None
