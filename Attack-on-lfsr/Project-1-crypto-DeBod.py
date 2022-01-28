

import time

#see the report for a more expalined documentation

# xor bits in init 
def xor(init, bit_to_xor,):
    result = 0
    for i in bit_to_xor[:len(bit_to_xor)-1]:
        result ^= (init[bit_to_xor[-1]-i]) 
    return init + [result]

#compute lfsr for a lenght n 
def lfsr(poly,init,n):
    bit_to_xor = poly[::-1]
    bit_to_xor = [bit_to_xor[-1] -1 -x  for x in bit_to_xor]


    for i in range(0,n-poly[0]):
        init = xor(init,bit_to_xor)
        bit_to_xor = [x+1 for x in bit_to_xor]
        
    return init

#correlation between 2 list
def compare(a,keystream):
    count =0
    for i in range(0,min(len(a),len(keystream))):
        if a[i] == keystream[i]:
            count+=1
    return count

#setup the initial states and verfify correlatio 
def all_correlation(p,key):
    for i in range(1<<p[0]):
        s=bin(i)[2:]
        s='0'*(p[0]-len(s))+s
        init = [int(x) for x in list(s)]

        a = compare(lfsr(p,init,1024),key)

        if a > 650 :
            return [a,init]
        



#p = [22,1,0]
#p = [23,5,0]
p = [19,5,2,1,0]

start = time.time()

hexa = "0x00810535067310561CC3AD0121527C4E309504C81B3B044719333923E01B0F00FA041B99538D1541C15ADD1E0039088D3860185E82B6DE00A9AAFE986111137A7AF73C312525380FCF52170ACC3825D421BBF00924615D022831166DC2F2DFE4510C23D7B352B74FD53F4195E6202DE4692D821DD93F597BE829638AD719A970"
scale = 16  
res = bin(int(hexa, scale)).zfill(8)
key =  8*[0] + [int(x) for x in list(res)[2:]]
correct = all_correlation(p,key)
print("{} percent with {} and the inital state is {} ".format(correct[0]/1024,correct[0],correct[1]))
end = time.time()
print(f"Runtime of the program is {end - start}")

