import time
class RSA:
    def __init__(self,p,q,e):
        self.p = p
        self.q = q
        self.n = self.p * self.q
        self.w = (self.p-1)*(self.q-1)
        self.e = e
        self.d = self.modinv(self.e,self.w)
   
    #since python 3.8 pow can be useed to determine 
    def modexp(self,x,y,n):
        return pow(x,y,n)
    def modinv(self,x,n):
        return pow(x,(-1),n)

    def enc(self,m):
        return self.modexp(m,self.e,self.n) 
    def dec(self,c):
        return self.modexp(c,self.d,self.n)

text = "this is a text which needs to be encrypted with RSA "

p = 147513732454791286855894116408250922648769471923036927880790753919871952672308331279550605377807291710348597515184859660202801025967131853934063539004405289481737363292768134297535316056328161832744772210538303782101006513784097226420866643633546813327763529407492394840771466569824419814700456992846334731281
q = 150735041362626454417511646300711556141544472374851217978606636468341071806150452400352225218785400357093050355924724149364822513948644422533623676488140164031920481113890696128286021327454231109796167684696885749396571704094576432688322687991081472100194231663588044246927950986278951923846041547982212150073
e = 65537 

#init object
rsa = RSA(p,q,e)

#create int from text and encrypt it store l for decryption
t = time.time()
inttext = int.from_bytes(text.encode(),"big")
l = len(text.encode())
c = rsa.enc(inttext)
print(c)
print(f"encryption :{time.time() - t} sec")
#decryption
t = time.time()
m = rsa.dec(c)
decoded = str(m.to_bytes(m.bit_length()+7//8,"big").decode())
print(decoded)
print(f"decryption : {time.time() - t} sec")

def attack(c,n,e):
    cprime = (pow(2,e)*c)%n
    cprimedecypher = rsa.dec(cprime)
    return (cprimedecypher//2) % n

t = time.time()
at = attack(c,p*q,e)
print(str(at.to_bytes(at.bit_length()+7//8,"big").decode()))
print(f"attack : {time.time() - t} sec")
