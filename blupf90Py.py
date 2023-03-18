##!/usr/bin/venv python
# coding: utf-8

import os
import shutil
import subprocess
import numpy as np
import pandas as pd


class parseFileBlup:
	pass





# -------------- Формирвоание файла параметров para --------------------------
class RunProcBlupf90:
	'''
	1) Соствление файла параметров
		1.1) Расчет предварительных варианс
	2) Запуск renumf90.exe на 1)
	3) Запусе remlf90.exe на renf90.par
	4) Парсинг файла с расчитанныеми вариансами.
	5) обновление файла параметров 1)
	6) выполнение 2)
	7) Подготовка данных для блапф90
		7ю1) Запуск blupf90.exe
	8) Сохранение необходимых файлов (remlf90.log, solution, renadd02.ped)
		.\MODEL_NAME
			.\FEATURE_NAME
				...
	'''

	default_struct_param = {
		'DATAFILE': '',
		'TRAITS': '12',
		'FIELDS_PASSED TO OUTPUT': '1',
		'RESIDUAL_VARIANCE': '0.5492E-01',
		'EFFECT': ['8 cross alpha', '10 cov', '1 cross alpha'],
		'RANDOM': 'animal',
		'FILE': '',
		'FILE_POS': ['1 2 3 0 0'],
		'(CO)VARIANCES': '0.7152E-02',
		'OPTION': ['sol se'],
	}

	def __init__(self,
				 file_ped,
				 file_prod,
				 feature_name=[],
				 fix_factor='',
				 model_name=[]):

		self.file_pedigree = file_ped
		self.file_productivity = file_prod
		self.feature = feature_name
		self.model = model_name
		self.fix_factor = fix_factor
		self.var_guestimate = 0

		self.input_file_param = 'params.txt'
		self.file_renf90 = 'renf90.par'
		self.file_variance = 'remlf90.log'
		self.file_aivariance = 'airemlf90.log'
		self.prog_blupf90 = 'blupf90.exe'
		self.prog_renumf90 = 'renumf90.exe'
		self.prog_remlf90 = 'remlf90.exe'
		self.prog_airemlf90 = 'airemlf90.exe'

		self.exception_file = os.listdir(os.getcwd())

		self.data_ped = pd.DataFrame()
		self.data_prod = pd.DataFrame()

		self.run_processing()

	def run_processing(self):
		try:
			self.load_data()
			self.__class__.default_struct_param.update(
				{
					'DATAFILE': os.path.split(self.file_productivity)[1],
					'FILE': os.path.split(self.file_pedigree)[1]}
			)

			for item_model in self.model:
				for item_feature in self.feature:
					print(
						f'	Обсчет модели {item_model},  признак - {item_feature}')

					# 1) Расчет предвартельных варианс
					self.calculation_of_preliminary_variances(item_feature)
					id_model = \
						self.data_prod.columns.to_list().index(item_model) + 1
					id_feature = self.data_prod.columns.to_list().index(
						item_feature) + 1

					# 2) Обновление файла параметров, заменив вариансы на
					# расчитанные
					parameters = self.update_dict_param(
						self.__class__.default_struct_param,
						{
							'TRAITS': f'{id_feature}',
							'RESIDUAL_VARIANCE': f'{self.var_guestimate}',
							'EFFECT':
								[f'{id_model} cross alpha', '11 cov', '1 cross alpha'],
							'(CO)VARIANCES':
								f'{round(self.var_guestimate/3, 2)}',
						}
					)

					# 3) Создание файла параметров
					self.create_file_param(parameters)

					# 4) Удаление из файлов данных название полей
					self.data_preparation()

					# 5) Запус renumf90, формирующий renf90.par, который
					# является входных файлом для последующих програм
					self.run_exe(self.prog_renumf90, self.input_file_param)

					# 6) Запуск remlf90.exe - поиск диссперсий
					self.run_exe(self.prog_airemlf90, self.file_renf90)

					# 7) Парсинг файла с рассчитанными вариансами и
					# обновление файла параметров
					calcul_var = self.parse_file_aivariance()
					new_param = self.update_dict_param(parameters, calcul_var)
					self.create_file_param(new_param)

					# 8) Повторение пункта 5)
					self.run_exe(self.prog_renumf90, self.input_file_param)

					# 9) Расчет blupf90.exe
					self.run_exe(self.prog_blupf90, self.file_renf90)

					self.save_data(dir_save=os.path.join(
						'Out_data', item_model, item_feature
					))

			# Возвращение данных к привычному виду
			self.data_preparation(default_choice=True)

		except Exception as err:
			print(err)

	def load_data(self):
		self.data_ped = pd.read_csv(
			self.file_pedigree, delimiter=' ', low_memory=False, dtype=str
		)

		self.data_prod = pd.read_csv(
			self.file_productivity, delimiter=' ', low_memory=False
		)

	def data_preparation(self, default_choice=False):

		if not default_choice:
			param = {'header': False, 'index': False, 'sep': ' '}
			self.data_ped.to_csv(self.file_pedigree, **param)
			self.data_prod.to_csv(self.file_productivity, **param)

		else:
			param = {'sep': ' ', 'index': False, 'chunksize': 300000}
			self.data_ped.to_csv(self.file_pedigree, **param)
			self.data_prod.to_csv(self.file_productivity, **param)

	def save_data(self, dir_save='./Out_files'):

		lst_files_for_move = list(filter(
			lambda x: x if x not in self.exception_file and
			not os.path.isdir(x) else False, os.listdir(os.getcwd())
		))

		if os.path.isdir(dir_save) and os.path.exists(dir_save):

			for item_file in lst_files_for_move:
				file = os.path.normpath(os.path.join('/', item_file))
				directory = os.path.normpath(dir_save)
				shutil.move(file, directory)

		else:
			os.makedirs(dir_save)
			self.save_data(dir_save=dir_save)

