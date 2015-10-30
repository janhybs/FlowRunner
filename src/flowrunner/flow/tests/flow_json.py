#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from flowrunner.utils.json_preprocessor import JsonPreprocessor


class FlowJson(JsonPreprocessor):
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
        json_report = FlowJson.convert_fields(json_report, int, FlowJson.int_props)
        json_report = FlowJson.convert_fields(json_report, float, FlowJson.float_props)
        # recursive fields
        json_report = FlowJson.convert_fields(json_report, int, FlowJson.int_recursive_props, True)
        json_report = FlowJson.convert_fields(json_report, float, FlowJson.float_recursive_props, True)
        json_report = FlowJson.create_prop(json_report, 'program-flags', 'program-build',
                                           lambda x: x.split()[x.split().index('flags:') + 1:])
        json_report = FlowJson.delete_props(json_report, FlowJson.del_props)

        return json_report
