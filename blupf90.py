#!/usr/bin/venv python
# coding: utf-8

from pathlib import Path

from .parsers import PSolution, PPed
from .utils import run_app, CheckMixin
from . import BLUPF90, RENF90_PAR

import pandas as pd


class Blupf90(CheckMixin):
	""" BLUP (Best Linear Unbiased Prediction - the best linear unbiased
	prediction) method for determining the genetic potential of animals """

	def __init__(self) -> None:
		self.__data =

	def run(self, app: str | Path) -> bool:
		"""

		:param app:
		:return:
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

		if app.stem != BLUPF90:
			raise Exception(f"The program being run is not {BLUPF90}.")

		_par_file = app.parent / RENF90_PAR
		if not self.is_file(_par_file):
			raise FileExistsError(f"{_par_file} file is not found. Run renumf90.")

		if not run_app(app, _par_file):
			return False

		_file_log = app.parent / AIREML_LOG
		if not self.is_file(_file_log):
			raise FileExistsError(f"{_file_log} file is not found.")

	@property
	def evaluation(self) -> pd.DataFrame:
		return self.__data
