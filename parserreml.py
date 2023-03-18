##!/usr/bin/venv python
# coding: utf-8##!/usr/bin/venv python
# coding: utf-8

import re
import os
import json as js


class PReml:
	""" Processing the file method reml in which the variance information
	is stored """

	__filename_reml = None
	__pattern_for_search = re.compile(r"(^remlf[0-9]{2}.log\b)")

	def __init__(self) -> None:
		self.path_to_file_reml = None
		self.__variance: dict = {}

	def get_var(self) -> dict:
		""" The method return a dict with variances. """
		return self.__variance

	def get_filename(self) -> str:
		return self.__class__.__filename_reml

	def parse_file_variance(self, path_to_file: str) -> None:
		""" Parsing the log file of the reml.exe(sh) program. """

		self.path_to_file_reml = path_to_file
		self.__class__.__filename_reml = os.path.basename(path_to_file)

		if self.check_file_remlf90():
			with open(path_to_file, 'r') as file_var:
				list_str_from_remlf90 = list(map(
					lambda x: x.strip(), file_var.readlines()
				))

				for item in list_str_from_remlf90:
					index = list_str_from_remlf90.index(item) + 1

					if 'Genetic variance(s)' in item:
						self.__variance['genetic_variance'] = \
							list_str_from_remlf90[index]

					elif 'Residual variance(s)' in item:
						self.__variance['residual_variance'] = \
							list_str_from_remlf90[index]

				self.__variance['heritability'] = round(
					float(self.__variance['genetic_variance']) / (
							float(self.__variance['genetic_variance']) +
							float(self.__variance['residual_variance'])
					), 3)
		else:
			raise OSError("File remlf.log not found!")

	def check_file_remlf90(self) -> bool:
		""" The method checks if the file being passed is reml.log """

		if os.path.isfile(self.path_to_file_reml) and \
				os.path.exists(self.path_to_file_reml):
			return True

		if self.__pattern_for_search.findall(self.get_filename()):
			return True

		return False

	def to_json(self, path_to_file: str) -> None:
		""" Save to file Json.
		:param path_to_file: - Path to file for saving.
		"""
		if os.path.isfile(path_to_file):
			with open(f"{path_to_file}", "w") as file:
				js.dump(self.__variance, file, indent=4)
		else:
			raise OSError(f"The path - {path_to_file}, passed is not a file!")
