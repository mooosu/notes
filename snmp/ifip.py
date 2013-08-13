from ns import Namespace,SnmpObject

class IfMib(SnmpObject):
    namespace = "IF-MIB"

Namespace.register(IfMib)

class IfMibObject(object):
    def __init__(self,data):
        self.strs = []
        for key,v in data.items():
            setattr(self,key,v)
            self.strs.append("%s:%s" % ( key ,v ))

    def __repr__(self):
        return ','.join(self.strs) + "\n"
    @classmethod
    def register(self):
        IfMib.register(self)

    @classmethod
    def parse(self,data):
        indcies = []
        self.objects = []
        for i in data[self.index]:
            indcies.append(i)
        for i in indcies:
            pairs = {}
            for key in self.keys:
                pairs[key] = data[key].get(i,None)
            obj = self(pairs)
            self.objects.append(obj)

        return self.objects

class IfMibData(IfMibObject):
    name = "IfMib"
    index = "ifIndex"
    keys = ["ifDescr","ifType","ifMtu","ifSpeed","ifPhysAddress","ifAdminStatus","ifOperStatus","ifLastChange","ifInOctets","ifInUcastPkts","ifInNUcastPkts",
            "ifInDiscards","ifInErrors","ifInUnknownProtos","ifOutOctets","ifOutUcastPkts","ifOutNUcastPkts","ifOutDiscards","ifOutQLen","ifSpecific"]

IfMibData.register()
