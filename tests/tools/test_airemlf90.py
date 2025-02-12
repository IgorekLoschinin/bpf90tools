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

from bpf90tools.src.bpf90tools import AIremlf90
from bpf90tools.src.bpf90tools.utils import transform
from bpf90tools.src.bpf90tools.tools.settings import (
	AIREMLF90,
	RENF90_PAR
)
from . import (
	_DIR_UTILS,
	_DIR_FILES
)

_DIR_AIREML = _DIR_FILES / "common"


@pytest.fixture
def make_space_preparation(tmp_path) -> Path:
	_dir_aireml = tmp_path / "aireml_dir"
	_dir_aireml.mkdir(parents=True)

	_app = _DIR_UTILS / transform(AIREMLF90)
	shutil.copy2(_app, _dir_aireml)

	if sys.platform == "win32":
		shutil.copy2(_DIR_UTILS / "libiomp5md.dll", _dir_aireml)

	for item in _DIR_AIREML.glob("./*"):
		shutil.copy2(item, _dir_aireml)

	return _dir_aireml


@pytest.fixture
def obj_aireml(request, make_space_preparation: Path) -> AIremlf90:
	return AIremlf90(
		app=transform(AIREMLF90),
		work_dir=make_space_preparation if request.param is None else request.param,
		fn_par=RENF90_PAR
	)


class TestAIRemlf90(object):

	@pytest.mark.parametrize("obj_aireml", [None], indirect=True)
	def test_aireml_successful(
			self, obj_aireml: AIremlf90, make_space_preparation: Path, tmp_path
	) -> None:

		_log_file = make_space_preparation / "airemlf90.log"

		assert obj_aireml.run()
		assert _log_file.is_file() and _log_file.exists()
		assert obj_aireml.variance is not None

	@pytest.mark.parametrize("obj_aireml", ["random/"], indirect=True)
	def test_aireml_raise_of_work_dir(self, obj_aireml: AIremlf90) -> None:

		with pytest.raises(OSError, match="Directory does not exist."):
			obj_aireml.run()

	@pytest.mark.parametrize(
		"kwargs", [{"app": transform(AIREMLF90), "fn_par": "renf90.par1"}]
	)
	def test_aireml_raise_config(
			self, kwargs: dict, make_space_preparation: Path
	) -> None:
		_aireml = AIremlf90(**kwargs, work_dir=make_space_preparation)

		with pytest.raises(
				OSError, match="File is not found. The first run renum!"
		):
			_aireml.run()

		assert all(list(map(
			lambda x: True if x is None else False,
			_aireml.variance.model_dump().values()
		)))

	def test_aireml_raise_app_exists_os(
			self, make_space_preparation: Path
	) -> None:
		_app = None

		match sys.platform:
			case "linux":
				_app = "airemlf90.exe"

			case "win32":
				_app = "airemlf90"

		_aireml = AIremlf90(
			app=_app,
			work_dir=make_space_preparation,
			fn_par="renf90.par"
		)

		with pytest.raises(
				ValueError, match=f"The program being run is not {_app}."
		):
			_aireml.run()

	@pytest.mark.parametrize(
		"kwargs", [{"app": transform(AIREMLF90), "fn_par": "renf90_fail.par"}]
	)
	def test_aireml_fail_run_app_exists_log(
			self, kwargs: dict, make_space_preparation: Path
	) -> None:
		shutil.copy2(
			_DIR_FILES / "fail/renf90_fail.par", make_space_preparation
		)

		_aireml = AIremlf90(**kwargs, work_dir=make_space_preparation)

		with pytest.raises(OSError, match="airemlf90.log file is not found."):
			_aireml.run()

		assert all(list(map(
			lambda x: True if x is None else False,
			_aireml.variance.model_dump().values()
		)))
