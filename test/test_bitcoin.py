import unittest
from bertocoin.__main__ import Bitcoin
from unittest.mock import MagicMock
import binascii


class Testing(unittest.TestCase):

    def test__private_key_from_passphrase(self):
        """
        Ensure that Bitcoin.__private_key_from_passphrase(<secret>)
        returns the sha256 of the given string secret
        """

        btc = Bitcoin('', '0123')

        string_a = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor'
                    ' incididunt ut labore et dolore magna aliqua.')
        hash_a = '973153f86ec2da1748e63f0cf85b89835b42f8ee8018c549868a1308a19f6ca3'
        self.assertEqual(btc._Bitcoin__private_key_from_passphrase(string_a), hash_a)

        string_b = ('Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut '
                    'aliquip ex ea commodo consequat.')
        hash_b = '37a770409eb4e1867ea7fe27168d38184350a31d6e1885cf456112f428e29dc8'
        self.assertEqual(btc._Bitcoin__private_key_from_passphrase(string_b), hash_b)

        string_c = 'cd372fb85148700fa88095e3492d3f9f5beb43e555e5ff26d95f5a6adc36f8e6'
        hash_c = 'e67e72111b363d80c8124d28193926000980e1211c7986cacbd26aacc5528d48'
        self.assertEqual(btc._Bitcoin__private_key_from_passphrase(string_c), hash_c)

        string_empty = ''
        hash_empty = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
        self.assertEqual(btc._Bitcoin__private_key_from_passphrase(string_empty), hash_empty)

    def test__b58encode(self):
        """
        Ensure b58 encoding from byte sequence works correctly. Remember that to ensure that leading zeros
        have an influence on the result, the bitcoin base58 encoding includes a manual step to convert
        all leading 0x00s to 1s.
        Online tool: https://appdevtools.com/base58-encoder-decoder
        """

        btc = Bitcoin('', '0123')

        input_a = bytes.fromhex('022cda0ce470147f840e3e0cfe3ff00c964e073015efc2ec31bfe48f5ebd86480b')
        b58_a = 'eUiXSRhqfqG2WEAJDG2LwhUTjjK6aqqpEd5gdCxhj2pJ'
        self.assertEqual(btc._Bitcoin__b58encode(input_a), b58_a)

        input_b = bytes.fromhex('031e7bcc70c72770dbb72fea022e8a6d07f814d2ebe4de9ae3f7af75bf706902a7')
        b58_b = 'vjwqCDKAkkz161wXytMc6moDo71L27yxNAdquUwvUfnN'
        self.assertEqual(btc._Bitcoin__b58encode(input_b), b58_b)

        # assert correct padding
        input_c = bytes.fromhex('00765d28b452bc80fdd6885b05c644e643bf89ba6451f62283')
        b58_c = '1BnrLSLhaZv1vTQ3z5yidteZ8CDfMJCXRL'
        self.assertEqual(btc._Bitcoin__b58encode(input_c), b58_c)

    def test__b58decode(self):
        """
        b58 encoding from byte sequence works correctly
        Online tool: https://appdevtools.com/base58-encoder-decoder
        """

        btc = Bitcoin('', '0123')

        b58_a = 'eUiXSRhqfqG2WEAJDG2LwhUTjjK6aqqpEd5gdCxhj2pJ'
        bytes_a = bytes.fromhex('022cda0ce470147f840e3e0cfe3ff00c964e073015efc2ec31bfe48f5ebd86480b')
        self.assertEqual(btc._Bitcoin__b58decode(b58_a), bytes_a)

        b58_b = 'vjwqCDKAkkz161wXytMc6moDo71L27yxNAdquUwvUfnN'
        bytes_b = bytes.fromhex('031e7bcc70c72770dbb72fea022e8a6d07f814d2ebe4de9ae3f7af75bf706902a7')
        self.assertEqual(btc._Bitcoin__b58decode(b58_b), bytes_b)

    def test_generate_coin(self):
        """
        Assert that the WIF and public address are correctly generated from the input secret
        It also makes sure the debug and non-debug mode work as expected
        """

        btc_1 = Bitcoin('60cf347dbc59d31c1358c8e5cf5e45b822ab85b79cb32a9f3d98184779a9efc2', '0123')
        WIF_1, public_address_b58_1 = btc_1.generate_coin(debug=True)
        self.assertEqual(WIF_1, '5JYvSurww2jTxmCeoN8T9QgRMWp45rre7WgFS76ae6Rgd1BnkC6')
        self.assertEqual(public_address_b58_1, '17JsmEygbbEUEpvt4PFtYaTeSqfb9ki1F1')

        btc_2 = Bitcoin('F273F81F4F7696F704964367815E4A641C5D80B468B1601F5EE6F2AB9F3A4188', '0123')
        WIF_2, public_address_b58_2 = btc_2.generate_coin(debug=True)
        self.assertEqual(WIF_2, '5Kf4ibycbXZQJPRFNprACLNn4i2WapFLXPq397ZYLSYKuic6cqH')
        self.assertEqual(public_address_b58_2, '1GB79Up5834H5GYMunBhMRxUxgz7rF82FT')

        btc_3 = Bitcoin('f273f81f4f7696f704964367815e4a641c5d80b468b1601f5ee6f2ab9f3a4188', '0123')
        WIF_3, public_address_b58_3 = btc_3.generate_coin(debug=True)
        self.assertEqual(WIF_3, '5Kf4ibycbXZQJPRFNprACLNn4i2WapFLXPq397ZYLSYKuic6cqH')
        self.assertEqual(public_address_b58_3, '1GB79Up5834H5GYMunBhMRxUxgz7rF82FT')

        btc_4 = Bitcoin('D46M9vCkKHHhiFsHK1-MC2G8O9Y4UCemx2U9sFPljy/)rlg-nFT5IH64l3uldFXb', '1234')
        WIF_4, public_address_b58_4 = btc_4.generate_coin(debug=False)
        self.assertEqual(WIF_4, '5J3btiKckkMpV9Ttm4epAt7Z8U3L8k3S8VsQm1rizSQ6DxE5gLi')
        self.assertEqual(public_address_b58_4, '1BnrLSLhaZv1vTQ3z5yidteZ8CDfMJCXRL')

        btc_5 = Bitcoin('D46M9vCkKHHhiFsHK1-MC2G8O9Y4UCemx2U9sFPljy/)rlg-nFT5IH64l3uldFXb', '1234')
        private_key_hex = '1e3c24dea238b9cfb8b14468709394d6cde24a51771ba5e85643afe8664410f7'
        btc_5._Bitcoin__private_key_from_passphrase = MagicMock(return_value=private_key_hex)
        WIF_5, public_address_b58_5 = btc_5.generate_coin(debug=False)

        self.assertEqual(WIF_5, '5J3btiKckkMpV9Ttm4epAt7Z8U3L8k3S8VsQm1rizSQ6DxE5gLi')
        self.assertEqual(public_address_b58_5, '1BnrLSLhaZv1vTQ3z5yidteZ8CDfMJCXRL')
        btc_5._Bitcoin__private_key_from_passphrase.assert_called_with(
            'Coin_1234_D46M9vCkKHHhiFsHK1-MC2G8O9Y4UCemx2U9sFPljy/)rlg-nFT5IH64l3uldFXb'
        )

    def test__ripemd160(self):
        """
        ripemd160 correctly hashed binary input and outputs hash in bin too
        Online tool: https://hash.rfctools.com/ripemd160-hash-generator/
        """

        btc = Bitcoin('', '0123')

        input_a = '973153f86ec2da1748e63f0cf85b89835b42f8ee8018c549868a1308a19f6ca3'.encode('utf-8')
        ripemd_a = b'0ef9258f3cde3a50ddc768f8a1c5041dd4b5c459'
        self.assertEqual(binascii.hexlify(btc._Bitcoin__ripemd160(input_a)), ripemd_a)

        input_b = '37a770409eb4e1867ea7fe27168d38184350a31d6e1885cf456112f428e29dc8'.encode('utf-8')
        ripemd_b = b'33fdaca3beeba39d2ac18cecb543bf065c938432'
        self.assertEqual(binascii.hexlify(btc._Bitcoin__ripemd160(input_b)), ripemd_b)

        input_c = 'e67e72111b363d80c8124d28193926000980e1211c7986cacbd26aacc5528d48'.encode('utf-8')
        ripemd_c = b'71b1f6bfc5c99903d443be2bd6d1c8e2ec979d85'
        self.assertEqual(binascii.hexlify(btc._Bitcoin__ripemd160(input_c)), ripemd_c)

        input_empty = ''.encode('utf-8')
        ripemd_empty = b'9c1185a5c5e9fc54612808977ee8f548b2258d31'
        self.assertEqual(binascii.hexlify(btc._Bitcoin__ripemd160(input_empty)), ripemd_empty)

    def test__hex_to_byte(self):
        """
        Hex strings are properly converted to bytes
        """

        btc = Bitcoin('', '0123')

        input_a = '60cf347dbc59d31c1358c8e5cf5e45b822ab85b79cb32a9f3d98184779a9efc2'
        bytes_a = bytes.fromhex('60cf347dbc59d31c1358c8e5cf5e45b822ab85b79cb32a9f3d98184779a9efc2')
        self.assertEqual(btc._Bitcoin__hex_to_byte(input_a), bytes_a)

        input_b = 'f273f81f4f7696f704964367815e4a641c5d80b468b1601f5ee6f2ab9f3a4188'
        bytes_b = bytes.fromhex('f273f81f4f7696f704964367815e4a641c5d80b468b1601f5ee6f2ab9f3a4188')
        self.assertEqual(btc._Bitcoin__hex_to_byte(input_b), bytes_b)


if __name__ == '__main__':
    unittest.main()
