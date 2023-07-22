#!/usr/bin/venv python
# coding: utf-8
from pathlib import Path
from . import IParser
from ..utils import CheckMixin


import numpy as np
import pandas as pd


class PSolution(IParser, CheckMixin):
	""" Processing the file with results of the assessment """

	def __init__(self, varg: float = None) -> None:
		"""
		:param varg: - The genetic ability required to calculate the
			confidence of the estimate
		"""
		self.__varg = varg
		self.__data_sol = None

	@property
	def solutions(self) -> pd.DataFrame | None:
		return self.__data_sol

	def parse_file(self, file: str | Path) -> None:
		""" Handler for a file with the results of evaluations of breeding
		values

		:param file: - Path to file solutions
		:return: - DataFrame table data
		"""

		if isinstance(file, str):
			file = Path(file)

		if not self.is_file(file):
			raise OSError(
				f"The file being transferred could not be processed."
				f" Check the file - {file.stem}"
			)

		try:
			self._read(file)

			self.__data_sol = self.__data_sol.loc[
				self.__data_sol.effect == self.__data_sol.effect.max()
			]

			self.__data_sol = \
				self.__data_sol.rename(columns={"solution": "EBV"})

			if self.__varg is not None:
				self.__data_sol["REL"] = self.__data_sol['SE'].apply(
					lambda x: self._rel_from_sep(x, self.__varg)
				).astype(np.int16)

				self.__data_sol = self.__data_sol[["EBV", "REL", "level"]]

			else:
				self.__data_sol = self.__data_sol[["EBV", "SE", "level"]]

		except Exception as e:
			raise e

	def _read(self, pth_file: Path) -> None:
		""" Reading a file

		:param pth_file: - The path to the file
		"""

		with pth_file.open(mode="r", encoding="utf-8") as file:

			# Parsing the string containing the field names
			col_name = file.readline().replace('/', ' ').strip().split()
			list_sol = [line.strip().split() for line in file]

			self.__data_sol = pd.DataFrame(list_sol, columns=col_name)

		self.__data_sol = self.__data_sol.\
			rename(columns={'s.e.': 'SE'}).\
			astype({'effect': 'int8', 'solution': 'float64', 'SE': 'float64'})

	@staticmethod
	def _rel_from_sep(se_data: float, var_gen: float) -> float:
		""" Derivation of the reliability of the estimate from its
		standard deviation.

		:param se_data: - Standard deviation calculated by blupf90
		:param var_gen: - Genetic variance calculated by remlf90
		:return: - The return reliability
		"""
		h = (1 - (se_data ** 2) / var_gen) * 100

		if h < 0:
			return 0

		return np.floor(h)
