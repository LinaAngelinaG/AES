from block_cypher import cipher_block_enc, xor
from bitstring import BitArray

block_length_bits = 32
block_length_bytes = block_length_bits // 8


def ecb_enc(plaintext, key):
    plaintext = open(plaintext, 'r', encoding='utf-8')
    plain = bytearray.fromhex(plaintext.readline())
    plaintext.close()
    key = check_key(key)
    blocks_value, point = get_block_val(len(plain))
    result = bytearray()
    round_key = get_round_keys(key)
    for i in range(blocks_value):
        res = plain[i * block_length_bytes:(i + 1) * block_length_bytes]
        res = cipher_block_enc(res, round_key)
        result.extend(res)
    if point == 1:
        last_block = work_last_block(plain[blocks_value * block_length_bytes:])
        last_block = cipher_block_enc(last_block, round_key)
        result.extend(last_block)
    print(result.hex())
    return result


def get_round_keys(key):
    round_key = bytearray(3 * block_length_bytes)
    round_key[:block_length_bytes] = key
    round_key[block_length_bytes:2 * block_length_bytes] = bytearray.fromhex(inv(key.hex()))
    for i in range(block_length_bytes):
        round_key[i + 2 * block_length_bytes] = key[i] ^ round_key[i + block_length_bytes]
    return round_key


def inv(vec):
    res = BitArray(hex=vec)
    last = len(res) - 1
    first = 0
    while last > first:
        save = res[last]
        res[last] = res[first]
        res[first] = save
        last = last - 1
        first = first + 1
    return res.hex.replace('0x', '')


def check_key(key):
    key = key.replace('0x', '')
    if len(key.encode("utf8"))//2 < block_length_bytes:
        return bytearray(key + bytearray(block_length_bytes - len(key.encode("utf8"))).hex())
    elif len(key.encode("utf8"))//2 > block_length_bytes:
        return bytearray(key.encode("utf8")[:block_length_bytes])
    else:
        return bytearray.fromhex(key)


def cbc_enc(plaintext, key, iv_vector):
    plaintext = open(plaintext, 'r', encoding='utf-8')
    plain = bytearray.fromhex(plaintext.readline())
    plaintext.close()
    key = check_key(key)
    blocks_value, point = get_block_val(len(plain))
    result = bytearray()
    round_key = get_round_keys(key)
    cur_iv = check_key(iv_vector)
    for i in range(blocks_value):
        cur_iv = xor(plain[i * block_length_bytes:(i + 1) * block_length_bytes], cur_iv)
        cur_iv = cipher_block_enc(cur_iv, round_key)
        result.extend(cur_iv)
    if point == 1:
        last_block = work_last_block(plain[blocks_value * block_length_bytes:])
        cur_iv = xor(last_block, cur_iv)
        cur_iv = cipher_block_enc(cur_iv, round_key)
        result.extend(cur_iv)
    print(result.hex())
    return result


def get_block_val(length):
    blocks_value = length // block_length_bytes
    if length % block_length_bytes != 0:
        return blocks_value, 1
        # УЛС и аппаратные средства
    return blocks_value, 0


def work_last_block(last_block):
    i = block_length_bytes - len(last_block)
    return last_block + bytearray(i)
