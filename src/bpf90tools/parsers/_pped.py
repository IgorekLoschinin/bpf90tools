#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2025-2026 Igor Loschinin.
# Distributed under the lgplv3 software license, see the accompanying
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.

__author__ = "Igor Loschinin (igor.loschinin@gmail.com)"
__all__ = ("PPed", )

from pathlib import Path

import pandas as pd

from . import IParser
from ..utils import CheckMixin


class PPed(IParser, CheckMixin):
	""" Pedigree file processing - renadd__.ped which is obtained as a result
	of processing by renumf90 program.
	Example file: renadd02.ped
	"""

	def __init__(self) -> None:
		self.__data_ped = None
		self.__lst_ped = []

	@property
	def values(self) -> pd.DataFrame | None:
		""" Return of dataframe - ['nomer', 'ID']. """
		return self.__data_ped

	def parse_file(self, pth_file: str | Path) -> bool:
		""" The parsing data files pedigree.

		:param pth_file: The path to file renadd.ped - pedigree.
		:return: Throws an exception when an error occurs.
		"""

		if isinstance(pth_file, str):
			pth_file = Path(pth_file)

		if not pth_file.is_absolute():
			pth_file = pth_file.absolute()

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

		except Exception as e:
			raise e

		return True

	def _read(self, file: Path) -> None:
		""" Reading a file.

		:param file: The path to the file.
		"""
		with file.open(mode="r", encoding="utf-8") as obj_file:
			self.__lst_ped = [
				[item.strip().split()[0], item.strip().split()[-1]]
				for item in obj_file
			]
