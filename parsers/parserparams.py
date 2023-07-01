#!/usr/bin/venv python
# coding: utf-8
from pathlib import Path
from . import IParser
from .keyword import Keyword
from ..utils import CheckMixin

from collections import defaultdict


class PParams(IParser, Keyword, CheckMixin):
	""" This is a class that processes a parameter file which is a
	configuration file for calculating blupf90. """

	def __init__(self) -> None:
		self.__data_param = defaultdict(list)

	@property
	def params(self) -> dict:
		""" Method that returns data - a dictionary of keywords and their
		values. """
		return self.__data_param

	def parse_file(self, pth_file: str) -> None:
		""" Parsing the param.txt file

		:param pth_file:
		:return:
		"""

		if isinstance(pth_file, str):
			pth_file = Path(pth_file)

		try:
			if not self.is_file(pth_file):
				raise OSError("File param.txt not found!")

			lines = self._read(pth_file)

			key_word_par = ""
			for line in lines:
				if line.strip().startswith('#'):
					continue

				if line.startswith("OPTION") or line.startswith("COMBINE"):
					self.__data_param[key_word_par].append(
						self.split_single_line_property(line.strip())
					)

				else:
					if line.strip() in self.__class__.all_join_keyword:
						if line.strip() in self.__data_param.keys():
							pass
						else:
							key_word_par = line.strip()
					else:
						self.__data_param[key_word_par].append(line.strip())

		except Exception as exp:
			raise exp

	def _read(self, pth_file: str | Path) -> None | list:
		""" Method that processes a text file with parameters to form a
		dictionary

		:param pth_file:
		:return:
		"""

		with pth_file.open(mode='r', encoding='utf-8') as file:
			return file.readlines()

	@staticmethod
	def split_single_line_property(prop: str) -> dict:
		"""  """

		if prop.startswith("OPTION"):
			comb_prop, value = prop.split(" ", 1)

			return {comb_prop: [value]}

		if prop.startswith("COMBINE"):
			pass
