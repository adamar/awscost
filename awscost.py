#!/usr/bin/env python
# -*- coding: utf-8 -*-


class AWSCosts(object):

    def _find_item_by_value(self, obj, key):
        ret = []

        def _recurse(obj):
            if isinstance(obj, dict):
                if key in obj.values():
                    ret.append(obj)
                for k, v in obj.iteritems():
                    _recurse(obj[k])
            elif isinstance(obj, list):
                for i in obj:
                    _recurse(i)

        _recurse(obj)

        return ret


    def _find_item_by_key(self, obj, key):
        ret = []

        def _recurse(obj):
            if isinstance(obj, dict):
                if key in obj:
                    ret.append(obj)
                for k, v in obj.iteritems():
                    _recurse(obj[k])
            elif isinstance(obj, list):
                for i in obj:
                    _recurse(i)

        _recurse(obj)

        return ret


    def _return_file_contents(self, filename):
        with open(filename, 'r') as content_file:
            return self._parse_to_json(content_file.read())


    def _parse_to_json(self, f):
        f = re.sub("/\\*[^\x00]+\\*/", "", f, 0, re.M)
        f = re.sub("([a-zA-Z0-9]+):", "\"\\1\":", f)
        f = re.sub(";", "\n", f)
        f = re.sub("callback\(", "", f)
        f = re.sub("\)$", "", f)
        data = json.loads(f)
        return data


    class CustomError(Exception):
        def __init__(self, arg):
            self.msg = arg

    class Ec2InstanceNotFound(Exception):
        def __init__(self, msg):
            self.msg = msg

    class RegionNotFound(Exception):
        def __init__(self, msg):
            self.msg = msg














