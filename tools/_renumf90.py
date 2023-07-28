#!/usr/bin/venv python
# coding: utf-8

from pathlib import Path

from . import PARAM_FILE, RENUMF90, If90
from ..utils import run_app, CheckMixin, transform


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

		self._config = None  # Absolute path for param file

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

		if self._app != transform(RENUMF90):
			raise Exception(f"The program being run is not {self._app}.")

		if self._par_file is not None:
			self._config = self._work_dir / self._par_file

		else:
			self._config = self._work_dir / PARAM_FILE

		if not self.is_file(self._config):
			raise OSError(f"{self._config} file is not found.")

		_app_file = self._work_dir / self._app
		if not run_app(_app_file, self._config, dir_cwd=self._work_dir):
			return False

		return True
