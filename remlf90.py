#!/usr/bin/venv python
# coding: utf-8

from pathlib import Path

from .parsers import PReml, Variance
from .utils import run_app, CheckMixin
from . import REMLF90, RENF90_PAR, REMLF90_LOG


class Remlf90(CheckMixin):
	""" Restricted Maximum Likelihood (REML) approach for estimating covariance
	matrices in linear stochastic models """

	def __init__(self) -> None:
		self.__parser = PReml()

	def reml(self, app: str | Path) -> bool:
		""" Calculate variance the method reml

		:param app: - Absolute or relative path to remlf90
		:return: - Returns true if the program started and ran without errors
			else false
		:raise: - Exceptions when files do not exist
		"""

		if isinstance(app, str):
			app = Path(app)

		if not app.is_absolute():
			app = app.absolute()

		if not self.is_file(app):
			raise FileExistsError(
				"There is no parameter file in the folder in which "
				"the application being launched is located."
			)

		if app.stem != REMLF90:
			raise Exception(f"The program being run is not {REMLF90}.")

		_par_file = app.parent / RENF90_PAR
		if not self.is_file(_par_file):
			raise FileExistsError(f"{_par_file} file is not found.")

		if not run_app(app, _par_file):
			return False

		_file_log = app.parent / REMLF90_LOG
		if not self.is_file(_file_log):
			raise FileExistsError(f"{_file_log} file is not found.")

		try:
			self.__parser.parse_file(_file_log)
		except:
			return False

		return True

	@property
	def variance(self) -> Variance | None:
		return self.__parser.values
