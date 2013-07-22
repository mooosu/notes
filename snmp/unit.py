from node import Node
class Orgnization(Node):
    def __init__(self,*args):
        super(Orgnization,self).__init__(*args)


if __name__ == "__main__":
    o = Orgnization("node_id","myname","/a/b/c")
    print o.get_node_id()
    print o.get_name()
    print o.get_path()
