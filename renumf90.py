#!/usr/bin/venv python
# coding: utf-8

import os

# from utils._utils import run_exe


class Renumf90(object):

	def __init__(self,
				 path_to_exe: str,
				 filename_cfg: str) -> None:
		"""

		:param path_to_exe:
		:param filename_cfg:
		"""

		self.path_to_file_exe = path_to_exe
		self.filename_config = filename_cfg

	def start(self) -> None:
		try:

			if not self.check_file_cfg():
				raise Exception(
					"Application renumf90.exe not found in currently dir."
				)

			if not self.check_file_exe():
				raise Exception(
					"There is no parameter file in the folder in which "
					"the application being launched is located."
				)

			run_exe(self.path_to_file_exe, self.filename_config)

		except Exception:
			pass

	def check_file_exe(self) -> bool:
		""" Check if the file exists in the directory
		and that it has the .exe extension """

		if os.path.isfile(self.path_to_file_exe) and \
			os.path.exists(self.path_to_file_exe):
			return True

		return False

	def check_file_cfg(self) -> bool:
		""" The method checks if the file exists in the directory
		where the application being launched is located. """

		path_to_file_config = os.path.join(
			os.path.dirname(self.path_to_file_exe), self.filename_config
		)

		if os.path.exists(path_to_file_config) and \
			os.path.isfile(path_to_file_config):

			return True

		return False






