from gevent import Greenlet
def myfunction(arg1,arg2,kwarg1=2):
    print arg1,arg1,kwarg1
g = Greenlet.spawn(myfunction, 'arg1', 'arg2', kwarg1=1)
g1 = Greenlet.spawn(myfunction, 'arg1', 'arg2')
g1.join
g.join()

