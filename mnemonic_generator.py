import sys
from mnemonic import Mnemonic
import bip32utils
import hashlib
import ecdsa

def generate_mnemonic(language="english", words=12):
    if words not in [12, 24]:
        raise ValueError("Only 12 or 24 word mnemonics supported.")
    mnemo = Mnemonic(language)
    strength = 128 if words == 12 else 256
    return mnemo.generate(strength=strength)

def derive_eth_address(seed):
    from hashlib import sha3_256
    mnemo = Mnemonic("english")
    seed_bytes = mnemo.to_seed(seed, passphrase="")

    # Derive Ethereum address from BIP44 path m/44'/60'/0'/0/0
    bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed_bytes)
    child_key = bip32_root_key_obj.ChildKey(44 + bip32utils.BIP32_HARDEN)\
                                   .ChildKey(60 + bip32utils.BIP32_HARDEN)\
                                   .ChildKey(0 + bip32utils.BIP32_HARDEN)\
                                   .ChildKey(0).ChildKey(0)

    privkey = child_key.PrivateKey()
    sk = ecdsa.SigningKey.from_string(privkey, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    pub_key = b'\x04' + vk.to_string()
    keccak_hash = sha3_256(pub_key[1:]).digest()
    address = '0x' + keccak_hash[-20:].hex()
    return address

def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    for i in range(count):
        mnemonic = generate_mnemonic(words=12)
        print(f"\n🔑 Mnemonic #{i+1}:")
        print(mnemonic)
        print(f"🪪 ETH Address: {derive_eth_address(mnemonic)}")

if __name__ == "__main__":
    main()
