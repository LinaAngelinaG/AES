from block_cypher import cipher_block_dec, xor
from encryption import check_key, get_block_val, work_last_block, get_round_keys

block_length_bits = 32
block_length_bytes = block_length_bits // 8


def ecb_dec(plaintext, key):
    plaintext = open(plaintext, 'r', encoding='utf-8')
    plain = bytearray.fromhex(plaintext.readline())
    plaintext.close()
    blocks_value, point = get_block_val(len(plain))
    result = bytearray()
    key = check_key(key)
    round_key = get_round_keys(key)
    save = round_key[block_length_bytes:2*block_length_bytes]
    round_key[block_length_bytes:2*block_length_bytes] = round_key[2*block_length_bytes:]
    round_key[2 * block_length_bytes:] = save
    for i in range(blocks_value):
        res = cipher_block_dec(plain[i * block_length_bytes:(i + 1) * block_length_bytes], round_key)
        result.extend(res)
    if point == 1:
        last_block = work_last_block(plain[blocks_value * block_length_bytes:])
        last_block = cipher_block_dec(last_block, round_key)
        result.extend(last_block)
    print(result.hex())
    return result


def cbc_dec(plaintext, key, iv_vector):
    plaintext = open(plaintext, 'r', encoding='utf-8')
    plain = bytearray.fromhex(plaintext.readline())
    plaintext.close()
    blocks_value, point = get_block_val(len(plain))
    result = bytearray()
    key = check_key(key)
    round_key = get_round_keys(key)
    save = round_key[block_length_bytes:2 * block_length_bytes]
    round_key[block_length_bytes:2 * block_length_bytes] = round_key[2 * block_length_bytes:]
    round_key[2 * block_length_bytes:] = save
    cur_iv = check_key(iv_vector)
    for i in range(blocks_value):
        block = plain[i * block_length_bytes:(i + 1) * block_length_bytes]
        res = cipher_block_dec(block, round_key)
        res = xor(cur_iv, res)
        result.extend(res)
        cur_iv = block
    if point == 1:
        last_block = work_last_block(plain[blocks_value * block_length_bytes:])
        last_block = cipher_block_dec(last_block, round_key)
        last_block = xor(cur_iv, cipher_block_dec(last_block, round_key))
        result.extend(last_block)
    print(result.hex())
    return result.hex()
