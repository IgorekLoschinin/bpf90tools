#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2025-2026 Igor Loschinin.
# Distributed under the lgplv3 software license, see the accompanying
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.

__author__ = "Igor Loschinin (igor.loschinin@gmail.com)"
__all__ = ("Remlf90", )

from pathlib import Path

from ._if90 import If90
from .settings import (
	REMLF90,
	RENF90_PAR,
	REMLF90_LOG
)
from .._utils import (
	run_app,
	CheckMixin,
	transform
)
from ..parsers import (
	PVar,
	Variance
)


class Remlf90(If90, CheckMixin):
	""" Restricted Maximum Likelihood (REML) approach for estimating covariance
	matrices in linear stochastic models """

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

		self.__parser = PVar()

	def run(self) -> bool:
		""" Calculate variance the method reml

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

		# Define file param
		if self._par_file is not None:
			_config = self._work_dir / self._par_file

		else:
			_config = self._work_dir / RENF90_PAR

		if not self.is_file(_config):
			raise OSError("File is not found. The first run renum!")

		# Run app
		if self._app != transform(REMLF90):
			raise ValueError(f"The program being run is not {self._app}.")

		_app_file = self._work_dir / self._app
		if not run_app(_app_file, _config, dir_cwd=self._work_dir):
			return False

		# Getting variance
		_file_log = self._work_dir / REMLF90_LOG
		if not self.is_file(_file_log):
			raise OSError("remlf90.log file is not found.")

		if not self.__parser.parse_file(_file_log):
			return False

		return True

	@property
	def variance(self) -> Variance | None:
		return self.__parser.values
