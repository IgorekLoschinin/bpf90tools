#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2025-2026 Igor Loschinin.
# Distributed under the lgplv3 software license, see the accompanying
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.

__author__ = "Igor Loschinin (igor.loschinin@gmail.com)"

import shutil
import sys
from pathlib import Path

import pytest

from bpf90tools.src.bpf90tools import Renumf90
from bpf90tools.src.bpf90tools._utils import transform
from bpf90tools.src.bpf90tools.tools.settings import (
	RENUMF90,
	PARAM_FILE
)
from . import (
	_DIR_UTILS,
	_DIR_FILES
)

_DIR_RENUM = _DIR_FILES / "renum"


@pytest.fixture
def make_space_preparation(tmp_path) -> Path:
	_dir_renum = tmp_path / "renum_dir"
	_dir_renum.mkdir(parents=True)

	_app = _DIR_UTILS / transform(RENUMF90)
	shutil.copy2(_app, _dir_renum)

	if sys.platform == "win32":
		shutil.copy2(_DIR_UTILS / "libiomp5md.dll", _dir_renum)

	for item in _DIR_RENUM.glob("./*"):
		shutil.copy2(
			item, _dir_renum
		)

	return _dir_renum


@pytest.fixture
def obj_renum(request, make_space_preparation: Path) -> Renumf90:
	return Renumf90(
		app=transform(RENUMF90),
		work_dir=make_space_preparation if request.param is None else request.param,
		fn_par=PARAM_FILE
	)


class TestRenumf90(object):

	@pytest.mark.parametrize("obj_renum", [None], indirect=True)
	def test_renum_successful(
			self, obj_renum: Renumf90, make_space_preparation: Path, tmp_path
	) -> None:

		assert obj_renum.run()
		assert (make_space_preparation / "renf90.par").exists()

	@pytest.mark.parametrize("obj_renum", ["random/"], indirect=True)
	def test_renum_raise_of_work_dir(self, obj_renum: Renumf90) -> None:

		with pytest.raises(OSError, match="Directory does not exist."):
			obj_renum.run()

	@pytest.mark.parametrize(
		"kwargs", [{"app": transform(RENUMF90), "fn_par": "param1.txt"}]
	)
	def test_renum_raise_config(
			self, kwargs: dict, make_space_preparation: Path
	) -> None:
		_renum = Renumf90(**kwargs, work_dir=make_space_preparation)

		with pytest.raises(OSError):
			_renum.run()

		assert not (make_space_preparation / "renf90.par").exists()

	def test_renum_raise_app_exists_os(
			self, make_space_preparation: Path
	) -> None:
		_app = None

		match sys.platform:
			case "linux":
				_app = "renumf90.exe"

			case "win32":
				_app = "renumf90"

		_renum = Renumf90(
			app=_app,
			work_dir=make_space_preparation,
			fn_par=PARAM_FILE
		)

		with pytest.raises(
				ValueError, match=f"The program being run is not {_app}."
		):
			_renum.run()

	@pytest.mark.parametrize(
		"kwargs", [{"app": transform(RENUMF90), "fn_par": "param_fail.txt"}]
	)
	def test_renum_fail_run_app(
			self, kwargs: dict, make_space_preparation: Path
	) -> None:
		shutil.copy2(
			_DIR_FILES / "fail/param_fail.txt", make_space_preparation
		)

		_renum = Renumf90(**kwargs, work_dir=make_space_preparation)
		_renum.run()

		assert not (make_space_preparation / "renf90.par").exists()
