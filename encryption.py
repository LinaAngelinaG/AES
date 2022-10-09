from bitstring import BitArray

from block_cypher import cipher_block_enc, xor

block_length_bits = 32
block_length_bytes = block_length_bits // 8


def ecb_enc(plaintext, key):
    plain = bytearray.fromhex(plaintext)
    key = check_key(key)
    blocks_value, point = get_block_val(len(plain))
    result = bytearray()
    for i in range(blocks_value):
        res = plain[i * block_length_bytes:(i + 1) * block_length_bytes]
        res = cipher_block_enc(res, key)
        result.extend(res)
    if point == 1:
        last_block = work_last_block(plain[blocks_value * block_length_bytes:])
        last_block = cipher_block_enc(last_block, key)
        result.extend(last_block)
    return result


def check_key(key):
    if len(key.encode("utf8")) < block_length_bytes:
        return bytearray(key + bytearray(block_length_bytes-len(key.encode("utf8"))).hex())
    elif len(key.encode("utf8")) > block_length_bytes:
        return bytearray(key.encode("utf8")[:block_length_bytes])


def cbc_enc(plaintext, key, iv_vector):
    plain = bytearray.fromhex(plaintext)
    key = check_key(key)
    blocks_value, point = get_block_val(len(plain))
    result = bytearray()
    cur_iv = check_key(iv_vector)
    for i in range(blocks_value):
        cur_iv = xor(plain[i * block_length_bytes:(i + 1) * block_length_bytes], cur_iv)
        cur_iv = cipher_block_enc(cur_iv, key)
        result.extend(cur_iv)
    if point == 1:
        last_block = work_last_block(plain[blocks_value * block_length_bytes:])
        cur_iv = xor(last_block, cur_iv)
        cur_iv = cipher_block_enc(cur_iv, key)
        result.extend(cur_iv)
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
