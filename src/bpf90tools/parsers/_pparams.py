#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2025-2026 Igor Loschinin.
# Distributed under the lgplv3 software license, see the accompanying
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.

__author__ = "Igor Loschinin (igor.loschinin@gmail.com)"
__all__ = ("PParams", )

from collections import defaultdict
from pathlib import Path

from . import IParser
from ._keywords import Keywords
from .._utils import CheckMixin


class PParams(IParser, Keywords, CheckMixin):
	""" This is a class that processes a parameter file which is a
	configuration file for calculating blupf90.
	"""

	def __init__(self) -> None:
		self.__data_param = defaultdict(list)

	@property
	def params(self) -> dict[str, list]:
		""" Method that returns data - a dictionary of keywords and their
		values.
		"""
		return self.__data_param

	def parse_file(self, pth_file: str | Path) -> bool:
		""" Parsing the param.txt file.

		:param pth_file: The path to the file param.txt.
		:return: Throws an exception when an error occurs.
		"""

		if isinstance(pth_file, str):
			pth_file = Path(pth_file)

		if not self.is_file(pth_file):
			raise OSError("File param.txt not found!")

		try:
			lines = self._read(pth_file)

			key_word_par = ""
			for line in lines:
				if line.strip().startswith('#'):
					continue

				if line.strip().split(" ", 1)[0] in self.complex_par:
					opt, value = line.strip().split(" ", 1)
					self.__data_param[opt].append(value)

				else:
					if line.strip() in self.single_par:
						if line.strip() in self.__data_param.keys():
							pass
						else:
							key_word_par = line.strip()
					else:
						self.__data_param[key_word_par].append(line.strip())

		except Exception as exp:
			raise exp

		return True

	def _read(self, pth_file: str | Path) -> None | list:
		""" Reading a file.

		:param pth_file: The path to the file.
		:return: Return the list line.
		"""

		with pth_file.open(mode='r', encoding='utf-8') as file:
			return file.readlines()
