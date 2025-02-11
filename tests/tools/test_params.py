#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2025-2026 Igor Loschinin.
# Distributed under the lgplv3 software license, see the accompanying
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.

__author__ = "Igor Loschinin (igor.loschinin@gmail.com)"

import pytest

from bpf90tools.src.bpf90tools import Params


@pytest.fixture
def obj_params(tmp_path) -> Params:
	_dir_par = tmp_path / "param"
	_dir_par.mkdir(parents=True)

	return Params(file_config=_dir_par / "param.txt")


class TestParams(object):

	def test_params_successful(self, obj_params) -> None:
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

		assert obj_params.create(valid_struct)
		assert not obj_params.create({})

	@pytest.mark.parametrize(
		"valid_struct",
		[
			{'DATAFILE': [10]},
			{'DATAFILE': [{}]},
			{'DATAFILE': 10},
		]
	)
	def test_fails_params(
			self, obj_params: Params, valid_struct: dict
	) -> None:

		assert not obj_params.create(valid_struct)
