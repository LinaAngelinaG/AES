from s_box import s_box
from inv_s_box import inv_s_box

rounds_value = 2
block_length_bytes = 4


def make_one_round_enc(new_word, round_key):
    # Shift bits in rows
    save = new_word[block_length_bytes - 2]
    new_word[block_length_bytes - 2] = new_word[block_length_bytes - 1]
    new_word[block_length_bytes - 1] = save
    new_word = xor(new_word, round_key)
    return new_word


def make_one_round_dec(new_word, round_key):
    # Shift bits in rows
    new_word = xor(new_word, round_key)
    save = new_word[block_length_bytes - 2]
    new_word[block_length_bytes - 2] = new_word[block_length_bytes - 1]
    new_word[block_length_bytes - 1] = save
    return new_word


def shift_bytes_with_inv_s_box(block):
    new_word = bytearray(block_length_bytes)
    for i in range(block_length_bytes):
        new_word[i] = inv_s_box[block[i]]
    return new_word


def shift_bytes_with_s_box(block):
    new_word = bytearray(block_length_bytes)
    for i in range(block_length_bytes):
        new_word[i] = s_box[block[i]]
    return new_word


def cipher_block_enc(plain_text_block, key):
    block = xor(key, plain_text_block)
    round_key = bytearray(2 * block_length_bytes)
    for i in range(block_length_bytes):
        round_key[i] = 255 - key[i]
        round_key[i + block_length_bytes] = key[i] ^ round_key[i]
    for i in range(rounds_value):
        block = shift_bytes_with_s_box(block)  # SubBytes with s-box
        block = make_one_round_enc(block, round_key[i * block_length_bytes:(i + 1) * block_length_bytes])
    return block


def xor(key, block):
    res = bytearray(block_length_bytes)
    for i in range(block_length_bytes):
        res[i] = key[i] ^ block[i]
    return res


def cipher_block_dec(plain_text_block, key):
    block = plain_text_block
    round_key = bytearray(2 * block_length_bytes)
    for i in range(block_length_bytes):
        round_key[i + block_length_bytes] = 255 - key[i]
        round_key[i] = key[i] ^ round_key[i + block_length_bytes]
    for i in range(rounds_value):
        block = make_one_round_dec(block, round_key[i * block_length_bytes:(i + 1) * block_length_bytes])
        block = shift_bytes_with_inv_s_box(block)  # SubBytes with s-box
    block = xor(key, block)
    return block
