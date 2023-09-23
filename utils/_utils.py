#!/usr/bin/env python
# coding: utf-8
from __future__ import annotations

from pathlib import Path

import sys
import subprocess


def run_app(app_file: Path, param_file: Path, dir_cwd: Path = None) -> bool:
    """ Running programs of the blupf90 family

    :param app_file: - Application to run
    :param param_file: - Parameter file that is needed to run the application
    :param dir_cwd: - Directory where the application is located
    :return: - Returns true if the method completed without errors, false if
        an error or exception occurred
    """

    try:
        _args = None
        match sys.platform:
            case "win32":
                _args = [str(app_file)]

            case "linux":
                _args = [f"ulimit -s unlimited && {app_file}"]

        process = subprocess.Popen(
            args=_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            cwd=str(dir_cwd) if dir_cwd is not None else dir_cwd,
            shell=True
        )
        cmd_out, _ = process.communicate(f'{param_file.name}\n'.encode())

        with open(
                app_file.parent.joinpath(
                    f'{app_file.stem}_console_output.log'), 'w'
        ) as save_file:
            save_file.write(cmd_out.decode())

    except Exception as e:
        return False

    return True


def transform(string: str) -> str:
    """ Converting a string with the name of the program for the operating
    system used

    :param string: - Name line
    :return: Return the converting string
    """

    match sys.platform:
        case "win32":
            return f"{string}.exe"

        case "linux":
            return string

        case _:
            raise Exception(
                f"Not processed for this platform - {sys.platform}"
            )
