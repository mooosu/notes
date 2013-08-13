class Namespace(object):
    # namespace : handler class
    _registered_namespaces = {}
    @classmethod
    def get_registerd_namespaces(self):
        return self._registered_namespaces
    @classmethod
    def register(self,klass):
        namespace = klass.namespace
        if namespace in self._registered_namespaces:
            if self._registered_namespaces[namespace] != klass:
                raise "Conflict"
        else:
            self._registered_namespaces[namespace] = klass

    @classmethod
    def find(self,namespace):
        return self._registered_namespaces[namespace]

class SnmpObject(object):
    _objects = {}
    _indices = {}
    namespace = "SnmpObject"
    @classmethod
    def get_objects(self):
        return self._objects

    @classmethod
    def get_indices(self):
        return self._indices

    @classmethod
    def find(self,snmp_object_name):
        return self._objects[snmp_object_name]

    @classmethod
    def register(self,klass):
        name = klass.name
        if name in self._objects:
            if self._objects[name] != klass:
                raise "Conflict"
        else:
            self._objects[name] = klass
            self._indices[klass.index] = name
