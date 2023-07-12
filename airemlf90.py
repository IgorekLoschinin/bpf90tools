#!/usr/bin/venv python
# coding: utf-8

from pathlib import Path

from .parsers import PAIReml, Variance
from .utils import run_app, CheckMixin
from . import AIREMlF90, RENF90_PAR, AIREML_LOG


class AIremlf90(CheckMixin):
	""" A modification of REMLF90 with computing by the Average-Information
	Algorithm

	For most problems, it converges in far
	fewer rounds than EM REML as implemented in REMLF90. While typically REMLF90
	takes 50-300 rounds to converge, AIREMLF90 converges in 5-15 rounds and to a
	higher accuracy. For selected problems, AI REML fails to converge when the
	covariance matrix is close to non-positive definite.
	"""

	def __init__(self) -> None:
		self.__parser = PAIReml()

	def aireml(self, app: str | Path) -> bool:
		""" Calculate variance the method aireml

		:param app: - Absolute or relative path to airemlf90
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

		if app.stem != AIREMlF90:
			raise Exception(f"The program being run is not {AIREMlF90}.")

		_par_file = app.parent / RENF90_PAR
		if not self.is_file(_par_file):
			raise FileExistsError(f"{_par_file} file is not found.")

		if not run_app(app, _par_file):
			return False

		_file_log = app.parent / AIREML_LOG
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
