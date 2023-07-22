#!/usr/bin/venv python
# coding: utf-8

from abc import ABC, abstractmethod
from pathlib import Path


class If90(ABC):

	def __init__(
			self, *, app: str, work_dir: str | Path, fn_par: str | None = None
	) -> None:
		self._app = app
		self._work_dir = work_dir
		self._par_file = fn_par

	@abstractmethod
	def run(self) -> bool:
		raise NotImplementedError
