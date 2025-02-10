#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2025-2026 Igor Loschinin.
# Distributed under the lgplv3 software license, see the accompanying
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.

__author__ = "Igor Loschinin (igor.loschinin@gmail.com)"
__all__ = ("PSolution", )

from pathlib import Path

import numpy as np
import pandas as pd

from . import IParser
from .._utils import CheckMixin


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

	def parse_file(self, file: str | Path) -> bool:
		""" Handler for a file with the results of evaluations of breeding
		values

		:param file: - Path to file solutions
		:return: - Returns true if file parsing was successful, false if
			it failed
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

			if "s.e." in self.__data_sol.columns:
				self.__data_sol = self.__data_sol.\
					rename(columns={"s.e.": "SE", "solution": "EBV"}).\
					astype({'effect': 'int8', 'EBV': 'float64', 'SE': 'float64'}).\
					loc[self.__data_sol.effect == self.__data_sol.effect.max()]

				if self.__varg is not None:
					self.__data_sol["REL"] = self.__data_sol['SE'].apply(
						lambda x: self._rel_from_sep(x, self.__varg)
					).astype(np.int16)

					self.__data_sol = self.__data_sol[["EBV", "REL", "level"]]

				else:
					self.__data_sol = self.__data_sol[["EBV", "SE", "level"]]

			else:
				self.__data_sol = self.__data_sol. \
					rename(columns={"solution": "EBV"}). \
					astype({'effect': 'int8', 'EBV': 'float64'}). \
					loc[
						self.__data_sol.effect == self.__data_sol.effect.max(),
						["EBV", "level"]
					]

		except Exception as e:
			raise e

		return True

	def _read(self, pth_file: Path) -> None:
		""" Reading a file

		:param pth_file: - The path to the file
		"""

		with pth_file.open(mode="r", encoding="utf-8") as file:

			# Parsing the string containing the field names
			col_name = file.readline().replace('/', ' ').strip().split()
			list_sol = [line.strip().split() for line in file]

			self.__data_sol = pd.DataFrame(list_sol, columns=col_name)

	@staticmethod
	def _rel_from_sep(se_data: float, var_gen: float) -> float:
		""" Derivation of the reliability of the estimate from its
		standard deviation.

		:param se_data: - Standard deviation calculated by blupf90
		:param var_gen: - Genetic variance calculated by remlf90
		:return: - The return reliability
		"""
		rel = (1 - (se_data ** 2) / var_gen) * 100

		if rel < 0:
			return 0.0

		return np.floor(rel)

	@property
	def _varg(self) -> float | None:
		return self.__varg

	@_varg.setter
	def _varg(self, value: float) -> None:
		self.__varg = value
