#!/usr/bin/venv python
# coding: utf-8
from pathlib import Path
from ..utils import CheckMixin

from pydantic import BaseModel


class Variance(BaseModel):
	varG: float = None
	varE: float = None
	aic: float = None
	bic: float = None
	heritability: float = None


class PAIReml(CheckMixin):
	""" Processing the file method airemlf90 in which the variance information
	is stored """

	def __init__(self) -> None:
		self.__variance = Variance()
		self.__lst_strings = []

	@property
	def values(self) -> Variance | None:
		return self.__variance

	def parse_file(self, pth_file: str | Path) -> None:
		""" Parsing the log file of the airemlf90.exe(sh) program

		:param pth_file:
		:return:
		"""

		if isinstance(pth_file, str):
			pth_file = Path(pth_file)

		if not self.is_file(pth_file):
			raise OSError(f"The path - {pth_file.stem}, passed is not a file!")

		try:
			self._read(pth_file)

			for line in self.__lst_strings:

				if 'Genetic variance(s)' in line:
					self.__variance.varG = \
						float(self.__lst_strings[self._next_value(line)])

				elif 'Residual variance(s)' in line:
					self.__variance.varE = \
						float(self.__lst_strings[self._next_value(line)])

				elif '-2logL' and 'AIC' in line:
					div_item_on_part = line.split(':')

					for i_part in div_item_on_part:
						if '-2logL' in i_part:
							self.__variance.bic = \
								float(i_part.split('=')[-1].strip())

						elif 'AIC' in i_part:
							self.__variance.aic = \
								float(i_part.split('=')[-1].strip())

			self._heritability()

		except Exception as exp:
			raise exp

	def _read(self, file: Path) -> None:
		"""

		:param file:
		:return:
		"""
		with file.open(mode='r', encoding="utf-8") as file_log:
			self.__lst_strings = list(map(
				lambda x: x.strip(), file_log.readlines()
			))

	def _next_value(self, elem: str) -> int:
		"""

		:param elem:
		:return:
		"""

		return self.__lst_strings.index(elem) + 1

	def _heritability(self) -> None:
		"""  """
		try:
			self.__variance.heritability = round(
				self.__variance.varG / (
						self.__variance.varG + self.__variance.varE
				), 3)

		except ZeroDivisionError:
			self.__variance.heritability = 0
