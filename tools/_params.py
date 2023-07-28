#!/usr/bin/venv python
# coding: utf-8

from pathlib import Path


class Params(object):
	""" Creates a parameter file """

	def __init__(
			self,
			file_config: str | Path | None = None,
			type_model: str = "single"  # or multi
	) -> None:
		"""
		:param file_config: - The name or path to the file in which the
			program launch options will be written
		:param type_model: - Model type
		"""

		self.type_model = type_model
		self._file_param = file_config

	def create(self, obj_param: dict) -> bool:
		""" Method that forms the structure of the config and saves it
		to a file

		:param obj_param: An object of the dictionary type that stores the
			structure of the required parameters and from the value for the
			config.

		:return: An object of the dictionary type that stores the structure
			of the required parameters and from the value for the config.
		"""

		if not obj_param:
			return False

		list_param = []
		for key, value in obj_param.items():
			for item_value in value:
				list_param.extend([key, item_value])

		with open(self._file_param, 'w') as file_param:
			file_param.writelines('#PARAMETER FILE\n')

			for param in list_param:
				if param in ['RESIDUAL_VARIANCE', '(CO)VARIANCES']:
					file_param.writelines(param + '\n\t')

				elif param == 'OPTION':
					file_param.writelines(param + ' ')

				else:
					file_param.writelines(param + '\n')

		return True
