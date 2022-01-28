from Crypto.Cipher import AES
from Crypto.Random import *
from Crypto.Util.Padding import pad, unpad
import time

class CTR():
    #init the class cbc with a random iv and a selected key 
    def __init__(self,key):
        self.key = key
        self.iv = get_random_bytes(16)
        self.cipher = AES.new(key,AES.MODE_ECB)

    #function to devide and encode a plaintext in blocs of 128bits
    def _devide_blocks_enc(self,a):
        a = a.encode()
        a = pad(a,16)
        plainbytes = list()
        for i in range(0,len(a),16):
            plainbytes.append(a[i:i+16])
        return plainbytes 

    #function to devide a ciphertext in blocs of 128bits
    def _devide_blocks_dec(self,a):
        plainbytes = list()
        for i in range(0,len(a),16):
            plainbytes.append(a[i:i+16])
        return plainbytes
    #fucntion to encrypt and decrypt CTR mode of aes with p as list of blocs
    # and iv the nonce that will be used
    def _ctr(self,p,iv):
        ciphertext = b''
        for byte in p:       
            cipherblock = self.cipher.encrypt(iv)
            xor = self._byte_xor(byte,cipherblock)
            ciphertext += xor
            btoi = int.from_bytes(iv, 'big')
            btoi += 1
            iv = btoi.to_bytes(len(iv), 'big')
        return ciphertext

    def _byte_xor(self, byte1, byte2):
        return bytes([x ^ y for x, y in zip(byte1,byte2)])

    def encrypt(self,message):
        table = self._devide_blocks_enc(message)
        return self._ctr(table,self.iv)
    def decrypt(self,message):
        table = self._devide_blocks_dec(message)
        return unpad(self._ctr(table,self.iv),16).decode()


def main():
    key = get_random_bytes(32)
    ctr = CTR(key)


    a = time.time()
    with open("plaintext.txt",'r') as plaintext,open("cipherctr.txt",'wb') as text:
        cipher = AES.new(key,AES.MODE_CTR)
        ciphertext = cipher.encrypt(plaintext.read().encode())
        text.write(ciphertext)
    print("CTR from  Crypto.Cipher, encryption time : {} sec".format(time.time()-a))    

    a = time.time()
    with open("cipherctr.txt",'rb') as plaintext,open("decipherctr.txt",'w') as text:
        cipher = AES.new(key,AES.MODE_CTR,nonce=cipher.nonce)
        cleartext = cipher.decrypt(plaintext.read()).decode()
        text.write(cleartext)
    print("CTR from  Crypto.Cipher, decryption time : {} sec".format(time.time()-a))    



    a = time.time()
    with open("./plaintext.txt",'r') as plaintext,open("./cipherctr.txt",'wb') as text:
        ciphertext = ctr.encrypt(plaintext.read())
        text.write(ciphertext)
    print("CTR from  My CTR , encryption time : {} sec".format(time.time()-a))   
    a = time.time()
    with open("./cipherctr.txt",'rb') as plaintext,open("./decipherctr.txt",'w') as text:
        cleartext = ctr.decrypt(plaintext.read())
        text.write(cleartext)
    print("CTR from  My CTR , encryption time : {} sec".format(time.time()-a))  


if __name__ == "__main__":
    main()
