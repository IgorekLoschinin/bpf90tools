#!/usr/bin/venv python
# coding: utf-8

from pathlib import Path
from pydantic import BaseModel

from . import IParser
from ..utils import CheckMixin


class Variance(BaseModel):
	varG: float = None
	varE: float = None
	aic: float = None
	bic: float = None
	heritability: float = None


class PVar(IParser, CheckMixin):
	""" Processing the file method (ai)remlf90 in which the variance information
	is stored """

	def __init__(self) -> None:
		self.__variance = Variance()
		self.__lst_strings = []

	@property
	def values(self) -> Variance | None:
		return self.__variance

	def parse_file(self, pth_file: str | Path) -> bool:
		""" Parsing the log file of the (ai)remlf90.exe(sh) program

		:param pth_file: - The path to the file log
		"""

		if isinstance(pth_file, str):
			pth_file = Path(pth_file)

		if not pth_file.is_absolute():
			pth_file = pth_file.absolute()

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
					div_item_on_part = tuple(filter(
						lambda x: x.strip(":")
						if not self.is_empty(x) and x != '='
						else None,
						line.split(" ")
					))

					self.__variance.bic = float(div_item_on_part[1])
					self.__variance.aic = float(div_item_on_part[3])

			self._heritability()

		except Exception:
			return False

		return True

	def _read(self, file: Path) -> None:
		""" Reading a file

		:param file: - The path to the file
		"""
		with file.open(mode='r', encoding="utf-8") as file_log:
			self.__lst_strings = list(map(
				lambda x: x.strip(), file_log
			))

	def _next_value(self, elem: str) -> int:
		""" Determines the index of the next element in the list

		:param elem: - List item
		:return: - Return the index of the next element
		"""

		return self.__lst_strings.index(elem) + 1

	def _heritability(self) -> None:
		""" Heritability, the degree of conditionality of the phenotypic
		variability of any trait in an animal population by genotypic
		differences between individuals """

		try:
			if (self.__variance.varE and self.__variance.varG) is not None:
				self.__variance.heritability = round(
					self.__variance.varG / (
							self.__variance.varG + self.__variance.varE
					), 3)

		except ZeroDivisionError:
			self.__variance.heritability = 0
