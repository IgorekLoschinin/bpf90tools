#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2025-2026 Igor Loschinin.
# Distributed under the lgplv3 software license, see the accompanying
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.

__author__ = "Igor Loschinin (igor.loschinin@gmail.com)"
__all__ = ("IParser", )

from abc import (
	ABC,
	abstractmethod
)


class IParser(ABC):
    """ Abstract class for file parsers.

    Defines an interface for classes that must implement methods
    for processing and reading files.
    """

    @abstractmethod
    def parse_file(self, file: str) -> None:
        """ Processes the specified file. """
        raise NotImplementedError

    @abstractmethod
    def _read(self, file) -> None:
        """ Reads the contents of the specified file. """
        raise NotImplementedError

