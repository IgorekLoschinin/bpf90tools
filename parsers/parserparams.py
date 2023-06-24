#!/usr/bin/venv python
# coding: utf-8
from pathlib import Path
from ..keyword import Keyword
from ..utils import CheckMixin
from collections import defaultdict


class ParseParams(Keyword, CheckMixin):
	""" This is a class that processes a parameter file which is a
	configuration file for calculating blupf90. """

	def __init__(self) -> None:
		self.__data_param = defaultdict(list)

	@property
	def params(self) -> dict:
		""" Method that returns data - a dictionary of keywords and their
		values. """
		return self.__data_param

	def _load(self, pth_file: str | Path) -> None:
		""" Method that processes a text file with parameters to form a
		dictionary. """

		if isinstance(pth_file, str):
			pth_file = Path(pth_file)

		with pth_file.open(mode='r', encoding='utf-8') as file:
			key_word_par = ""

			for str_par in file.readlines():
				if str_par.strip().startswith('#'):
					continue

				if self.is_single_line_properties(str_par.strip()):
					self.__data_param.update(
						self.split_single_line_property(str_par.strip())
					)

				else:
					if str_par.strip() in self.__class__.all_join_keyword:
						if str_par.strip() in self.__data_param.keys():
							pass
						else:
							key_word_par = str_par.strip()
					else:
						self.__data_param[key_word_par].append(str_par.strip())
