#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2025-2026 Igor Loschinin.
# Distributed under the lgplv3 software license, see the accompanying
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.

__author__ = "Igor Loschinin (igor.loschinin@gmail.com)"
__all__ = ("If90", )

from abc import (
	ABC,
	abstractmethod
)
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
