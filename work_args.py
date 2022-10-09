import os.path
import pathlib
import decryption
import encryption
import argparse as args


def work_args():
    parser = args.ArgumentParser()

    parser.add_argument("--enc", default=False, type=bool)
    parser.add_argument("--dec", default=False, type=bool)
    parser.add_argument("--filename", type=str)
    parser.add_argument("--mode", default='ecb', type=str)
    parser.add_argument("--key", type=str)
    parser.add_argument("--iv", default=None, type=str)

    all_args = parser.parse_args()

    enc = all_args.enc
    dec = all_args.dec
    filename = all_args.filename
    mode = all_args.mode
    key = all_args.key
    iv = all_args.iv

    if enc:
        if mode.__eq__('ecb'):
            encryption.ecb_enc(filename, key)
        elif mode.__eq__('cbc') and iv is not None:
            encryption.cbc_enc(filename, key, iv)
        else:
            raise IOError("Need iv value")
    elif dec:
        if mode.__eq__('ecb'):
            decryption.ecb_dec(filename, key)
        elif mode.__eq__('cbc') and iv is not None:
            decryption.cbc_dec(filename, key, iv)
    else:
        raise IOError("Invalid value of function - should chose encryption ir decryption")
