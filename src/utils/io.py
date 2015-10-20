#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import os


def browse(dir):
    all_files = list()
    for root, dirs, files in os.walk(dir):
        for f in files:
            all_files.append(os.path.join(root, f))
    return all_files


def _mkdir_recursive(path):
    sub_path = os.path.dirname(path)
    if not os.path.exists(sub_path):
        _mkdir_recursive(sub_path)
    if not os.path.exists(path):
        os.mkdir(path)


def mkdir(f, is_file=True):
    path = f if not is_file else os.path.dirname(f)
    _mkdir_recursive(path)


def strip_ext(f):
    filename, file_extension = os.path.splitext(f)
    return filename
