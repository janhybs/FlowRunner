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
    f = os.path.abspath(f)
    path = f if not is_file else os.path.dirname(f)
    _mkdir_recursive(path)


def strip_ext(f):
    filename, file_extension = os.path.splitext(f)
    return filename


def abs_path (path):
    return os.path.abspath(path)


def join_path(*paths):
    return os.path.join(*paths)


def end_path (path, level=1):
    paths = []
    for i in range(level):
        paths.append(os.path.basename(path))
        path = os.path.dirname(path)
        if path == os.path.dirname(path):
            break
    paths.reverse()
    return join_path(*paths)


def relative (root, subdir):
    common = os.path.commonprefix([root, subdir])
    rel = subdir.replace(common, '')

    if subdir != rel and rel.startswith('/'):
        return rel.lstrip('/')
    return rel
