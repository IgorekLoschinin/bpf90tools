#!/usr/bin/venv python
# coding: utf-8
from pathlib import Path
from ..utils import CheckMixin

import numpy as np
import pandas as pd


class PSolution(CheckMixin):
	""" Processing the file with results of the assessment """

	def __init__(self, varg: float = None) -> None:
		"""
		:param varg: - The genetic ability required to calculate the
			confidence of the estimate.
		"""
		self.__varg = varg
		self.__data_sol = None

	@property
	def data_sol(self) -> pd.DataFrame | None:
		""" The method return a data frame with the results. """
		return self.__data_sol

	def parse_file(self, file: str | Path) -> None:
		""" Handler for a file with the results of evaluations of breeding
		values

		:param file: - path to file solutions
		return: dataFrame table data
		"""

		if isinstance(file, str):
			file = Path(file)

		if not self.is_file(file):
			raise OSError(
				f"The file being transferred could not be processed."
				f" Check the file - {file.stem}"
			)
		try:
			self._load(file)

			self.__data_sol = self.__data_sol.loc[
				self.__data_sol.effect == self.__data_sol.effect.max()
				]

			self.__data_sol['effect'] = \
				self.__data_sol['effect'].astype(int)

			self.__data_sol[['solution', 's.e.']] = \
				self.__data_sol[['solution', 's.e.']].astype(float)

			self.__data_sol = \
				self.__data_sol.rename(columns={"solution": "EBV"})

			if self.__varg is not None:
				self.__data_sol["REL"] = \
					self.__data_sol['s.e.'].apply(
						lambda x: self.rel_from_sep(x, self.__varg)
					).astype(np.int16)

				self.__data_sol = self.__data_sol[
					["EBV", "REL", "level"]
				]

			else:
				self.__data_sol = self.__data_sol[
					["EBV", "s.e.", "level"]
				]

		except Exception as e:
			raise e

	def _load(self, file: Path) -> None:
		"""

		:param file:
		:return:
		"""

		with file.open(mode="r", encoding="utf-8") as file:
			data_sol = file.readlines()

			# Parsing the string containing the field names
			col_name = file[0].replace('/', ' ').strip().split()
			list_sol = [item.strip().split() for item in data_sol[1:]]

			self.__data_sol = pd.DataFrame(
				list_sol, columns=col_name
			).astype({'effect': 'inf8'})

	@staticmethod
	def rel_from_sep(se_data: float, var_gen: float) -> float:
		""" Derivation of the reliability of the estimate from its
		standard deviation.

		:param se_data: - standard deviation calculated by blupf90.
		:param var_gen: - genetic variance calculated by remlf90.
		return: The return reliability.
		"""
		h = (1 - (se_data ** 2) / var_gen) * 100

		if h < 0:
			return 0

		return np.floor(h)

	def merge_with_ped(self, data_ped: pd.DataFrame, on=None) -> pd.DataFrame:
		""" Method that will combine two data objects by key
		fields - solutions and renadd.
		"""

		merge_sol_and_ped = pd.merge(
			self.__data_sol,
			data_ped,
			left_on="level",
			right_on="NOMER" if on is None else on
		).drop(columns=["level", "NOMER"])

		return merge_sol_and_ped
