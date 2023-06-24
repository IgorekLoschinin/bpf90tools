#!/usr/bin/env python
# coding: utf-8
from __future__ import annotations

from pathlib import Path
from functools import reduce, wraps

import time
import json
import subprocess
import pandas as pd


def timeit(func):

    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper


def merge_lst_df(
        lst_df: list[pd.DataFrame], key_on: str, how: str = 'inner'
) -> pd.DataFrame:
    """ Sequential concatenation of dataframes that contain one common field.

    :param lst_df: - List of data frames to be merged into one
    :param key_on: - The key field by which it will be necessary to merge
    :param how: Type of merge to be performed.
            {‘left’, ‘right’, ‘outer’, ‘inner’, ‘cross’}, default ‘inner’
    :return: A DataFrame of the list merged objects
    """
    return reduce(
        lambda df1, df2: pd.merge(df1, df2, on=key_on, how=how),
        lst_df
    )


def run_app(app_file: Path, param_file: Path, dir_cwd: Path = None) -> int:
    """

    :param app_file:
    :param param_file:
    :param dir_cwd:
    :return:
    """

    try:
        process = subprocess.Popen(
            args=[f"ulimit -s unlimited && {app_file}"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            cwd=str(dir_cwd),
            shell=True
        )
        cmd_out, _ = process.communicate(f'{param_file.name}\n'.encode())

        with open(
                app_file.parent.joinpath(
                    f'{app_file.stem}_console_output.log'), 'w'
        ) as save_file:
            save_file.write(cmd_out.decode())

        code = process.wait()

    except Exception as e:
        raise e

    return code


def calculate_preliminary_variances(feature: pd.Series) -> float:
    """ Calculation of intermediate variances. """
    return round((feature.var()) / 2.5, 2)


def to_json(
        obj: list | dict, to_file: str | Path = "", mode: str = "w"
) -> bool:
    """ Write to json file.

    :param obj:
    :param to_file:
    :param mode:
    :return:
    """

    try:
        with open(to_file, mode) as file:
            json.dump(obj, file, indent=4)

    except Exception as e:
        return False

    return True


def from_json(to_file: str | Path) -> list | dict | None:
    """ Upload json format file.

    :param to_file:
    :return:
    """

    try:
        if Path(to_file).is_file() and Path(to_file).exists():
            with open(to_file, 'r') as file:
                return json.load(file)

    except Exception as e:
        print(e)
