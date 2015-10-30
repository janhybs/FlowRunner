import json


class JsonPreprocessor(object):
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

    @staticmethod
    def filter(obj, field, bool_func):
        """
        Removes children if given field meets bool_func
        :type obj: dict
        :type field: str
        :type bool_func: function
        :return:
        """
        if type(obj) is dict:
            for name, values in obj.items():
                if bool_func(values.get(field, None)):
                    del obj[name]
        elif type(obj) is list:
            for item in obj:
                if bool_func(item.get(field, None)):
                    obj.remove(item)
        return obj
