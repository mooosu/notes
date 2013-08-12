import host_resource
from ns import Namespace
class SnmpDataParser(object):
    def __init__(self):
        pass
    def load_file(self,filename):
        namespaces = self.parse_file(filename)
        for k,v in namespaces.items():
            ns = Namespace.find(k)
            values = namespaces[k]
            for index,v in ns._indices.items():
                if index in values:
                    klass = ns._registered_objects[v]
                    print klass.parse(values)

    def parse_file(self,filename):
        f = open(filename)
        namespaces = self.parse(f)
        f.close()
        return namespaces

    def parse(self,data_in):
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
                k , v = value.split(' ',1)
                key_name,key_index = k.split('.',1)
                if key_name not in data:
                    data[key_name] = {}
                key_data = data[key_name]

                if key_index not in key_data:
                    key_data[key_index] = v.strip()
        return namespaces
import sys
SnmpDataParser().load_file(sys.argv[1])
