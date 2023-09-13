#!/usr/bin/venv python
# coding: utf-8

__author__ = "Igor Loschinin (igor.loschinin@gmail.com)"

from . import _DIR_UTILS
from .. import Renumf90

import pytest


@pytest.fixture
def obj_renum(request) -> Renumf90:
	return Renumf90(**request.param)


class TestRenumf90(object):

	def test_(self) -> None:
		...
