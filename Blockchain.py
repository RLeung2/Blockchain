import hashlib
import random


class Blockchain:

    """
        Exercise 1: Finding the nonce
        Given an input string of at most 70 characters, this function generates padding on the right
        such that the padded string is 100 characters in length and its SHA256 hash starts with “0000”.
        This is done by repeatedly randomly generating a nonce using all alphanumeric characters until
        one if found that satisfies the condition of its SHA256 hash starting with "0000".
    """
    def generate_nonce(self, string):
        # If the string is greater than 70 characters, no nonce is returned
        if len(string) > 70:
            return ""

        alphanumeric_characters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        nonce_length = 100 - len(string)
        nonce = ""

        # Keep generating new paddings until a valid one is found
        while not self.is_valid_sha256(string + nonce):
            nonce = ''.join(random.choice(alphanumeric_characters) for i in range(nonce_length))
        return nonce

    # Helper method that finds the SHA256 hash of the padded string and checks if it starts with "0000"
    @staticmethod
    def is_valid_sha256(string):
        sha256_hash = hashlib.sha256(string.encode())
        sha256_hash = sha256_hash.hexdigest()
        if sha256_hash[:4] == "0000":
            return True
        return False


if __name__ == "__main__":
    test = Blockchain()
    nonce = test.generate_nonce("3")
    print(nonce)
