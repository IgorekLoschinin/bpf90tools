#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2025-2026 Igor Loschinin.
# Distributed under the lgplv3 software license, see the accompanying
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.

__author__ = "Igor Loschinin (igor.loschinin@gmail.com)"
__all__ = ("Renumf90", )

from pathlib import Path

from ._if90 import If90
from .settings import (
	PARAM_FILE,
	RENUMF90
)
from .._utils import (
	run_app,
	CheckMixin,
	transform
)


class Renumf90(If90, CheckMixin):
	""" Renumbering and quality control be done by RENUMF90, which
	is also driven by a parameter file. """

	def __init__(
			self,
			*,
			app: str,
			work_dir: str | Path,
			fn_par: str | None = None
	) -> None:
		"""
		:param app: - The name of the program
		:param work_dir: - Directory where all programs and files are located
		:param fn_par: - The name of the parameter file with settings
		"""
		If90.__init__(self, app=app, work_dir=work_dir, fn_par=fn_par)

	def run(self) -> bool:
		""" RENUM is a renumbering program to create input (data, pedigree,
		and parameter) files for BLUPF90 programs and provide basic statistics

		:return: - Returns true if the program started and ran without errors
			else false
		:raise: - Exceptions when files do not exist
		"""

		if isinstance(self._work_dir, str):
			self._work_dir = Path(self._work_dir)

		if not self._work_dir.is_absolute():
			self._work_dir = self._work_dir.absolute()

		if not self.is_dir(self._work_dir):
			raise OSError("Directory does not exist.")

		if self._par_file is not None:
			_config = self._work_dir / self._par_file

		else:
			_config = self._work_dir / PARAM_FILE

		if not self.is_file(_config):
			raise OSError(f"{_config} file is not found.")

		if self._app != transform(RENUMF90):
			raise ValueError(f"The program being run is not {self._app}.")

		_app_file = self._work_dir / self._app
		if not run_app(_app_file, _config, dir_cwd=self._work_dir):
			return False

		return True
