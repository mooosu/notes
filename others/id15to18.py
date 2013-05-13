def idtrans(idcard_input):
 idlist = list(idcard_input)
 idlist.insert(6,"1")
 idlist.insert(7,"9")
 wi = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
 ai = {"0":"1","1":"0","2":"X","3":"9","4":"8","5":"7","6":"6","7":"5","8":"4","9":"3","10":"2"}
 last_num = ai[str(reduce((lambda x,y:x+y),map(lambda x,y:int(x)*y,idlist,wi))%11)]
 idlist.append(last_num)
 return reduce((lambda x,y:x+y),idlist)
####################


def generate_verify_code(id_head):
   weight_list = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1 ]
   code = 0
   for i in [0,16]:
      code = code + int(id_head[i]) * weight_list[i]
   code = code % 11

   verify_code = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
   return verify_code[code]

idno = ""
ret = idtrans(idno)
print ret
print generate_verify_code(ret)
