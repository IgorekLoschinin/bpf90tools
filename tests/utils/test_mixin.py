#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2025-2026 Igor Loschinin.
# Distributed under the lgplv3 software license, see the accompanying
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.

__author__ = "Igor Loschinin (igor.loschinin@gmail.com)"

from pytest import fixture
from bpf90tools.src.bpf90tools._utils import CheckMixin


@fixture
def mixin():
	return CheckMixin()


def test_mixin_is_not_file(mixin) -> None:
	_file = "asdf/af/da/sdfasd/fa/file.txt"
	assert not mixin.is_file(_file)


def test_mixin_is_file(mixin) -> None:
	_file = "__init__.py"
	assert mixin.is_file(_file)


def test_mixin_is_not_dir(mixin) -> None:
	_dir = "asdf/af/da/sdfasd/fa"
	assert not mixin.is_dir(_dir)


def test_mixin_is_dir(mixin) -> None:
	_dir = "/"
	assert mixin.is_dir(_dir)


def test_mixin_is_not_empty(mixin) -> None:
	_struct = [['ds'], (1, 2), {'sd', }, 'sdf']

	for item in _struct:
		assert not mixin.is_empty(item)


def test_mixin_is_empty(mixin) -> None:
	_struct = [[], (), {}, '']

	for item in _struct:
		assert mixin.is_empty(item)
