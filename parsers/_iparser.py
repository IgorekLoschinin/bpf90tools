#!/usr/bin/venv python
# coding: utf-8
from abc import ABC, abstractmethod


class IParser(ABC):

	@abstractmethod
	def parse_file(self, file: str) -> None:
		raise NotImplementedError

	@abstractmethod
	def _read(self, file) -> None:
		raise NotImplementedError
