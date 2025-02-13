#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2025-2026 Igor Loschinin.
# Distributed under the lgplv3 software license, see the accompanying
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.

__author__ = "Igor Loschinin (igor.loschinin@gmail.com)"
__all__ = ("Keywords", )


class Keywords(object):
    """ A class that stores sets of keywords used in various genetic analysis
    programs.

    This class defines keyword sets for different software tools, such as
    RENUMF90, BLUPF90, REMLF90, and AIREMLF90. These keywords are used in
    parameter files to control various settings and options.
    """

    # Keywords for RENUMF90
    RENUMF90_keyword = {
        "DATAFILE",
        "SKIP_HEADER",
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
        "(CO)VARIANCES_MPE",
        "COMBINE",
        "OPTION alpha_size",
        "OPTION max_string_readline",
        "OPTION max_field_readline",
    }

    # Keywords for BLUPF90
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

    # Keywords for REMLF90 (Variance component estimation)
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

    # Keywords for AIREMLF90
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

    @property
    def unique_keywords(self) -> set[str]:
        """ Returns a set of all unique keywords from all keyword groups. """
        return (
            self.__class__.RENUMF90_keyword
            | self.__class__.BLUPF90_keyword
            | self.__class__.REMLF90_keyword
            | self.__class__.AIREMLF90_keyword
        )

    @property
    def single_par(self) -> set[str]:
        """ Returns a set of keywords that typically take a single
        parameter. """
        return {
            "DATAFILE",
            "EFFECT",
            "FILE",
            "FILE_POS",
            "GEN_INT",
            "INBREEDING",
            "NESTED",
            "OPTIONAL",
            "PED_DEPTH",
            "RANDOM",
            "REC_SEX",
            "RESIDUAL_VARIANCE",
            "SNP_FILE",
            "TRAITS",
            "UPG_TYPE",
            "WEIGHT(S)",
            "(CO)VARIANCES",
            "(CO)VARIANCES_MPE",
            "(CO)VARIANCES_PE",
            "FIELDS_PASSED TO OUTPUT",
        }

    @property
    def complex_par(self) -> set[str]:
        """ Returns a set of keywords that are more complex and may take
        multiple parameters. """
        return {
            "COMBINE",
            "OPTION",
        }
