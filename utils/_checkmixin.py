#!/usr/bin/env python
# coding: utf-8
from pathlib import Path


class CheckMixin(object):
    """ A mixin class that is used to validate data, files, and directories.
    Used to refine the behavior of other classes, not intended to spawn
    self-usable objects """

    @staticmethod
    def is_file(pth_file: str | Path) -> bool:
        """ Method that checks if the passed path points to a file

        :param pth_file: Path to the file to be checked for existence
        :return: Return true if the file exists and false if the file does not
                    exist
        """
        pointer_on_file = Path(pth_file)

        if pointer_on_file.is_file() and pointer_on_file.exists():
            return True

        return False

    @staticmethod
    def is_dir(path_dir: str | Path) -> bool:
        """ Method that checks if the passed path points to a directory

        :param path_dir: - Path to the directory to be checked for existence
        :return: Return true if the directory exist and false if the dir does
                    not exist
        """
        pointer_on_dir = Path(path_dir)

        if pointer_on_dir.is_dir() and pointer_on_dir.exists():
            return True

        return False

    @staticmethod
    def is_empty(obj: str | list | dict | set | tuple) -> bool:
        """ The method checks if the passed object is empty.

        :param obj: - A object of the standard type to checked if is empty
                        or not
        :return: - Return true if of the object empty and false if not empty
        """

        if len(obj) != 0:
            return False

        return True
