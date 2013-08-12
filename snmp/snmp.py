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
