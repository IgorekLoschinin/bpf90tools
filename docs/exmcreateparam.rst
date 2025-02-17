Create param file
=================

Automatic generation of parameter file
""""""""""""""""""""""""""""""""""""""

The library has a module ``bpf90tools.tools.tempconfig``, which offers templates
(examples) on how to correctly build an object with parameters to be passed
to Params. You can take it from the lib and modify it.

**The contents of tempconfig**::

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


.. note::
    The object is a slavar, where key is the exact name of the parameter,
    value is the value or type of its property.

.. note::
    The OPTION parameter can be grouped. It looks like this:
     'OPTION': ['sol se', 'alpha_size 40', 'fact_once memory', 'use_yams'].

Create param
""""""""""""

**Import lib**::

    from bpf90tools import Params

    from bpf90tools.tools.tempconfig import (
        BASE_TEMPLET_SINGLE_BLUP,
        BASE_TEMPLET_SINGLE_GBLUP
    )

**1. Recording a template object**

* for blup::

    create_param_blup = Params(
        file_config="./foldtest/test1/exm_create_param/param_exm_blup.txt"
    )
    create_param_blup.create(BASE_TEMPLET_SINGLE_BLUP)

Result::

        #PARAMETER FILE
        DATAFILE

        TRAITS

        FIELDS_PASSED TO OUTPUT
        1
        RESIDUAL_VARIANCE
            0.5492E-01
        EFFECT
        8 cross alpha
        EFFECT
        10 cov
        EFFECT
        1 cross alpha
        RANDOM
        animal
        FILE

        FILE_POS
        1 2 3 0 0
        (CO)VARIANCES
            0
        OPTION sol se
        OPTION alpha_size 40
        OPTION fact_once memory
        OPTION use_yams


* for gblup::

    create_param_gblup = Params(
        file_config="./foldtest/test1/exm_create_param/param_exm_gblup.txt"
    )
    create_param_gblup.create(BASE_TEMPLET_SINGLE_GBLUP)

Result::

    #PARAMETER FILE
    DATAFILE

    TRAITS
    12
    FIELDS_PASSED TO OUTPUT
    1
    RESIDUAL_VARIANCE
        0.5492E-01
    EFFECT
    8 cross alpha
    EFFECT
    10 cov
    EFFECT
    1 cross alpha
    RANDOM
    animal
    FILE

    FILE_POS
    1 2 3 0 0
    SNP_FILE

    (CO)VARIANCES
        0
    OPTION sol se
    OPTION alpha_size 40
    OPTION fact_once memory
    OPTION use_yams

**2. Template modification - adding values in place of omissions**

* for blup::

    object_param_blup = BASE_TEMPLET_SINGLE_BLUP.copy()
    object_param_blup.update({
        'DATAFILE': ['data.txt'],
        'TRAITS': ['2'],
        'RESIDUAL_VARIANCE': ['0.5492E-01'],
        'EFFECT': ['8 cross alpha', '6 cross alpha', '10 cov', '1 cross alpha'],
        'RANDOM': ['diagonal'],
        'FILE': ['pedigree.txt'],
    })

    create_param_blup = Params(
        file_config="./foldtest/test1/exm_create_param/param_exm_blup_mod.txt"
    )
    create_param_blup.create(object_param_blup)

Result::

    #PARAMETER FILE
    DATAFILE
    data.txt
    TRAITS
    2
    FIELDS_PASSED TO OUTPUT
    1
    RESIDUAL_VARIANCE
        0.5492E-01
    EFFECT
    8 cross alpha
    EFFECT
    6 cross alpha
    EFFECT
    10 cov
    EFFECT
    1 cross alpha
    RANDOM
    diagonal
    FILE
    pedigree.txt
    FILE_POS
    1 2 3 0 0
    (CO)VARIANCES
        0
    OPTION sol se
    OPTION alpha_size 40
    OPTION fact_once memory
    OPTION use_yams

* for gblup::

    object_param_gblup = BASE_TEMPLET_SINGLE_GBLUP.copy()
    object_param_gblup.update({
        'DATAFILE': ['dataphen.txt'],
        'TRAITS': ['12'],
        'FIELDS_PASSED TO OUTPUT': ['1'],
        'RESIDUAL_VARIANCE': ['0.5492E-01'],
        'EFFECT': ['8 cross alpha', '10 cov', '1 cross alpha'],
        'RANDOM': ['animal'],
        'FILE': ['ped.txt'],
        'FILE_POS': ['1 2 3 0 0'],
        'SNP_FILE': ["snp.txt"],
        '(CO)VARIANCES': ['0.123'],
    })

    create_param_gblup = Params(
        file_config="./foldtest/test1/exm_create_param/param_exm_gblup_mod.txt"
    )
    create_param_gblup.create(object_param_gblup)

Result::

    #PARAMETER FILE
    DATAFILE
    dataphen.txt
    TRAITS
    12
    FIELDS_PASSED TO OUTPUT
    1
    RESIDUAL_VARIANCE
        0.5492E-01
    EFFECT
    8 cross alpha
    EFFECT
    10 cov
    EFFECT
    1 cross alpha
    RANDOM
    animal
    FILE
    ped.txt
    FILE_POS
    1 2 3 0 0
    SNP_FILE
    snp.txt
    (CO)VARIANCES
        0.123
    OPTION sol se
    OPTION alpha_size 40
    OPTION fact_once memory
    OPTION use_yams


**3. Composition of the object according to the proposed file**

For example, we have this config::

    DATAFILE
     datarep
    TRAITS
     4
    FIELDS_PASSED TO OUTPUT

    WEIGHT(S)

    RESIDUAL_VARIANCE
      1.0
    EFFECT
     2 cross alpha
    EFFECT
     3 cross alpha
    EFFECT
     8 cov
    EFFECT
     1 cross alpha
    RANDOM
     animal
    OPTIONAL
     pe
    FILE
     ped1
    FILE_POS
     1 2 3 0 0
    PED_DEPTH
     3
    (CO)VARIANCES
      0.65
    (CO)VARIANCES_PE
      0.21

In the form of a dictionary::

    object_param = {
        'DATAFILE': ['datarep'],
        'TRAITS': ['4'],
        'FIELDS_PASSED TO OUTPUT': [''],
        'WEIGHT(S)': [''],
        'RESIDUAL_VARIANCE': ['1.0'],
        'EFFECT': ['2 cross alpha', '3 cross alpha', '8 cov', '1 cross alpha'],
        'RANDOM': ['animal'],
        'FILE': ['ped1'],
        'FILE_POS': ['1 2 3 0 0'],
        'PED_DEPTH': ['3'],
        '(CO)VARIANCES': ['0.65'],
        '(CO)VARIANCES_PE': ['0.21'],
    }

Generate param::

    create_param = Params(
        file_config="./foldtest/test1/exm_create_param/param_exm_rand.txt"
    )
    create_param.create(object_param)

Result::

    #PARAMETER FILE
    DATAFILE
    datarep
    TRAITS
    4
    FIELDS_PASSED TO OUTPUT

    WEIGHT(S)

    RESIDUAL_VARIANCE
        1.0
    EFFECT
    2 cross alpha
    EFFECT
    3 cross alpha
    EFFECT
    8 cov
    EFFECT
    1 cross alpha
    RANDOM
    animal
    FILE
    ped1
    FILE_POS
    1 2 3 0 0
    PED_DEPTH
    3
    (CO)VARIANCES
        0.65
    (CO)VARIANCES_PE
    0.21
