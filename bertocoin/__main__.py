# -*- coding: utf-8 -*-
# author: Alberto Femenías Hermida

import argparse
import os
import sys
import binascii
import hashlib
import ecdsa
import json
import subprocess
import pyqrcode
import re
import time
from ripemd import ripemd160


class CoinInput:
    """
    The CoinInput is a static class that holds all the methods necessary to obtain and
    validate the user inputs needed to build the coin.
    The main method is command_line_arguments, which collects all inputs via cli
    arguments. The secret seed can also be input via file and is read by the
    read_entropy_file. There is also a method to create a secure secret and another one
    to validate that the secret provided by the user has enough entropy.
    """

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
        indices = [byte % len(charset) for byte in bytearray(random_bytes)]
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

    @staticmethod
    def read_entropy_file(file_path):
        """
        Reads secrete seed as all the content of the text file "entropy.txt"

        :param    file_path: The path to the directory that stores the file

        :return: The content of the file as a string
        """
        try:
            file = open('entropy.txt', 'r')
            print('Reading entropy file {}...'.format(file_path))
            print()
            return file.read()
        except IOError:
            raise IOError
        except Exception:
            print('An error ocurred while reading entropy file {}'.format(file_path))

    @classmethod
    def command_line_arguments(cls):
        """
        It returns a Namespace object with the arguments given in the command line.
        """

        parser = argparse.ArgumentParser("python3 {}".format(os.path.basename(__file__)),
                                         formatter_class=argparse.RawTextHelpFormatter,
                                         description="This utility creates a ./delete-me/print-me.svg file containing\n"
                                                     "a printable file holding the information of a physical a coin.")

        parser.add_argument("-s", "--serial", type=int,
                            help="· Serial number displayed in the coin's face.\n"
                                 "  Valid values: 0 to 9999. Default = 0.",
                            default=0)

        parser.add_argument('--debug', dest='debug_mode', action='store_true',
                            help="· Coins should not be produced using this mode!\n"
                                 "  In debug mode, sensible information will be output. Instead of a random seed,\n"
                                 "  the secret provided must be 32 bytes of data in hex format (private key).\n"
                                 "  The coin serial number will not influence the private key like in normal mode.")
        parser.set_defaults(debug_mode=False)

        parser.add_argument("-p", "--passphrase", type=str,
                            help="· Secret that will be used to generate private key.\n"
                                 "  By default the program will try to read the secret seed from \"./entropy.txt\".\n"
                                 "  You can override this behaviour providing the secret via this in-line argument.\n"
                                 "  E.g.: --passphrase='Th1s.Iz.My:SupeR.Sekret.-3aB1F79AeE21GcAb07d4'")

        parser.add_argument("--generate-pass", dest='generate_pass', action='store_true',
                            help="· Use this argument to auto-generate a secret using the best source of randomness\n"
                                 "  provided by the host operating system.\n"
                                 "  With this argument all inputs are ignored and only the secure secret is return.")
        parser.set_defaults(generate_pass=False)

        parser.add_argument("-n", "--numerator", type=int,
                            help="· Numerator of the fraction printed in the coin's face.\n"
                                 "  Valid values: 1 to 1000. Default = 1.",
                            default=1)

        parser.add_argument("-d", "--denominator", type=int,
                            help="· Denominator of the fraction printed in the coin's face.\n"
                                 "  Valid values: 1 to 1000. Default = 1000.",
                            default=1000)

        parser.add_argument("-t", "--timeout", type=int,
                            help="· How many seconds before the printable template and associated files are deleted.\n"
                                 "  Default = 300 (5 minutes).",
                            default=300)

        arguments = parser.parse_args()

        # if no passphrase is provided we try to read it from the entropy file
        if (not arguments.generate_pass and (arguments.passphrase is None or arguments.passphrase == "")):
            try:
                arguments.passphrase = cls.read_entropy_file("entropy.txt")
            except IOError:
                raise IOError("No file 'entropy.txt' in the current directory! You must provide either an entropy file "
                              "or a passphrase as inline argument.\n"
                              "Enter --help to show the help message.")

        return arguments


class Bitcoin:
    """
    This Bitcoin class gathers all the necessary methods needed to produce the public
    address and WIF of a bitcoin coin from just a secret seed. The self.generate_coin
    method executes all the steps needed to convert the secret into addresses.
    This class does not generate a secret seed, it has to be provided as an argument.
    """

    def __init__(self, secret_seed, serial_number):
        self.secret = secret_seed
        self.serial_number = serial_number

    def __private_key_from_passphrase(self, passphrase):
        """
        Given a string passphrase it returns a private key obtained by hashing it
        :param src: The passphrase to convert
        :return: A hex string with the sha256() hash digest of the given passphrase
        """

        privatekey = hashlib.sha256(passphrase.encode("utf-8")).hexdigest()
        return str(privatekey)

    def __ripemd160(self, byte_seq):
        """
        Given a sequence of bytes <byte_seq> it returns its RIPEMD160 hash object
        :param v: The sequence of bytes whose hash we want to obtain
        :return: A hash of the bytes <byte_seq> input, using the RIPEMD160 algorithm
        """
        data = ripemd160.new()
        data.update(byte_seq)
        ripemd160_byte_seq = data.digest()

        return ripemd160_byte_seq

    def __b58encode(self, byte_array):
        """
        Given a byte sequence <byte_array>, it returns a string that represents this value in Base58 format.
        To ensure that leading zeros have an influence on the result, the bitcoin base58 encoding includes
        a manual step to convert all leading 0x00s to 1s.
        :param v -> The sequence of bytes encode
        :return: A string in format Base58 representing the value of v
        """

        digit = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        base = len(digit)
        val = 0
        for b in bytearray(byte_array):
            val *= 256
            val += b

        result = ""
        while val:
            (val, mod) = divmod(val, base)
            result = digit[mod] + result

        pad = 0
        for b in byte_array:
            if b == 0x00:
                pad += 1
            else:
                break

        ret = (digit[0] * pad) + result

        return ret

    def __b58decode(self, encoded_string):
        """
        Decode a Base58 <encoded_string> string to byte sequence
        :param encoded_string -> The string in Base58 format
        :return: A sequence of bytes corresponding to the input string
        """
        alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        base = len(alphabet)

        # Initialize the byte array
        byte_array = bytearray()

        # Initialize the current value
        current_value = 0

        # Iterate through each character in the encoded string
        for c in encoded_string:
            # Get the index of the character in the alphabet
            index = alphabet.index(c)

            # Add the index * (base ^ position) to the current value
            current_value = current_value * base + index

        # Convert the current value to a byte array
        while current_value > 0:
            # Get the next byte
            next_byte = current_value & 0xff

            # Append the byte to the byte array
            byte_array.append(next_byte)

            # Remove the byte from the current value
            current_value >>= 8

        # Reverse the byte array and return it
        byte_array.reverse()
        return byte_array

    def __hex_to_byte(self, hex_str):
        """
        Convert a string hex byte values into a byte sequence. The Hex Byte values may
        or may not be space separated.
        :param hexStr: A string of hex bytes values
        :return: A byte sequence with the hex values converted.
        """
        return bytes.fromhex(hex_str)

    def generate_coin(self, debug=False):

        print("┌─────     Universidad de La Coruña     ─────┐")
        print("│                                            │")
        print("│            Trabajo Fin de Grado            │")
        print("├────────────────────────────────────────────┤")
        print("└─────     Alberto Femenías Hermida     ─────┘")
        print()

        coin_prefix = 'Coin_' + self.serial_number + '_'

        if not debug:
            # the private key of the coin is obtained by digesting the secret AND the serial
            coin_secret_seed = coin_prefix + self.secret
            private_key_as_hex_string = self.__private_key_from_passphrase(coin_secret_seed)
        else:
            print("· Debug mode is on.")
            print("· Note: In debug mode sensible information will be displayed.")
            print()

            is_hexprivate_key_hex = re.compile(r"^[0-9A-fz]{64}$")
            if not is_hexprivate_key_hex.match(self.secret):
                print("Invalid passphrase!")
                print("In debug mode the secret provided must be 64 chars of data in hex format (private key)!")
                exit(1)
            coin_secret_seed = self.secret
            # in debug mode there is no digest: secret seed is the private key
            private_key_as_hex_string = self.secret

        # to obtain the WIF we must:
        # 1. add a 0x80 byte in front of it for mainnet addresses
        private_key_as_bytes = self.__hex_to_byte(private_key_as_hex_string)
        fullkey = '80' + private_key_as_hex_string
        # 2. compute the 4 checksum bytes
        sha256a = hashlib.sha256(binascii.unhexlify(fullkey)).hexdigest()
        sha256b = hashlib.sha256(binascii.unhexlify(sha256a)).hexdigest()
        # 3. append the checksum and convert to base58
        WIF = self.__b58encode(binascii.unhexlify(fullkey + sha256b[:8]))

        # now get the uncompressed public key from our private key:
        sk = ecdsa.SigningKey.from_string(private_key_as_bytes, curve=ecdsa.SECP256k1)
        vk = sk.get_verifying_key()
        # uncompressed public keys start with 04
        uncompressedkey = binascii.hexlify(vk.to_string()).decode()

        # then we compute the compressed public key (as they are more efficient) by:
        # 1. obtaining the correct compressed prefix
        if int(uncompressedkey, 16) % 2 == 1:
            pubkeyprefix = '03'  # If the Y value for the Public Key is odd.
        else:
            pubkeyprefix = '02'  # Or else, if the Y value is even.
        # 2. remove the Y coordinate and prepend the prefix
        public_key_compressed_in_hex = pubkeyprefix + uncompressedkey[0:64].zfill(64)

        # now we convert the compressed public key into the compressed public address:
        hash160 = self.__ripemd160(hashlib.sha256(binascii.unhexlify(public_key_compressed_in_hex)).digest())
        # add the network byte
        publ_addr_a = b"\x00" + hash160
        # compute the checksum, append and convert to base58
        checksum = hashlib.sha256(hashlib.sha256(publ_addr_a).digest()).digest()[:4]
        public_address_b58 = self.__b58encode(publ_addr_a + checksum)

        if debug:
            print("· Coin serial prefix                        :", coin_prefix)
            print("· Secret string seed                        :", coin_secret_seed)
            print("· Private key in hex (hex digest)           :", private_key_as_hex_string)
            print("· Private address (WIF format)              :", WIF)
            print("· Public key in hex, full and uncompressed  :", '04' + binascii.hexlify(vk.to_string()).decode())
            print("· Public key in hex, compressed             :", public_key_compressed_in_hex)
            print("· Public address, compressed, in base58     :", public_address_b58)
            print()

        return WIF, public_address_b58


class CoinStamper:
    """
    The duty of the CoinStamper is to produce a printable file and the address QR codes.
    All the information needed to produce the coin (serial, fraction, addres and WIF)
    have to be provided as arguments, this class has no knowledge of bitcoin, it just
    generates the final resources from the coin information object.
    """

    def __init__(self,
                 resources_path="./resources",
                 template_input="bertocoin.svg",
                 template_output="print-me.svg",
                 temp_folder="delete-me"):

        self.temp_folder = temp_folder
        self.template_input_path = f"{resources_path}/{template_input}"
        self.template_output_path = os.path.join(temp_folder, template_output)
        self.private_qr_pathname = os.path.join(temp_folder, "coin_private_qr.png")
        self.public_qr_pathname = os.path.join(temp_folder, "coin_public_qr.png")

    def __similar_splits(self, s, n):
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
        part_size = (len(s) - remainder) // n
        excess = remainder

        index = 0
        ret = []
        for i in range(n):
            delta = 1 if excess > 0 else 0
            excess -= 1
            next_index = (index + part_size + delta)
            chunk = s[index:next_index]
            ret.append(chunk)
            index = next_index

        sanity_check = "".join(ret)
        if not sanity_check == s:
            exception_msg = f"Unexpected error, splits don't add up to the whole string.\n <{s}> != <{sanity_check}>"
            raise Exception(exception_msg)

        return ret

    def __replace_template_variable(self, line, template_var, expanded_value, debug=False):
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
            if debug:
                print('Found ', template_var)
            ret = line.replace(template_var, expanded_value)
        return ret

    def __create_temp_folder(self):
        """
        Utility method. It creates a temp folder to place the temporary files used to generate the
        printable template.
        :return: Nothing.
        """
        dir_name = self.temp_folder
        # Create target directory if it doesn't exist
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

    def __generate_QR_codes(self, WIF, public_address):
        """
        Generates the two QR png images (WIF and public address) using the QR code generator
        utility PyQRCode.
        :param WIF: Wallet Input Format to be hidden in the coin
        :param public_address: Public address displayed in the face of the coin
        :return: saves the QR codes to two different png files.
        """
        self.__create_temp_folder()

        qr = pyqrcode.create(WIF)
        qr.png(self.private_qr_pathname, scale=2)
        qr = pyqrcode.create(public_address)
        qr.png(self.public_qr_pathname, scale=2)

    def process_template(self, coin_info):
        """
        It creates the printable file by replacing the variables inside the .svg template
        file with their respective values. This method will also generate the QR images
        which are also part of the processed template.

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
        self.__create_temp_folder()
        template_input = open(self.template_input_path, 'r')
        template_output = open(self.template_output_path, 'w')
        template_lines = template_input.readlines()

        wif = self.__similar_splits(coin_info["WIF"], 3)
        address = self.__similar_splits(coin_info["address"], 3)
        serial = coin_info["serial_number"]
        numerator = coin_info["numerator"]
        denominator = coin_info["denominator"]

        for line in template_lines:

            # Replace ::serial::
            line = self.__replace_template_variable(line, '::serial::', serial)

            # Replace ::f::
            line = self.__replace_template_variable(line, '::f::', '{}:{}'.format(numerator, denominator))

            # Replace ::address.XX::
            for i in range(0, 3):
                line = self.__replace_template_variable(line,
                                                        '::address.000{}::'.format(i + 1),
                                                        address[i])

            # Replace ::secret.XX::
            for i in range(0, 3):
                line = self.__replace_template_variable(line,
                                                        '::secret.000{}::'.format(i + 1),
                                                        wif[i])

            template_output.writelines(line)

        template_output.close()
        template_input.close()

        self.__generate_QR_codes(coin_info["WIF"], coin_info["address"])

        # return the path to the printable file we just generated
        return self.template_output_path


class CoinTerminator:
    """
    The CoinTerminator gathers all the necessary steps needed to finish the execution
    once the printable resource has been generated. There are 3 main steps left to do
    before closing which are:
      - Showing the instructions on how to print the file.
      - Waiting some seconds to let the user some room set up the print.
      - Delete all generated files (printable and QRs)
    The first 2 steps are executed by the method self.show_instructions and the last
    one is performed by self.destroy_temp_folder
    """

    def __init__(self, printable_filepath):
        self.dying_folder = printable_filepath.split('/')[0]
        self.printable_file = printable_filepath.split('/')[1]
        self.entropy_file = "entropy.txt"

    def __progress_bar(self, iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
        """
        This method is ment to be called inside a loop to create the efect of a progress bar.
        :params:
        :param iteration: current iteration (Int))
        :param total: total iterations (Int)
        :param prefix: prefix string (Str)
        :param suffix: suffix string (Str)
        :param decimals: positive number of decimals in percent complete (Int)
        :param bar_length: character length of bar (Int)
        """
        str_format = "{0:." + str(decimals) + "f}"
        percents = str_format.format(100 * (iteration / float(total)))
        filled_length = int(round(bar_length * iteration / float(total)))
        bar = '█' * filled_length + '-' * (bar_length - filled_length)

        sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

        if iteration == total:
            sys.stdout.write('\n')
        sys.stdout.flush()

    def __delayed_type(self, type_me, delay=0.1, newline=True):
        """
        Send characters to console, one by one, simulating manual typing
        :param type_me: Text to send
        :param public_address: Delay between keystrokes (float)
        :param newline: whether or not finish with a new line
        :return: <it outputs via stdout>
        """

        type_me = type_me + " "
        for i in range(len(type_me)):
            partial = type_me[0:i]

            sys.stdout.write('\r{}'.format(partial)),
            sys.stdout.flush()
            time.sleep(delay)

        if newline:
            sys.stdout.write('\n')
        sys.stdout.flush()

    def __secure_delete(self, path, recursive=False):
        """
        Removes files and directories is a secure manner by making a call
        to srm (or Secure Remove), command line utility for Unix-like systems
        :param recursive: deletes files and subdirectories
        :param path: the path to the file or directory that will be remove
        """

        r_arg = "-r" if recursive else ""
        subprocess.check_call(f'srm {r_arg} {path}', shell=True)

    def show_instructions(self, timeout):
        """
        Shows the instructions indicating how to print the coin as well as how to delete the
        created resources to maintain the coin secure.
        After the instructions, the method displays a progress bar showing the time left.
        This method does not destroy the resources.
        :param timeout: The number of seconds the user has to print the file,
        :return: <it outputs via stdout>
        """
        BLUE = '\033[94m'
        END_COLOR = '\033[0m'
        RED = '\033[31m'

        self.__delayed_type("INSTRUCTIONS")
        self.__delayed_type("------------")
        print()
        self.__delayed_type("1.- Navigate to this folder: ")
        self.__delayed_type("    {}{}/{}{} ".format(BLUE,
                                                    os.path.abspath(os.getcwd()),
                                                    self.dying_folder, END_COLOR),
                            delay=0.005)
        print()
        self.__delayed_type("2.- Use your browser (Safari, Chrome...) to open this file: ")
        self.__delayed_type("    {}{}{} ".format(BLUE, self.printable_file, END_COLOR), delay=0.005)
        print()
        self.__delayed_type("3.- Print it on good-quality paper.")
        print()
        self.__delayed_type("4.- Follow the instructions provided in the template you just printed.")
        print()
        print()

        self.__delayed_type(RED + "WARNING:" + END_COLOR)
        self.__delayed_type("--------")
        self.__delayed_type('You only have {} seconds to print the template.'.format(timeout))
        self.__delayed_type('After that, all the files in the folder:')

        self.__delayed_type("    {}{}/{}{} ".format(BLUE,
                                                    os.path.abspath(os.getcwd()),
                                                    self.dying_folder, END_COLOR),
                            delay=0.005)

        self.__delayed_type("will be deleted, to protect the security of your coin.\n")
        self.__delayed_type("If the self-destroy process does not finish properly, "
                            "please delete the contents of that folder manually.")
        print()

        # print a progress bar to show time left
        for i in range(timeout):
            time.sleep(1)
            self.__progress_bar(i + 1,
                                timeout,
                                prefix='Self destroy timer:',
                                suffix='({} seconds left.)'.format(timeout - i),
                                bar_length=50)

    def destroy_temp_folder(self):
        """
        Utility method. It deletes the temp folder that was used to generate the printable template
        file as well as the entropy.txt input if it was used.
        :return: Nothing.
        """

        END_COLOR = '\033[0m'
        RED = '\033[31m'

        print()
        print("Destroying temporary folder...")
        if os.path.exists(self.dying_folder):
            try:
                self.__secure_delete(self.dying_folder, recursive=True)
                print("Done")
                print()
            except Exception as error:
                print(error)
                print(RED + "WARNING !!!" + END_COLOR)
                print(f"  Unable to secure delete coin folder and its associated files: {self.dying_folder}.")
                print("  Please remove them MANUALLY in a safe way, otherwhise "
                      "the security of the coin will be compromised.")
                print()

        # if the secret was input via file, delete also this file
        if os.path.isfile(self.entropy_file):
            try:
                print(f"Destroying {self.entropy_file}...")
                self.__secure_delete(self.entropy_file)
                print("Done")
                print()
            except Exception as error:
                print(error)
                print(RED + "WARNING !!!" + END_COLOR)
                print(f"  Unable to secure delete {self.entropy_file}.")
                print("  Please remove it MANUALLY in a safe way, otherwise "
                      "the security of the coin will be compromised.")
                print()


if __name__ == '__main__':
    # Testing data from:
    # - https://medium.freecodecamp.org/how-to-create-a-bitcoin-wallet-address-from-a-private-key-eca3ddd9c05f
    # Online testing tools:
    # - https://gobittest.appspot.com/
    # - https://privatekeys.pw/calc
    #
    # To test, call this code:
    #   $ python3 bertocoin --debug --passphrase=60cf347dbc59d31c1358c8e5cf5e45b822ab85b79cb32a9f3d98184779a9efc2
    #
    # Expected results:
    #
    # · Coin serial prefix                        : Coin_0000_
    # · Secret string seed secret                 : 60cf347dbc59d31c1358c8e5cf5e45b822ab85b79cb32a9f3d98184779a9efc2
    # · Hex digest of string seed secret          : 60cf347dbc59d31c1358c8e5cf5e45b822ab85b79cb32a9f3d98184779a9efc2
    # · Private key in hex                        : 60cf347dbc59d31c1358c8e5cf5e45b822ab85b79cb32a9f3d98184779a9efc2
    # · Private address (WIF format)              : 5JYvSurww2jTxmCeoN8T9QgRMWp45rre7WgFS76ae6Rgd1BnkC6
    # · Public key in hex, full and uncompressed  : 041e7bcc70c72770dbb72fea022e8a6d07f814d2ebe4de9ae3f7af75bf706902a7b73ff919898c836396a6b0c96812c3213b99372050853bd1678da0ead14487d7 # noqa: E501
    # · Public key in hex, compressed             : 031e7bcc70c72770dbb72fea022e8a6d07f814d2ebe4de9ae3f7af75bf706902a7
    # · Public address, compressed, in base58     : 17JsmEygbbEUEpvt4PFtYaTeSqfb9ki1F1
    #
    # If you want to check the integrity of a coin without debug mode, just input the WIF in this page:
    # https://www.bitaddress.org/ > Wallet Details > (Input WIF)
    # and validate that the public address is correct

    DEBUG = False

    # STEP 1: Obtain all necessary inputs to create the coin
    try:
        args = CoinInput.command_line_arguments()
        DEBUG = args.debug_mode
    except IOError as e:
        print(e)
        exit(1)

    if (args.generate_pass):
        print(CoinInput.secure_random_passphrase())
        exit(0)

    if (not DEBUG and not CoinInput.passphrase_is_robust(args.passphrase)):
        print("The passphrase you entered is not sufficiently robust! \n"
              "Please choose a different one with greater entropy.")
        exit(1)

    coin = {
        'passphrase': args.passphrase,
        'serial_number': str(args.serial).zfill(4),
        'numerator': str(args.numerator),
        'denominator': str(args.denominator),
        'WIF': None,
        'address': None
    }

    # STEP 2: Obtain WIF and public-address from secret
    btc = Bitcoin(coin['passphrase'], coin['serial_number'])
    WIF, public_address_b58 = btc.generate_coin(debug=DEBUG)

    coin["WIF"] = WIF
    coin["address"] = public_address_b58

    if (DEBUG):
        print("Attention: you are running the program in Debug mode so the passphrase entropy was not "
              "checked.\nThe coin generated might not be secure! \n")
        print("Here is all the information that constitutes the coin:")
        print(json.dumps(coin, indent=4))
        print()

    # STEP 3: Generate printable file with all coin info
    stamper = CoinStamper()
    generated_coin_dirpath = stamper.process_template(coin_info=coin)

    # STEP 4: Show instructions and then delete resources
    shredder = CoinTerminator(printable_filepath=generated_coin_dirpath)
    shredder.show_instructions(timeout=args.timeout)
    shredder.destroy_temp_folder()
