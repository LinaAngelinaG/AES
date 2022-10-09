from block_cypher import cipher_block_dec, xor
from encryption import check_key, get_block_val, work_last_block

block_length_bits = 32
block_length_bytes = block_length_bits // 8


def ecb_dec(plaintext, key):
    plain = bytearray(plaintext)
    blocks_value, point = get_block_val(len(plain))
    result = bytearray()
    key = check_key(key)
    for i in range(blocks_value):
        res = cipher_block_dec(plain[i * block_length_bytes:(i + 1) * block_length_bytes], key)
        result.extend(res)
    if point == 1:
        last_block = work_last_block(plain[blocks_value * block_length_bytes:])
        last_block = cipher_block_dec(last_block, key)
        result.extend(last_block)
    return result


def cbc_dec(plaintext, key, iv_vector):
    plain = bytearray(plaintext)
    blocks_value, point = get_block_val(len(plain))
    result = bytearray()
    key = check_key(key)
    cur_iv = check_key(iv_vector)
    for i in range(blocks_value):
        block = plain[i * block_length_bytes:(i + 1) * block_length_bytes]
        res = cipher_block_dec(block, key)
        res = xor(cur_iv, res)
        result.extend(res)
        cur_iv = block
    if point == 1:
        last_block = work_last_block(plain[blocks_value * block_length_bytes:])
        last_block = cipher_block_dec(last_block, key)
        last_block = xor(cur_iv, cipher_block_dec(last_block, key))
        result.extend(last_block)
    return result
