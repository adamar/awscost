#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import sys


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

    class Ec2InstanceTypeNotFound(Exception):
        def __init__(self, msg):
            self.msg = msg

    class RegionNotFound(Exception):
        def __init__(self, msg):
            self.msg = msg

    class ProductDescriptionNotFound(Exception):
        def __init__(self, msg):
            self.msg = msg



class EC2(AWSCosts):


    def __init__(self):

        self.on_demand_instance_map = {
                'Linux/UNIX': 'json/ec2/linux-od.min.js',
                'SUSE Linux': 'sles-od.min.js',
                'Red Hat Linux': 'rhel-od.min.js',
                'Windows': 'mswin-od.min.js',
                'Windows with SQL Standard': 'mswinSQL-od.min.js',
                'Windows with SQL Web': 'mswinSQLWeb-od.min.js'
                }
        self.reserved_instance_map = {
                'Linux/UNIX': 'linux-unix-shared.min.js',
                'SUSE Linux': 'suse-linux-shared.min.js',
                'Red Hat Linux': 'red-hat-enterprise-linux-shared.min.js',
                'Windows': 'windows-shared.min.js',
                'Windows with SQL Standard': 'windows-with-sql-server-standard-shared.min.js',
                'Windows with SQL Web': 'windows-with-sql-server-web-shared.min.js'
                }
           


    def get_on_demand_instance_price(self, region=None,
                                     instance_type=None, 
                                     product_description=None):

        """
        Retreieve the current per hour cost 
        of a specified instance type

        :param region:
           The region in which the instance is running

        :param instance_type:
           The instance size

        :param product_description:
           The OS type of the instance


        """

        self.region = region
        self.instance_type = instance_type
        self.product_description = product_description

        if self.product_description not in self.on_demand_instance_map:
            raise self.ProductDescriptionNotFound('Product Description not found')
        self.file_name = self.on_demand_instance_map[self.product_description]
        self.prices = self._return_file_contents(self.file_name)

        self.region_data = self._find_item_by_value(self.prices, self.region)
        if len(self.region_data) < 1:
            raise self.RegionNotFound('Region not found')

        self.ret = self._find_item_by_value(self.region_data, self.instance_type)
        if len(self.ret) < 1:
            raise self.Ec2InstanceTypeNotFound('Instance type not found')
        else:
            return self.ret[0]



    def get_reserved_instance_price(self, instance_type=None,
                                    product_description=None,
                                    offering_type=None):
        """
        Retreieve the current per hour cost 
        of a specified Reserved instance type

        :param region:
           The region in which the instance is running

        :param instance_type:
           The instance size

        :param product_description:
           The OS type of the instance

        :param offering_type:
           The reservation type


        """
        pass



