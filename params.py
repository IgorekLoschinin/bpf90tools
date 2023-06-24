#!/usr/bin/venv python
# coding: utf-8
from pathlib import Path


class Params(object):

	def __init__(
			self,
			file_config: str | Path | None = None,
			type_model: str = "single"
	) -> None:

		self.type_model = type_model
		self._file_param = file_config

	def create_config(self, obj_param: dict) -> bool:
		""" Method that forms the structure of the config and saves it
		to a file.

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
			if isinstance(value, list):

				for item_value in value:
					list_param.extend([key, item_value])

			else:
				list_param.extend([key, value])

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

	# setter
	def file_config(self, file: Path) -> None:
		"""  """
		self._file_param = file

	@staticmethod
	def update_config(def_param, param):
		copy_param = def_param.copy()
		copy_param.update(param)

		return copy_param

	@staticmethod
	def upgrade_config(def_param, param):
		pass

	def to_txt(self):
		pass

	def to_json(self):
		pass
