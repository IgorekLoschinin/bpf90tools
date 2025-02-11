#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2025-2026 Igor Loschinin.
# Distributed under the lgplv3 software license, see the accompanying
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.

__author__ = "Igor Loschinin (igor.loschinin@gmail.com)"
__all__ = (
	"run_app",
	"transform",
)

import subprocess
import sys

from pathlib import Path


def run_app(app_file: Path, param_file: Path, dir_cwd: Path = None) -> bool:
	""" Running programs of the blupf90 family.

	:param app_file: Application to run.
	:param param_file: Parameter file that is needed to run the application.
	:param dir_cwd: Directory where the application is located.
	:return: Returns true if the method completed without errors, false if an
		error or exception occurred.
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
	system used.

	:param string: Name line.
	:return: Return the converting string.
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
