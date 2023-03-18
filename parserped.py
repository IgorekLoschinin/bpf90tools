##!/usr/bin/venv python
# coding: utf-8

import re
import os
from pathlib import Path

import pandas as pd


class PPed(object):
	""" Pedigree file processing - renadd.ped which is obtained as a result
	of processing by renumf90 program.
	Example file: renadd02.ped	"""

	__filename_ped = None
	__pattern_for_search = re.compile(r"(^renadd[0-9]*.ped\b)")

	def __init__(self) -> None:
		self.path_to_file_ped = None
		self.__data_ped = None

	def get_data_ped(self) -> pd.DataFrame | None:
		""" The method return a data frame with the pedigree. """
		return self.__data_ped

	def parse_renadd(self, pth_to_ped: str | Path) -> None:
		""" The parsing data files pedigree.

		:param pth_to_ped: The path to file renadd.ped - pedigree
		"""

		self.path_to_file_ped = pth_to_ped
		self.__class__.__filename_ped = os.path.basename(pth_to_ped)

		if not self._check_filename():
			raise OSError(
				f"The file being transferred could not be processed."
				f" Check the file - {self.__class__.__filename_ped}"
			)

		with open(pth_to_ped, 'r') as file:
			list_ped = [
				[item.strip().split()[0], item.strip().split()[-1]]
				for item in file.readlines()
			]

		self.__data_ped = \
			pd.DataFrame(list_ped, columns=['NOMER', 'UNIQ_KEY'])

	def get_filename(self) -> str:
		""" Return only file name. """
		return self.__class__.__filename_ped

	def _check_filename(self) -> bool:
		""" Method that checks the file name by pattern. """

		if not (os.path.isfile(self.path_to_file_ped) and
				os.path.exists(self.path_to_file_ped)):
			return True

		if self.__pattern_for_search.findall(self.get_filename()):
			return True

		return False
