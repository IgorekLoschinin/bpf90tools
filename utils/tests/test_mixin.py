#!/usr/bin/venv python
# coding: utf-8

from .. import CheckMixin
from pytest import fixture


@fixture
def mixin():
	return CheckMixin()


def test_mixin_is_not_file(mixin) -> None:
	_file = "asdf/af/da/sdfasd/fa/file.txt"
	assert not mixin.is_file(_file)


def test_mixin_is_file(mixin) -> None:
	_file = "./__init__.py"
	assert mixin.is_file(_file)


def test_mixin_is_not_dir(mixin) -> None:
	_dir = "asdf/af/da/sdfasd/fa"
	assert not mixin.is_dir(_dir)


def test_mixin_is_dir(mixin) -> None:
	_dir = "./"
	assert mixin.is_dir(_dir)


def test_mixin_is_not_empty(mixin) -> None:
	_struct = [['ds'], (1, 2), {'sd', }, 'sdf']

	for item in _struct:
		assert not mixin.is_empty(item)


def test_mixin_is_empty(mixin) -> None:
	_struct = [[], (), {}, '']

	for item in _struct:
		assert mixin.is_empty(item)
