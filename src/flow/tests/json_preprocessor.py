#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import json


class JsonPreprocessor(object):
    int_props = ['task-size']
    float_props = ['timer-resolution']
    date_props = ['run-finished-at', 'run-started-at']
    del_props = ['run-process-count', 'stdout', 'program-build']
    int_recursive_props = ['call-count', 'call-count-min', 'call-count-max', 'call-count-sum', 'file-line']
    float_recursive_props = ['cumul-time', 'cumul-time-min', 'cumul-time-max', 'cumul-time-sum', 'percent']

    @staticmethod
    def clean_json(json_report):
        """
        Method will converts specific field to correct type, also some fields will be removed and some fields created
        :param obj:
        :return:
        """
        # simple fields
        json_report = JsonPreprocessor.convert_fields(json_report, int, JsonPreprocessor.int_props)
        json_report = JsonPreprocessor.convert_fields(json_report, float, JsonPreprocessor.float_props)
        # recursive fields
        json_report = JsonPreprocessor.convert_fields(json_report, int, JsonPreprocessor.int_recursive_props, True)
        json_report = JsonPreprocessor.convert_fields(json_report, float, JsonPreprocessor.float_recursive_props, True)
        json_report = JsonPreprocessor.create_prop(json_report, 'program-flags', 'program-build',
                                                   lambda x: x.split()[x.split().index('flags:') + 1:])
        json_report = JsonPreprocessor.delete_props(json_report, JsonPreprocessor.del_props)

        return json_report

    @staticmethod
    def merge_json_info(info_dict={}, files=[]):
        """
        Merges multiple json together
        :param info_dict: dict object
        :param files: list of file location
        :return:
        """
        result = info_dict.copy()
        for f in files:
            with open(f, 'r') as fp:
                json_data = json.load(fp)
                result.update(json_data)
        return result

    @staticmethod
    def convert_fields(obj, type, fields, recursive=False):
        """
        Converts given fields to specific type
        :param obj:
        :param type:
        :param fields:
        :param recursive:
        :return:
        """
        for p in fields:
            if p in obj:
                obj[p] = type(obj[p])

        if recursive and 'children' in obj:
            for item in obj['children']:
                JsonPreprocessor.convert_fields(item, type, fields, recursive)
        return obj

    @staticmethod
    def create_prop(obj, new_field, old_field, conversion):
        """
        Creates new field using old_field value
        :param obj:
        :param new_field:
        :param old_field:
        :param conversion:
        :return:
        """
        if old_field in obj:
            obj[new_field] = conversion(obj[old_field])
        return obj

    @staticmethod
    def delete_props(obj, fields):
        """
        Removes given fields from dict
        :param obj:
        :param fields:
        :return:
        """
        for p in fields:
            if p in obj:
                del obj[p]
        return obj