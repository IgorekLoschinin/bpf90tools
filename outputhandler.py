#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
from utils.utils import FindAll


class OutputHandler(object):
	""" Обработка данных оценки племенной ценности полученной методом blup.
	То есть обработка выдохных данных после завершения работы программ семейста
	 blupf90 """

	def __init__(self):
		pass

	# todo : МЕТОД РАБОТАЕТ НЕ КОРРЕКТНО ИЗ_ЗА FIND_ALL
	@staticmethod
	def processing_output_data(dir_path: str, var_g: float) -> pd.DataFrame:
		""" Processing of the solutions and pedigree files that result from
		the processing of blupf90 data. The parameter file is parsed, which
		contains all the information about the input data - the index of the
		trait, gene variants and errors.
		:return:
		"""

		pattern_solution = r"^solutions\b$"
		pattern_renadd = r"^renadd[0-9]*.ped\b"
		dir_in_which_file_sol_and_ped = os.path.dirname(dir_path)

		if not (os.path.isdir(dir_in_which_file_sol_and_ped) and
				os.path.exists(dir_in_which_file_sol_and_ped)):
			raise OSError(
				f"The passed path '{dir_in_which_file_sol_and_ped}'"
				f" to search for files is not a directory or does not exist."
			)

		file_solution = FindAll(dir_in_which_file_sol_and_ped)
		file_solution.search_file(pattern=pattern_solution)

		file_renadd = FindAll(dir_in_which_file_sol_and_ped)
		file_renadd.search_file(pattern=pattern_renadd)

		if file_solution.is_empty() and file_renadd.is_empty():
			raise Exception(
				f"Solution and renadd files were not found in "
				f"the directory {dir_in_which_file_sol_and_ped}."
			)

		obj_sol = PSolution(3, var_gen=var_g)
		obj_sol.parse_solutions(file_solution.get_result_search()[0])

		obj_ped = PPed()
		obj_ped.parse_renadd(file_renadd.get_result_search()[0])

		results = obj_sol.merge_with_ped(obj_ped.get_data_ped())

		return results
