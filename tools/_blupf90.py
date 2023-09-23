#!/usr/bin/venv python
# coding: utf-8

__author__ = "Igor Loschinin (igor.loschinin@gmail.com)"

import pandas as pd

from pathlib import Path

from ._if90 import If90
from .settings import (
	BLUPF90,
	RENF90_PAR,
	SOLUTIONS,
	RENADD
)
from ..parsers import PSolution, PPed
from ..utils import run_app, CheckMixin, transform


class Blupf90(If90, CheckMixin):
	""" BLUP (Best Linear Unbiased Prediction - the best linear unbiased
	prediction) method for determining the genetic potential of animals """

	def __init__(
			self,
			*,
			app: str,
			work_dir: str | Path,
			vara: str | None = None,
			fn_par: str | None = None
	) -> None:
		"""
		:param app: - The name of the program
		:param work_dir: - Directory where all programs and files are located
		:param vara: - Genetic variant. None by default. Used to translate
			s.e. to reliability
		:param fn_par: - The name of the parameter file with settings
		"""
		If90.__init__(self, app=app, work_dir=work_dir, fn_par=fn_par)

		self.__vara = vara
		self.__data = None

	@property
	def evaluation(self) -> pd.DataFrame | None:
		return self.__data

	def run(self) -> bool:
		""" Starts breeding value calculation

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

		if not self.__blup():
			return False

		if not self.__processing_result(self._work_dir):
			return False

		return True

	def __blup(self) -> bool:
		""" Starting the breeding value calculation """

		# Define file param
		if self._par_file is not None:
			_config = self._work_dir / self._par_file

		else:
			_config = self._work_dir / RENF90_PAR

		if not self.is_file(_config):
			raise OSError(f"{RENF90_PAR} file is not found. Run renumf90.")

		# Run app
		if self._app != transform(BLUPF90):
			raise ValueError(f"The program being run is not {self._app}.")

		_app_file = self._work_dir / self._app
		if not run_app(_app_file, _config, dir_cwd=self._work_dir):
			return False

		return True

	def __processing_result(self, work_dir: Path) -> bool:
		""" Processing data

		:param work_dir: - Directory where all programs and files are located
		:return: Return true if processing data successful else False
		"""

		f_solutions = work_dir / SOLUTIONS
		if not self.is_file(f_solutions):
			raise OSError(f"{SOLUTIONS} file is not found.")

		f_renadd = self.__search_ped(work_dir)
		data_ped = self.__handler_ped(f_renadd)
		data_sol = self.__handler_sol(f_solutions)

		self.__data = data_ped.merge(
			data_sol,
			left_on="nomer",
			right_on="level"
		).drop(columns=["level", "nomer"])

		return True

	def __handler_sol(self, pth_file: Path) -> pd.DataFrame:
		""" Results file handler with breeding value and estimation accuracy

		:param pth_file: - Path to file solutions
		:return: - Return dataframe with data - ebv, se or rel
		"""

		sol = PSolution(varg=self.__vara)
		sol.parse_file(pth_file)

		return sol.solutions

	@staticmethod
	def __handler_ped(pth_file: Path) -> pd.DataFrame:
		""" Ped file handler

		:param pth_file: - Path to file ped
		:return: - Return dataframe with data - [nomer, id]
		"""

		ped = PPed()
		ped.parse_file(pth_file)

		return ped.values

	@staticmethod
	def __search_ped(w_d: Path) -> Path | None:
		""" Search for a pedigree file

		:param w_d: - Search directory
		:return: - Returns either the file if found, or non if not found
		"""

		lst_files = []
		for item_f in w_d.glob("*"):
			lst_files.extend(RENADD.findall(item_f.name))

		if not lst_files or len(lst_files) > 1:
			return None

		return w_d / lst_files[0]
