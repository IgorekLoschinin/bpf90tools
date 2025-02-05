#!/usr/bin/env python
# coding: utf-8

BASE_TEMPLET_SINGLE_BLUP = {
	'DATAFILE': [''],
	'TRAITS': [''],
	'FIELDS_PASSED TO OUTPUT': ['1'],
	'RESIDUAL_VARIANCE': ['0.5492E-01'],
	'EFFECT': ['8 cross alpha', '10 cov', '1 cross alpha'],
	'RANDOM': ['animal'],
	'FILE': [''],
	'FILE_POS': ['1 2 3 0 0'],
	'(CO)VARIANCES': ['0'],
	'OPTION sol': ['se'],
	'OPTION alpha_size': ['40'],
	'OPTION fact_once': ['memory'],
	'OPTION': ['use_yams'],
}

BASE_TEMPLET_SINGLE_GBLUP = {
	'DATAFILE': [''],
	'TRAITS': ['12'],
	'FIELDS_PASSED TO OUTPUT': ['1'],
	'RESIDUAL_VARIANCE': ['0.5492E-01'],
	'EFFECT': ['8 cross alpha', '10 cov', '1 cross alpha'],
	'RANDOM': ['animal'],
	'FILE': [''],
	'FILE_POS': ['1 2 3 0 0'],
	'SNP_FILE': [""],
	'(CO)VARIANCES': ['0'],
	'OPTION sol': ['se'],
	'OPTION alpha_size': ['40'],
	'OPTION fact_once': ['memory'],
	'OPTION': ['use_yams'],
}
