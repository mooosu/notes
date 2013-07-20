class Node(object):
    def __init__(self,path,value):
        self.path = path
        self.value = value

    def get_path(self):
        return self.path

    def set_path(self,path):
        return self.path

    def get_value(self):
        return self.value

    def set_value(self,value):
        self.value = value
