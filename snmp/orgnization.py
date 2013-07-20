from node import Node
class Group(Node):
    def __init__(self,*args):
        super(Group,self).__init__(*args)
        self.device_units = []

    def add_device_unit(self,device_unit):
        self.device_units.append(device_unit)

    def get_device_units(self):
        return self.device_units

    def remove_device_unit(self,device_unit):
        pass


class Orgnization(Node):
    def __init__(self,*args):
        super(Orgnization,self).__init__(*args)
        self.groups = []


if __name__ == "__main__":
    o = Orgnization("/a/b/c","value")
    print o.get_path()
    print o.get_value()
