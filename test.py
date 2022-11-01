from encryption import *
from decryption import *


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    str = 'cwkjc'.encode('utf-8')
    hex_str = str.hex()
    key = hex(int("30303030", 16))
    print(key)
    #key = bytes('30303030', encoding='utf-8').hex()
    enc_str = ecb_enc("plaintext.txt", key)
    ff = open("ciphertext1.txt", 'w')
    ff.write(enc_str.hex())
    ff.close()
    #print(len(enc_str.hex()), ' enc ', enc_str.hex())
    #print(len(hex_str), ' hex_str ', hex_str)
    dec_str = ecb_dec("ciphertext1.txt", key)
    print(len(dec_str.hex()), ' dec ', dec_str.hex())

    #print(bytes.fromhex(dec_str).decode('utf-8'))

