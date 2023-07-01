#!/usr/bin/venv python
# coding: utf-8


class Keyword(object):
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

	BLUP90IOD2_keyword = {
		"OPTION conv_crit",
		"OPTION maxrounds",
		"OPTION blksize",
		"OPTION init_eq",
		"OPTION solv_method",
		"OPTION tol",
		"OPTION residual",
		# вероятно ошибка. residual - это значение, а не настройка
		"OPTION avgeps",
		"OPTION cont",
		"OPTION missing",
		"OPTION restart",
		"OPTION prior_solutions",
		"OPTION random_upg",
		"OPTION SNP_file",
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

	# ----------- Genomic programs -----------
	PREGSF90_keyword = {
		"OPTION SNP_file",
		"OPTION chrinfo",
		"OPTION sex_chr",
		"OPTION readGimA22i",
		"OPTION saveAscii",
		"OPTION whichG",
		"OPTION whichfreq",
		"OPTION FreqFile",
		"OPTION whichScale",
		"OPTION weightedG",
		"OPTION maxsnp",
		"OPTION minfreq",
		"OPTION callrate",
		"OPTION callrateAnim",
		"OPTION monomorphic",
		"OPTION hwe",
		"OPTION high_correlation",
		"OPTION verify_parentage",
		"OPTION exclusion_threshold",
		"OPTION exclusion_threshold_snp",
		"OPTION number_parent_progeny_evaluations",
		"OPTION outparent_progeny",
		"OPTION excludeCHR",
		"OPTION sex_chr",
		"OPTION threshold_duplicate_samples",
		"OPTION threshold_diagonal_g",
		"OPTION plotpca",
		"OPTION extra_info_pca",
		"OPTION saveCleanSNPs",
		"OPTION no_quality_control",
		"OPTION outcallrate",
		"OPTION thrWarnCorAG",
		"OPTION thrStopCorAG",
		"OPTION thrCorAG",
		"OPTION TauOmega",
		"OPTION AlphaBeta",
		"OPTION GammaDelta",
		"OPTION tunedG",
		"OPTION AlphaBeta",
		"OPTION nthreads",
		"OPTION ntheadsiod",
		"OPTION graphics",
		"OPTION msg",
		"OPTION saveAscii",
		"OPTION saveHinv",
		"OPTION saveAinv",
		"OPTION saveHinvOrig",
		"OPTION saveAinvOrig",
		"OPTION saveDiagGOrig",
		"OPTION saveGOrig",
		"OPTION saveA22Orig",
		"OPTION readOrigId",
		"OPTION savePLINK",
		"OPTION readGimA22i",
		"OPTION saveA22",
		"OPTION saveA22Inverse",
		"OPTION saveG",
		"OPTION saveGInverse",
		"OPTION saveGmA22",
		"OPTION readG",
		"OPTION readA22",
		"OPTION readA22Inverse",
		"OPTION readGmA22",
		"OPTION saveGInverse",
		"OPTION saveGInverse",
	}

	POSTGSF90_keyword = {
		"OPTION Manhattan_plot",
		"OPTION Manhattan_plot_R",
		"OPTION plotsnp",
		"OPTION SNP_moving_average",
		"OPTION windows_variance",
		"OPTION windows_variance_mbp",
		"OPTION windows_variance_type",
		"OPTION which_weight",
		"OPTION solutions_postGS",
		"OPTION postgs_trt_eff",
		"OPTION snp_effect_gebv",
		"OPTION snp_effect_dgv",
		"OPTION SNP_file",
		"OPTION se_covar_function",
	}

	all_join_keyword = \
		RENUMF90_keyword | \
		BLUPF90_keyword | \
		REMLF90_keyword | \
		AIREMLF90_keyword

	# BLUP90IOD2_keyword |\
	# PREGSF90_keyword |\
	# POSTGSF90_keyword
