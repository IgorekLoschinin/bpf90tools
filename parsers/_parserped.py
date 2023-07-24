#!/usr/bin/venv python
# coding: utf-8
from pathlib import Path
from . import IParser
from ..utils import CheckMixin

import pandas as pd


class PPed(IParser, CheckMixin):
	""" Pedigree file processing - renadd__.ped which is obtained as a result
	of processing by renumf90 program.
	Example file: renadd02.ped	"""

	def __init__(self) -> None:
		self.__data_ped = None
		self.__lst_ped = []

	@property
	def values(self) -> pd.DataFrame | None:
		return self.__data_ped

	def parse_file(self, pth_file: str | Path) -> None:
		""" The parsing data files pedigree.

		:param pth_file: The path to file renadd.ped - pedigree
		:return: - Throws an exception when an error occurs
		"""

		if isinstance(pth_file, str):
			pth_file = Path(pth_file)

		if not self.is_file(pth_file):
			raise OSError(
				f"The file being transferred could not be processed."
				f" Check the file - {pth_file.stem}"
			)

		try:
			self._read(pth_file)

			self.__data_ped = pd.DataFrame(
				self.__lst_ped, columns=["nomer", "ID"]
			)

		except FileNotFoundError as e1:
			raise e1
		except Exception as e2:
			raise e2

	def _read(self, file: Path) -> None:
		""" Reading a file

		:param file: - The path to the file
		"""
		with file.open(mode="r", encoding="utf-8") as file:
			self.__lst_ped = [
				[item.strip().split()[0], item.strip().split()[-1]]
				for item in file
			]
