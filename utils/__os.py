#!/usr/bin/env python
# coding: utf-8

import sys


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
