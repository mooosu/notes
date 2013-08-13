import os
import sys
from snmp import SnmpDataParser

f = open(sys.argv[1])
def parse(data_in):
    namespaces = {}
    prev_namespace = None
    for line in data_in:
        fields = line.split("::",1)
        if len(fields) == 2:
            namespace,value = fields
            if prev_namespace != namespace:
                prev_namespace = namespace
                namespaces[namespace] = {}
            data = namespaces[namespace]
            # ifMtu.1  16436
            #    k       v
            # IF-MIB::ifMtu.1 16436
            # namespace key_name key_index value
            tmp = value.strip().split(' ',1)
            k , v = tmp if len( tmp ) == 2 else (tmp[0] , None)
            key_name,key_index = k.split('.',1)
            key_data = data[key_name]={} if key_name not in data else data[key_name]
            if key_index not in key_data:
                key_data[key_index] = v
    return namespaces

import sys
import pdb;pdb.set_trace()
print SnmpDataParser().parse(open(sys.argv[1]))
