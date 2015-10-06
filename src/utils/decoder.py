#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import datetime
import json


class ProfilerJSONDecoder (json.JSONDecoder):
    """Class overriding JSONDecoder which possess default python json decoding method.
    This class decodes given json string and converts values to proper type since everything is represented as string
    Basic conversion are:
        integer
        float
        datetime
    returned object has all values properly typed so
    formatters can make mathematical or other operation without worries
    """


    def decode (self, json_string):
        """Decodes json_string which is string that is given to json.loads method"""
        default_obj = super (ProfilerJSONDecoder, self).decode (json_string)

        self.intFields          = ["file-line", "call-count", "call-count-min", "call-count-max", "call-count-sum"]
        self.floatFields        = ["cumul-time", "cumul-time-min", "cumul-time-max", "cumul-time-sum", "percent", "run-duration"]
        self.intFieldsRoot      = ["task-size", "run-process-count"]
        self.floatFieldsRoot    = ["timer-resolution"]
        self.dateFields         = ["run-started-at", "run-finished-at"]


        self.convert_fields (default_obj, self.intFields, int)
        self.convert_fields (default_obj, self.floatFields, float)
        self.convert_fields (default_obj, self.intFieldsRoot, int, False)
        self.convert_fields (default_obj, self.floatFieldsRoot, float, False)
        self.convert_fields (default_obj, self.dateFields, self.parse_date, False)

        return default_obj


    def default_serializer (self, obj):
        """Default JSON serializer."""
        if isinstance (obj, datetime.datetime):
            return obj.strftime ("%m/%d/%y %H:%M:%S")
        return str (obj)

    def parse_date (self, str):
        """Default parsing method for date"""
        return datetime.datetime.strptime (str, "%m/%d/%y %H:%M:%S")

    def convert_fields (self, obj, fields, fun, rec=True):
        """Recursive value type conversion"""
        for field in fields:
            for prop in obj:
                if prop == field:
                    obj[prop] = fun (obj[prop])
        if rec:
            try:
                for child in obj["children"]:
                    self.convert_fields (child, fields, fun)
            except:
                pass