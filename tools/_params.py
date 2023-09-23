#!/usr/bin/venv python
# coding: utf-8

from pathlib import Path


class Params(object):
	""" Creates a parameter file """

	def __init__(
			self,
			file_config: str | Path | None = None,
			type_model: str = "single"  # or mult
	) -> None:
		"""
		:param file_config: - The name or path to the file in which the
			program launch options will be written
		:param type_model: - Model type. Can be 'single' or 'mult'.
			Default single
		"""

		self._type_model = type_model

		if isinstance(file_config, str):
			file_config = Path(file_config)

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

		if self._file_param is None:
			return False

		match self._type_model:
			case 'single':
				if not self._single_model(obj_param):
					return False

			case 'mult':
				return False

			case _:
				return False

		return True

	def _single_model(self, param_data: dict) -> bool:
		""" Building a file with settings for a single-feature model

		:param param_data: - Dictionary with settings
		:return: Returns true if the settings file was created successfully
			and false if it failed
		"""

		try:
			list_param = []
			for key, value in param_data.items():
				for item_value in value:
					list_param.extend([key, item_value])

			with open(self._file_param, 'w') as file_param:
				file_param.writelines('#PARAMETER FILE\n')

				for param in list_param:
					if param in ['RESIDUAL_VARIANCE', '(CO)VARIANCES']:
						file_param.writelines(param + '\n\t')

					elif param.startswith("OPTION") or param.startswith("COMBINE"):
						file_param.writelines(param + ' ')

					else:
						file_param.writelines(param + '\n')

		except Exception as e:
			return False

		return True
