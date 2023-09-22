#!/usr/bin/venv python
# coding: utf-8

__author__ = "Igor Loschinin (igor.loschinin@gmail.com)"

from pathlib import Path

from ._if90 import If90
from ..parsers import PVar, Variance
from ..utils import run_app, CheckMixin, transform
from .settings import REMLF90, RENF90_PAR, REMLF90_LOG


class Remlf90(If90, CheckMixin):
	""" Restricted Maximum Likelihood (REML) approach for estimating covariance
	matrices in linear stochastic models """

	def __init__(
			self,
			*,
			app: str,
			work_dir: str | Path,
	) -> None:
		"""
		:param app: - The name of the program
		:param work_dir: - Directory where all programs and files are located
		"""
		If90.__init__(self, app=app, work_dir=work_dir)

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

		if self._app != transform(REMLF90):
			raise Exception(f"The program being run is not {self._app}.")

		_par_file = self._work_dir / RENF90_PAR
		if not self.is_file(_par_file):
			raise FileExistsError(f"{RENF90_PAR} file is not found.")

		_app_file = self._work_dir / self._app
		if not run_app(_app_file, _par_file, dir_cwd=self._work_dir):
			return False

		_file_log = self._work_dir / REMLF90_LOG
		if not self.is_file(_file_log):
			raise OSError(f"{_file_log} file is not found.")

		if not self.__parser.parse_file(_file_log):
			return False

		return True

	@property
	def variance(self) -> Variance | None:
		return self.__parser.values
