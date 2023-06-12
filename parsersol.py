##!/usr/bin/venv python
# coding: utf-8
from pathlib import Path

import re
import os
import numpy as np
import pandas as pd


class PSolution(object):
	""" Processing the file with results of the assessment. """

	__filename_sol = None
	__pattern_for_search = re.compile(r"(^solutions\b$)")

	def __init__(self, effect: int = None, var_gen: float = None) -> None:
		"""
		:param effect: - This is the ordinal value of the fixed effect. In
							this case, we need an animal effect.
		:param var_gen: - the genetic ability required to calculate the
							confidence of the estimate.
		"""
		self.path_to_file_sol = None
		self.effect = str(effect)
		self.variance_gen = var_gen
		self.__solution_dataframe = None

	def get_sol_df(self) -> pd.DataFrame | None:
		""" The method return a data frame with the results. """

		return self.__solution_dataframe

	def parse_solutions(self, pth_to_sol: str | Path) -> None:
		""" The parsing files solutions.

		:param pth_to_sol: - path to file solutions
		return: dataFrame table data
		"""

		self.path_to_file_sol = pth_to_sol
		self.__class__.__filename_sol = os.path.basename(pth_to_sol)

		if not self._check_filename():
			raise OSError(
				f"The file being transferred could not be processed."
				f" Check the file - {self.__class__.__filename_sol}"
			)

		with open(pth_to_sol, 'r') as file:
			data_sol = file.readlines()

			# Parsing the string containing the field names
			col_name = data_sol[0].replace('/', ' ').strip().split()
			list_sol = [item.strip().split() for item in data_sol[1:]]

			self.__solution_dataframe = pd.DataFrame(
				list_sol, columns=col_name
			).astype({'effect': 'inf8'})

		self.__solution_dataframe = self.__solution_dataframe.loc[
			self.__solution_dataframe.effect == self.__solution_dataframe.effect.max()
		]

		self.__solution_dataframe['effect'] = \
			self.__solution_dataframe['effect'].astype(int)

		self.__solution_dataframe[['solution', 's.e.']] = \
			self.__solution_dataframe[['solution', 's.e.']].astype(float)

		self.__solution_dataframe = \
			self.__solution_dataframe.rename(columns={"solution": "EBV"})

		if self.variance_gen is not None:
			self.__solution_dataframe["REL"] = \
				self.__solution_dataframe['s.e.'].apply(
					lambda x: self.rel_from_sep(x, self.variance_gen)
				).astype(np.int16)

			self.__solution_dataframe = self.__solution_dataframe[
				["EBV", "REL", "level"]
			]

		else:
			self.__solution_dataframe = self.__solution_dataframe[
				["EBV", "s.e.", "level"]
			]

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
			self.__solution_dataframe,
			data_ped,
			left_on="level",
			right_on="NOMER" if on is None else on
		).drop(columns=["level", "NOMER"])

		return merge_sol_and_ped

	def get_filename(self) -> str:
		""" Return only file name. """
		return self.__class__.__filename_sol

	def _check_filename(self) -> bool:
		""" Method that checks the file name by pattern. """

		if not (os.path.isfile(self.path_to_file_sol) and
				os.path.exists(self.path_to_file_sol)):
			return True

		if self.__pattern_for_search.findall(self.get_filename()):
			return True

		return False
