import os

f = open("data/system.txt")
def parse(data_in):
    namespaces = {}
    prev_namespace = None
    import pdb;pdb.set_trace()
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
print parse(f)
