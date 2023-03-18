##!/usr/bin/venv python
# coding: utf-8

import os


class IRunApp(object):

	def __init__(self):
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

	def run_exe(exe_file: str, param_file: str) -> int:
		""" Запуск программ с расширением .exe """

		process = subprocess.Popen(args=[exe_file],
								   stdin=subprocess.PIPE,
								   stdout=subprocess.PIPE)
		cmd_out, _ = process.communicate(f'{param_file}\n'.encode())

		with open(f'{exe_file.split(".")[0]}_console_output.log',
				  'w') as save_file:
			save_file.write(cmd_out.decode())

		code = process.wait()

		return code

	def move_files(self):
		pass

	def to_txt(self):
		pass

	def to_dir(self):
		pass