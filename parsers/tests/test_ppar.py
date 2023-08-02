#!/usr/bin/env python
# coding: utf-8
from pathlib import Path

from .. import PParams
from . import _DIR_FILES

import pytest

_FILES_PPARAMS = Path(_DIR_FILES) / "pparam_f"


@pytest.fixture
def obj_pparams():
	return PParams()


def test_not_params(obj_pparams) -> None:
	_file = _FILES_PPARAMS / "param123113.txt"

	with pytest.raises(OSError, match="File param.txt not found!"):
		obj_pparams.parse_file(_file)


def test_bp_params_1(obj_pparams) -> None:
	_file = _FILES_PPARAMS / "param1.txt"
	valid_struct = {
		'DATAFILE': ['phen.txt'],
		'TRAITS': ['5'],
		'FIELDS_PASSED TO OUTPUT': ['1'],
		'RESIDUAL_VARIANCE': ['1.0'],
		'EFFECT': [
			'1 cross alpha',
			'2 cross alpha',
			'3 cov',
			'4 cross alpha',
			'6 cross alpha'
		],
		'RANDOM': ['animal'],
		'FILE': ['ped.txt'],
		'FILE_POS': ['1 2 3 0 0'],
		'(CO)VARIANCES': ['0.65'],
		'OPTION': ['sol se', 'alpha_size 40'],
	}

	assert obj_pparams.parse_file(_file)
	assert valid_struct == pytest.approx(obj_pparams.params)


def test_bp_params_2(obj_pparams) -> None:
	_file = _FILES_PPARAMS / "param2.txt"
	valid_struct = {
		'DATAFILE': ['phen.txt'],
		'TRAITS': ['5'],
		'FIELDS_PASSED TO OUTPUT': ['1'],
		'RESIDUAL_VARIANCE': ['1.0'],
		'EFFECT': [
			'1 cross alpha',
			'2 cross alpha',
			'3 cov',
			'4 cross alpha',
			'6 cross alpha'
		],
		'RANDOM': ['animal'],
		'FILE': ['ped.txt']
	}

	assert obj_pparams.parse_file(_file)
	assert valid_struct == pytest.approx(obj_pparams.params)


def test_bp_params_3(obj_pparams) -> None:
	_file = _FILES_PPARAMS / "param3.txt"
	valid_struct = {
		'DATAFILE': ['phen.txt'],
		'TRAITS': ['5'],
		'FIELDS_PASSED TO OUTPUT': ['1'],
		'RESIDUAL_VARIANCE': ['1.0'],
		'EFFECT': [
			'1 cross alpha',
			'2 cross alpha',
			'3 cov',
			'4 cross alpha',
			'6 cross alpha'
		],
		'RANDOM': ['animal'],
		'FILE': ['ped.txt'],
		'FILE_POS': ['1 2 3 0 0'],
		'(CO)VARIANCES': ['0.65'],
		'OPTION': ['sol se', 'alpha_size 40'],
	}

	assert obj_pparams.parse_file(_file)
	assert valid_struct != pytest.approx(obj_pparams.params)


def test_bp_params_4(obj_pparams) -> None:
	_file = _FILES_PPARAMS / "param4.txt"
	valid_struct = {}

	assert obj_pparams.parse_file(_file)
	assert valid_struct == pytest.approx(obj_pparams.params)


def test_bp_params_5(obj_pparams) -> None:
	_file = _FILES_PPARAMS / "param5.txt"
	valid_struct = {
		'DATAFILE': ['phen.txt'],
		'TRAITS': ['5'],
		'FIELDS_PASSED TO OUTPUT': [''],
		'WEIGHT(S)': [''],
		'RESIDUAL_VARIANCE': ['1.0'],
		'EFFECT': [
			'1 cross alpha',
			'2 cross alpha',
			'3 cov',
			'4 cross alpha',
			'6 cross alpha'
		],
		'RANDOM': ['animal'],
		'FILE': ['ped.txt'],
		'FILE_POS': ['1 2 3 0 0'],
		'(CO)VARIANCES': ['0.65'],
		'OPTION': ['sol se', 'alpha_size 40'],
	}

	assert obj_pparams.parse_file(_file)
	assert valid_struct == pytest.approx(obj_pparams.params)
