#!/usr/bin/venv python
# coding: utf-8


class Keywords(object):
	RENUMF90_keyword = {
		"DATAFILE",
		"TRAITS",
		"FIELDS_PASSED TO OUTPUT",
		"WEIGHT(S)",
		"RESIDUAL_VARIANCE",
		"EFFECT",
		"NESTED",
		"RANDOM",
		"OPTIONAL",
		"FILE",
		"FILE_POS",
		"SNP_FILE",
		"PED_DEPTH",
		"GEN_INT",
		"REC_SEX",
		"UPG_TYPE",
		"INBREEDING",
		"(CO)VARIANCES",
		"(CO)VARIANCES_PE",
		"(CO)VARIANCES_PE",
		"(CO)VARIANCES_MPE",
		"COMBINE",
		"OPTION alpha_size",
		"OPTION max_string_readline",
		"OPTION max_field_readline",
	}

	# --------- BLUP ---------
	BLUPF90_keyword = {
		"OPTION conv_crit",
		"OPTION maxrounds",
		"OPTION solv_method",
		"OPTION r_factor",
		"OPTION sol",
		"OPTION blksize",
		"OPTION use_yams",
		"OPTION hetres_int",
		"OPTION fixed_var",
	}

	# ----------- Variance component estimation -----------
	REMLF90_keyword = {
		"OPTION conv_crit",
		"OPTION maxrounds",
		"OPTION sol",
		"OPTION",
		"OPTION constant_var",
		"OPTION missing",
		"OPTION use_yams",
		"OPTION SNP_file",
	}

	AIREMLF90_keyword = {
		"OPTION conv_crit",
		"OPTION maxrounds",
		"OPTION EM-REML",
		"OPTION sol",
		"OPTION tol",
		"OPTION fact_once",
		"OPTION constant_var",
		"OPTION missing",
		"OPTION use_yams",
		"OPTION approx_loglike",
		"OPTION hetres_pos",
		"OPTION hetres_pol",
		"OPTION SNP_file",
		"OPTION se_covar_function",
	}

	all_join_keyword = \
		RENUMF90_keyword | \
		BLUPF90_keyword | \
		REMLF90_keyword | \
		AIREMLF90_keyword

	@property
	def single_par(self) -> None:
		pass

	@property
	def complex_par(self) -> None:
		pass
