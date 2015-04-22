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




