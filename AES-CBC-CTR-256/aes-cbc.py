from Crypto.Cipher import AES
from Crypto.Random import *
from Crypto.Util.Padding import pad, unpad
import time

class CBC():
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
    #encyrypt cbc mode with p as the list of all 128 btis blocs
    #and iv as the iv
    def _encryptcdb(self,p,iv):
        ciphertext = b''
        for byte in p:        
            xor = self._byte_xor(byte,iv)
            cipherblock = self.cipher.encrypt(xor)
            ciphertext += cipherblock
            iv = cipherblock
        return ciphertext
    #decrypt cbc mode with p as the list of all 128 btis blocs
    #and iv as the iv
    def _decryptcbc(self,p,iv):
        deciphertext = b''
        for i in p:
            decrypt = self.cipher.decrypt(i)
            xor = self._byte_xor(decrypt,iv)
            deciphertext += xor
            iv = i
        return unpad(deciphertext,16)
    # xor two bytes 
    def _byte_xor(self, byte1, byte2):
        return bytes([x ^ y for x, y in zip(byte1,byte2)])

    #devide and ecrypt a message
    def encrypt(self,message):
        table = self._devide_blocks_enc(message)
        return self._encryptcdb(table,self.iv)
    #devide and decrypt a message
    def decrypt(self,message):
        table = self._devide_blocks_dec(message)
        return self._decryptcbc(table,self.iv).decode()



# test  encryption :  encrypt the content of a file (plaintext.txt)  into another file (text.txt)
# test  decryption :  decrypt the content of a file (textt.txt)  into another file (textdecipher.txt)
def main():

    key = get_random_bytes(32)
    cbc = CBC(key)
    
    #test encryption /decyrption from pycryptodome
    a = time.time()
    with open("plaintext.txt",'r') as plaintext,open("ciphercbc.txt",'wb') as text:
        cipher = AES.new(key,AES.MODE_CBC,cbc.iv)
        ciphertext = cipher.encrypt(pad(plaintext.read().encode(),16))
        text.write(ciphertext)
    print("CBC from  Crypto.Cipher, encryption time : {} sec".format(time.time()-a))    

    a = time.time()
    with open("ciphercbc.txt",'rb') as plaintext,open("deciphercbc.txt",'w') as text:
        cipher = AES.new(key,AES.MODE_CBC,cbc.iv)
        ciphertext = unpad(cipher.decrypt(plaintext.read()),16).decode()
        text.write(ciphertext)
    print("CBC from  Crypto.Cipher, decryption time : {} sec".format(time.time()-a))    



    #test encryption /decyrption from the class above that I created

    a = time.time()
    with open("plaintext.txt",'r') as plaintext,open("ciphercbc.txt",'wb') as text:
        ciphertext = cbc.encrypt(plaintext.read())
        text.write(ciphertext)
    print("CBC from  my CBC with ECB, encryption time : {} sec".format(time.time()-a))    

    a = time.time()
    with open("ciphercbc.txt",'rb') as plaintext,open("deciphercbc.txt",'w') as text:
        cleartext = cbc.decrypt(plaintext.read())
        text.write(cleartext)
    print("CBC from  my CBC with ECB, decryption time : {} sec".format(time.time()-a))    

if __name__ == "__main__":
    main()

