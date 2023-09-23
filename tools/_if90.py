#!/usr/bin/venv python
# coding: utf-8

__author__ = "Igor Loschinin (igor.loschinin@gmail.com)"

from abc import ABC, abstractmethod
from pathlib import Path


class If90(ABC):

	def __init__(
			self, *, app: str, work_dir: str | Path, fn_par: str | None = None
	) -> None:
		self._app = app
		self._work_dir = work_dir
		self._par_file = fn_par

	@property
	def work_dir(self) -> Path:
		return self._work_dir

	@property
	def file_par(self) -> str | None:
		return self._par_file

	@abstractmethod
	def run(self) -> bool:
		raise NotImplementedError

