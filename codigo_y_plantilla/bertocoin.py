# -*- coding: utf-8 -*-
# !/usr/bin/env python
# /Library/Python/2.7/site-packages (0.0.2)
# pip install ecdsa
# Alberto Femenías Hermida
#
# Basado en parte en código tomado de:
#
#  https://codereview.stackexchange.com/questions/185106/bitcoin-wallet-address-and-private-key-generator
#  http://code.activestate.com/recipes/510399-byte-to-hex-and-hex-to-byte-string-conversion/
#  https://github.com/HelloZeroNet/ZeroNet/blob/master/src/lib/BitcoinECC/newBitcoinECC.py

import argparse, os, sys, binascii, hashlib, ecdsa, pyqrcode, time, shutil


class Bitcoin:

    DEBUG = False

    TEMP_FOLDER = "delete-me"
    TEMPLATE_INPUT_FILENAME = "bertocoin.svg"
    TEMPLATE_OUTPUT_FILENAME = "print-me.svg"

    TEMPLATE_OUTPUT_PATHNAME = os.path.join(TEMP_FOLDER, TEMPLATE_OUTPUT_FILENAME)
    PRIVATE_QR_PATHNAME = os.path.join(TEMP_FOLDER, "coin_private_qr.png")
    PUBLIC_QR_PATHNAME = os.path.join(TEMP_FOLDER, "coin_public_qr.png")

    def __init__(self, secret_seed, debug=DEBUG):
        self.secret = secret_seed
        self.debug = debug

    @staticmethod
    def progress_bar(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
        """
        Source: https://gist.github.com/aubricus/f91fb55dc6ba5557fbab06119420dd6a

        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            bar_length  - Optional  : character length of bar (Int)
        """
        str_format = "{0:." + str(decimals) + "f}"
        percents = str_format.format(100 * (iteration / float(total)))
        filled_length = int(round(bar_length * iteration / float(total)))
        bar = '█' * filled_length + '-' * (bar_length - filled_length)

        sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

        if iteration == total:
            sys.stdout.write('\n')
        sys.stdout.flush()

    @staticmethod
    def delayed_type(my_text, delay = 0.1, newline = True):
        """
        Send characters to console, one by one, simulating manual typing

        @params:
            my_text     - Required  : Text to send (Str)
            delay       - Optional  : Delay between keystrokes (Float)

        """

        my_text = my_text + " "
        for i in range(len(my_text)):
            partial = my_text[0:i]

            # sys.stdout.write('\r%s' % partial),
            sys.stdout.write('\r{}'.format(partial)),
            sys.stdout.flush()
            time.sleep(delay)

        if newline: sys.stdout.write('\n')
        sys.stdout.flush()

    @classmethod
    def show_instructions(cls):

        BLUE = '\033[94m'
        END_COLOR = '\033[0m'
        RED = '\033[31m'


        cls.delayed_type("INSTRUCTIONS")
        cls.delayed_type("------------")
        print
        print
        cls.delayed_type("1.- Navigate to this folder:", newline=False )
        print
        print
        cls.delayed_type("    {}{}/{}{} ".format(BLUE, os.path.abspath(os.getcwd()), Bitcoin.TEMP_FOLDER, END_COLOR),delay=0.005)
        print
        cls.delayed_type("2.- Use your browser (Safari, Chrome, ...) to open this file: ")
        print
        cls.delayed_type("    {}{}{} ".format( BLUE, Bitcoin.TEMPLATE_OUTPUT_FILENAME, END_COLOR),delay=0.005)
        print
        cls.delayed_type("3.- Print it on good-quality paper")
        print
        cls.delayed_type("4.- Follow the instructions provided in the template you just printed")
        print


        print
        print
        cls.delayed_type(RED + "WARNING:" + END_COLOR)
        cls.delayed_type("--------")

        time_limit = cls.command_line_arguments().timeout
        cls.delayed_type('You only have {} seconds to print the template.'.format(time_limit))
        cls.delayed_type('After that, all the files in the folder:')

        cls.delayed_type("    {}{}/{}{} ".format(BLUE, os.path.abspath(os.getcwd()), Bitcoin.TEMP_FOLDER, END_COLOR),delay=0.005)

        cls.delayed_type('will be deleted, to protect the security of your coin.\n')
        cls.delayed_type('If the self-destroy process does not finish properly, ')
        cls.delayed_type('please delete the contents of that folder manually.')
        print

        for i in range(time_limit):
            # Do stuff...
            time.sleep(1)
            # Update Progress Bar
            cls.progress_bar(i + 1,
                             args.timeout,
                             prefix='Self destroy timer:',
                             suffix='({} seconds left.)'.format(args.timeout - i),
                             bar_length=50)


    @staticmethod
    def private_key_from_passphrase(src):
        """
        Given a passphrase <src> it returns a private key obtained by hashing it 
        :param src: The passphrase to convert   
        :return: A hex string with the sha256() hash digest of the given passphrase
        """
        privatekey = hashlib.sha256(src).hexdigest()
        return str(privatekey)

    @staticmethod
    def ripemd160(v):
        """
        Given a sequence of bytes <v> it returns its RIPEMD160 hash object
        :param v: The sequence of bytes whose hash we want to obtain
        :return: A hash object, that uses the RIPEME160 algorithm
        """
        d = hashlib.new('ripemd160')
        d.update(v)

        return d

    @staticmethod
    def similar_splits(s, n):
        """
        Given a string <s> it splits it into <n> 'almost' equal elements.
        If the splits can not be made equal, the excess is added to the first elements.

        :param s: The string to divide
        :param n: Number of splits
        :return: A list with the <n> splits
        """

        if n > len(s):
            err_msg = "{} equal splits requested, when a string of length {} was provided.".format(n, len(s))
            raise Exception(err_msg)

        remainder = len(s) % n
        part_size = (len(s) - remainder)/ n
        excess = remainder

        start = 0
        ret = []
        for i in range(n):
            delta = 1 if excess > 0 else 0
            excess -= 1
            chunk = s[start:start + part_size + delta]
            ret.append(chunk)
            start = start + part_size + delta

        sanity_check = "".join(ret)
        if not sanity_check == s:
            exception_msg = "Unexpected error, splits don't add up to the whole string.\n <{}> != <{}>".format(s, sanity_check)
            raise Exception(exception_msg)

        return ret


    @classmethod
    def create_temp_folder(cls):
        """
        Utility method. It creates a temp folder to place the temporary files used to generate the
        printable template.
        :return: Nothing.
        """
        dir_name = cls.TEMP_FOLDER
        # Create target Directory if it doesn't exist
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

    @classmethod
    def destroy_temp_folder(cls):
        """
        Utility method. It deletes the temp folder that was used to generate the printable template
        printable template.
        :return: Nothing.
        """
        dir_name = cls.TEMP_FOLDER
        # Destroy target Directory

        print
        print("Destroying temporary folder... {}".format(cls.TEMP_FOLDER))
        print
        if os.path.exists(dir_name):
            try:
                shutil.rmtree('{}'.format(cls.TEMP_FOLDER))
                # os.rmdir(dir_name)
                print("Done")
                print
            except:
                print("WARNING !!!")
                print("  I couldn't delete this folder and its associated files: {}.".format(cls.TEMP_FOLDER))
                print("  Please remove it MANUALLY.")

    @classmethod
    def replace_template_variable(cls, line, template_var, expanded_value):
        """
        It searches and replaces a substring <template_var> within a string <line>.
        Used to replace a variable, like '::serial::' inside the SVG template.
        :param line: A line of text within the template
        :param template_var: The literal we are looking for, e.g.: '::serial::'
        :param expanded_value: The value to replace it with, e.g.: '0007'
        :return: The line with the value replaced, if found.
        """
        ret = line
        if line.find(template_var) >= 0:
            if cls.DEBUG: print('Found ', template_var)
            ret = line.replace(template_var, expanded_value)
        return ret

    @classmethod
    def process_template(cls, coin_info):
        """
        It creates the file <cls.TEMPLATE_OUTPUT_PATHNAME> by replacing the variables inside the template
        file <cls.TEMPLATE_INPUT_FILENAME> with their respective values.
        
        Expected variables are:

        ::serial::      -> The serial number that will be printed in the coin, e.g.: <0021>
        ::f::           -> The fraction of bitcoin that will be stored in the coin. e.g.:  1:1000
        ::address.00x:: -> The address where the bitcoins will be placed.
                           e.g.: 5JgMaYD8yxft8SLQAj7Rme1pCGcQQ5Ce5VmhpijrARwwUYnBPDF
                           There are 3 fields in the template, each of which will be replaced with a fragment of
                           the address, like in:

                           ::address.001:: -> 1Mjm3C1gSScY
                           ::address.002:: -> xi9WRPCdVCMe
                           ::address.003:: -> KYUgLcCHEK

        :param coin_info: A dictionary containing the relevant info.
                          It has these keys:

                            "serial"        ->  A string containing the serial number, preformatted, e.g. '0021'
                            "numerator"     ->  The numerator of the fraction that represents the value of the coin.
                                                E.g.: 1
                            "denominator"   ->  The denominator of the fraction that represents the value of the coin.
                                                E.g.: 1000

                            "address"       ->  A string that contains the address where the value of the coin will
                                                be stored; represented in Base58check format
                            "WIF"           ->  A string that contains the private key used to unlock the funds of
                                                the coin, as a WIF string.

        """
        template_input = open(cls.TEMPLATE_INPUT_FILENAME, 'r')
        template_lines = template_input.readlines()

        cls.create_temp_folder()
        template_output = open(cls.TEMPLATE_OUTPUT_PATHNAME, 'w')
        counter = 0
        serial = coin_info["serial"]
        wif = cls.similar_splits(coin_info["WIF"], 3)

        address = cls.similar_splits(coin_info["address"], 3)

        numerator = coin_info["numerator"]
        denominator = coin_info["denominator"]

        for line in template_lines:

            counter += 1

            # Replace ::serial::
            line = cls.replace_template_variable(line, '::serial::', serial)

            # Replace ::f::
            line = cls.replace_template_variable(line, '::f::', '{}:{}'.format(numerator, denominator))

            # Replace ::address.XX::
            for i in range(0, 3):
                line = cls.replace_template_variable(line,
                                                     '::address.000{}::'.format(i + 1),
                                                     address[i])

            # Replace ::secret.XX::
            for i in range(0, 3):
                line = cls.replace_template_variable(line,
                                                     '::secret.000{}::'.format(i + 1),
                                                     wif[i])

            template_output.writelines(line)

        template_output.close()
        template_input.close()

    @staticmethod
    def b58encode(v):
        """
        Given a byte string <v>, it returns a string that represents this value in Base58 format.
        :param v -> The sequence of bytes encode
        :return: A string in format Base58 representing the value of v
        """

        digit = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        base = len(digit)
        val = 0
        for c in v:
            val *= 256
            val += ord(c)

        result = ""
        while val:
            (val, mod) = divmod(val, base)
            result = digit[mod] + result

        pad = 0
        for c in v:
            if c == "\x00":
                pad += 1
            else:
                break

        ret = (digit[0] * pad) + result

        return ret

    @staticmethod
    def b58decode(v):
        """
        Decode a Base58 <v> string to byte string
        :param v -> The string in Base58 format
        :return: A sequence of bytes corresponding to the input string
        """
        # Decode a Base58 string to byte string
        digit = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        base = len(digit)
        val = 0
        for c in v:
            val *= base
            val += digit.find(c)

        result = ""
        while val:
            (val, mod) = divmod(val, 256)
            result = chr(mod) + result

        pad = 0
        for c in v:
            if c == digit[0]:
                pad += 1
            else:
                break

        return "\x00" * pad + result

    @staticmethod
    def HexToByte(hexStr):
        """
        Convert a string hex byte values into a byte string. The Hex Byte values may
        or may not be space separated.

        :param hexStr: A string of hex bytes values
        :return: A byte string with the hex values converted.
        """

        bytes = []

        hexStr = ''.join(hexStr.split(" "))

        for i in range(0, len(hexStr), 2):
            bytes.append(chr(int(hexStr[i:i + 2], 16)))

        return ''.join(bytes)

    @staticmethod
    def secure_random_passphrase(length=64,
                                 charset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@()./+-"):
        """
        It returns a random string of length <length> using characters taken from <charset>
        :param length:  Size of the generated string.
        :param charset: String that contains characters that will be used to create the result
        :return:        A random string created with the parameters given and formed using the best source of
                        randomness provided by the host operating system -> os.urandom()
        """

        random_bytes = os.urandom(length)
        indices = [ord(byte) % len(charset) for byte in random_bytes]
        return "".join([charset[i] for i in indices])

    @staticmethod
    def passphrase_is_robust(passphrase):
        """
        Given a passphrase, it performs a series of checks to determine if it is robust enough to be used
        as a seed to generate the private key of the coin.

        :param      passphrase: A secret string of characters
        :return:    True or False, depending on the robustness of the given password
        """

        MINIMUM_STRENGTH = 2 ** 128
        MINIMUM_ENTROPY_SET_SIZE = 32

        symbols = set(list(passphrase))
        entropy_set_size = len(set(symbols))

        combinations = entropy_set_size ** len(passphrase)

        is_valid = (combinations > MINIMUM_STRENGTH) & (entropy_set_size > MINIMUM_ENTROPY_SET_SIZE)

        return is_valid

    @classmethod
    def command_line_arguments(cls):
        """
        It returns a Namespace object with the arguments given in the command line.
        """

        parser = argparse.ArgumentParser("python2.7 {}".format(os.path.basename(__file__)),
                                         formatter_class=argparse.RawTextHelpFormatter,
                                         description="Creates \delete-me\print-me.eps file to print coin information.")

        parser.add_argument("-s", "--serial", type=int,
                            help="Serial number.  \nValid values: 0 to 9999. Default is 0",
                            default=0)

        parser.add_argument("-p", "--passphrase", type=str,
                            help="Used to generate private key.\nE.g.: 'Th1s.Iz.My:SupeR.Sekret.-3aB1F769AeE21GcAb07d4'",
                            default = cls.secure_random_passphrase(64))

        parser.add_argument("-n", "--numerator", type=int,
                            help="Numerator of the fraction printed in the coin. \nValid values: 1 to 1000. Default is 1",
                            default=1)

        parser.add_argument("-d", "--denominator", type=int,
                            help="Denominator of the fraction printed in the coin. \nValues: 1 to 1000. Default is 1000",
                            default=1000)

        parser.add_argument("-t", "--timeout", type=int,
                            help ="How many seconds before the printable template and associated files are deleted."\
                                  "\nDefault = 300 (5 minutes).",
                            default = 30)

        arguments = parser.parse_args()

        if not cls.passphrase_is_robust(arguments.passphrase):
            exception_msg = "Passphrase <{}> is not sufficiently robust. " \
                            "Hint: Leave this parameter blank or choose a different one " \
                            "with greater entropy.".format(arguments.passphrase)
            raise Exception(exception_msg)

        return arguments

    def generate_coins(self, fromserial, toserial, showtrace=True):

        if showtrace:
            print
            print "· Universidad de La Coruña                  ·"
            print "·                                           ·"
            print "· Trabajo Fin de Grado  ·"
            print "· ----------------------------------------- ·"
            print "· Alberto Femenías Hermida                  ·"
            print
            print "· Debug mode is", self.debug
            if self.debug:
                print "· Note: In debug mode, only 1 iteration will be performed."
            print
            print

        if self.debug: toserial = fromserial

        for n in xrange(fromserial, toserial + 1):  # number of key pairs to generate`

            coin_prefix = 'Coin_' + '{:04d}'.format(n) + '_'
            if not self.debug:
                coin_secret_seed = coin_prefix + self.secret
                private_key_as_hex_string = self.private_key_from_passphrase(coin_secret_seed)
            else:
                coin_secret_seed = self.secret
                private_key_as_hex_string = self.secret

            private_key_as_bytes = self.HexToByte(private_key_as_hex_string)

            # fullkey = '80' + binascii.hexlify(priv_key).decode()
            fullkey = '80' + private_key_as_hex_string
            sha256a = hashlib.sha256(binascii.unhexlify(fullkey)).hexdigest()
            sha256b = hashlib.sha256(binascii.unhexlify(sha256a)).hexdigest()
            WIF = self.b58encode(binascii.unhexlify(fullkey + sha256b[:8]))

            # get public key , uncompressed address starts with "1"
            sk = ecdsa.SigningKey.from_string(private_key_as_bytes, curve=ecdsa.SECP256k1)
            vk = sk.get_verifying_key()

            uncompressedkey = binascii.hexlify(vk.to_string()).decode()

            # if ord(uncompressedkey[1]) % 2 == 1:

            if int(uncompressedkey, 16) % 2 == 1:
                pubkeyprefix = '03'  # If the Y value for the Public Key is odd.
            else:
                pubkeyprefix = '02'  # Or else, if the Y value is even.

            public_key_compressed_in_hex = pubkeyprefix + uncompressedkey[0:64].zfill(64)

            hash160 = self.ripemd160(hashlib.sha256(binascii.unhexlify(public_key_compressed_in_hex)).digest()).digest()
            publ_addr_a = b"\x00" + hash160
            checksum = hashlib.sha256(hashlib.sha256(publ_addr_a).digest()).digest()[:4]
            public_address_b58 = self.b58encode(publ_addr_a + checksum)

            i = n + 1
            # print('Private Key    ', str(i) + ": " + WIF.decode())
            #  if showtrace: print(coin_prefix, fullkey, WIF, public_address_b58)

            if showtrace:
                print "· Coin serial prefix                        :", coin_prefix
                print '· Secret string seed secret                 :', coin_secret_seed
                print '· Hex digest of string seed secret          :', private_key_as_hex_string
                print '· Private key in hex                        :', private_key_as_hex_string
                print '· Private address in base58                 :', WIF
                print "· Public key in hex, full and uncompressed  :", '04' + binascii.hexlify(vk.to_string()).decode()
                print "· Public key in hex, compressed             :", public_key_compressed_in_hex
                print '· Public address, compressed, in base58     :', public_address_b58
                print

            self.create_temp_folder()

            qr = pyqrcode.create(WIF)
            # qr.png(coin_prefix + 'PRIVATE_' + '.png', scale=2) -> Use different names for batch processing
            qr.png(self.PRIVATE_QR_PATHNAME, scale=2)
            qr = pyqrcode.create(public_address_b58)
            # qr.png(coin_prefix + 'PUBLIC_' + '.png', scale=2) -> Use different names for batch processing
            qr.png(self.PUBLIC_QR_PATHNAME, scale=2)
            if showtrace: print; print

            arguments = Bitcoin.command_line_arguments()

            coin_info = {}
            coin_info["serial"] = '{:04d}'.format(n)
            coin_info["numerator"] = arguments.numerator
            coin_info["denominator"] = arguments.denominator
            coin_info["WIF"] = WIF
            coin_info["address"] = public_address_b58
            Bitcoin.process_template(coin_info)


if __name__ == '__main__':

    # Testing data from https://medium.freecodecamp.org/how-to-create-a-bitcoin-wallet-address-from-a-private-key-eca3ddd9c05f
    # Online testing tool -> https://gobittest.appspot.com/
    #
    # To test, call this code:
    #
    #     btc = Bitcoin('60cf347dbc59d31c1358c8e5cf5e45b822ab85b79cb32a9f3d98184779a9efc2', debug=True)
    #     btc.generate_coins(args.serial, args.serial, showtrace=True)
    # 
    #
    # Expected results:
    #
    # · Coin serial prefix                        : Coin_0000_
    # · Secret string seed secret                 : 60cf347dbc59d31c1358c8e5cf5e45b822ab85b79cb32a9f3d98184779a9efc2
    # · Hex digest of string seed secret          : 60cf347dbc59d31c1358c8e5cf5e45b822ab85b79cb32a9f3d98184779a9efc2
    # · Private key in hex                        : 60cf347dbc59d31c1358c8e5cf5e45b822ab85b79cb32a9f3d98184779a9efc2
    # · Private address in base58                 : 5JYvSurww2jTxmCeoN8T9QgRMWp45rre7WgFS76ae6Rgd1BnkC6
    # · Public key in hex, full and uncompressed  : 041e7bcc70c72770dbb72fea022e8a6d07f814d2ebe4de9ae3f7af75bf706902a7b73ff919898c836396a6b0c96812c3213b99372050853bd1678da0ead14487d7
    # · Public key in hex, compressed             : 031e7bcc70c72770dbb72fea022e8a6d07f814d2ebe4de9ae3f7af75bf706902a7
    # · Public address, compressed, in base58     : 17JsmEygbbEUEpvt4PFtYaTeSqfb9ki1F1



    debugsession = False
    args = Bitcoin.command_line_arguments()

    if debugsession:
        btc = Bitcoin('60cf347dbc59d31c1358c8e5cf5e45b822ab85b79cb32a9f3d98184779a9efc2', debug=True)
    else:
        btc = Bitcoin(args.passphrase, debug=False)

    btc.generate_coins(args.serial, args.serial, showtrace=True)

    Bitcoin.show_instructions()
    Bitcoin.destroy_temp_folder()

