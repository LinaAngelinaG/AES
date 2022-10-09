from encryption import *
from decryption import *


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    str = 'cwkjc'.encode('utf-8')
    hex_str = str.hex()
    key = bytes('fghj', encoding='utf-8').hex()
    enc_str = cbc_enc(hex_str, key, key)
    print(len(enc_str.hex()), ' enc ', enc_str.hex())
    print(len(hex_str), ' hex_str ', hex_str)
    dec_str = cbc_dec(enc_str, key, key)
    print(len(dec_str.hex()), ' dec ', dec_str.hex())
    #print(bytes.fromhex(dec_str).decode('utf-8'))
