##!/usr/bin/venv python
# coding: utf-8
from pathlib import Path
from typing import List, Tuple
from collections import defaultdict
from .keywordparam import Keyword


class ParseParams(Keyword):
	""" This is a class that processes a parameter file which is a
	configuration file for calculating blupf90. """

	def __init__(self) -> None:
		self.__data_param = defaultdict(list)

	def read(self, file_params: Path) -> None:
		""" Method that processes a text file with parameters to form a
		dictionary. """

		with open(file_params, 'r') as file:
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

	def write(self) -> bool:
		pass

	def get_data_params(self) -> dict:
		""" Method that returns data - a dictionary of keywords and their
		values. """
		return self.__data_param

	def from_txt(self) -> list:
		pass

	def from_json(self) -> dict:
		pass

	def to_json(self) -> None:
		pass

	def to_txt(self) -> None:
		pass

	def to_list(self) -> List[Tuple]:
		""" файл параметров разбитый на список картежей """
		pass
