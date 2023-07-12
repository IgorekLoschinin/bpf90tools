#!/usr/bin/venv python
# coding: utf-8

from pathlib import Path

from . import PARAM_FILE, RENUMF90
from .utils import run_app, CheckMixin


class Renumf90(CheckMixin):
	""" Renumbering and quality control be done by RENUMF90, which
	is also driven by a parameter file. """

	def __init__(self) -> None:
		self._par_file = None  # File name
		self._config = None  # Absolute path for param file

	def renum(self, app: str | Path) -> bool:
		""" RENUM is a renumbering program to create input (data, pedigree,
		and parameter) files for BLUPF90 programs and provide basic statistics

		:param app: - Absolute or relative path to renumf90
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

		if app.stem != RENUMF90:
			raise Exception(f"The program being run is not {RENUMF90}.")

		if self._par_file is not None:
			self._config = app.parent / self._par_file

		else:
			self._config = app.parent / PARAM_FILE

		if not self.is_file(self._config):
			raise FileExistsError(f"{self._par_file} file is not found.")

		if not run_app(app, self._config):
			return False

		return True

	@property
	def par_file(self) -> str:
		return PARAM_FILE

	@par_file.setter
	def par_file(self, filename: str) -> None:
		self._par_file = filename
