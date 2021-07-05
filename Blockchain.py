import hashlib
import random
import time


class Blockchain:

    def __init__(self):
        # Variables for the mined block chain in Exercise 2
        # blockchain holds the list of blocks
        # hash_list holds the list of sha256 hashes
        self.blockchain = []
        self.hash_list = []

    """
        Exercise 1: Finding the nonce
        Given an input string of at most 70 characters, this function generates padding on the right
        such that the padded string is 100 characters in length and its SHA256 hash starts with “0000”.
        This is done by repeatedly randomly generating a nonce using all alphanumeric characters until
        one if found that satisfies the condition of the padded string's SHA256 hash starting with "0000".
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

    """
        Exercise 2: Constructing and verifying a blockchain
        A blockchain is an ordered list of blocks where each block has two fields:
            nonce: An alphanumeric string.
            miner: An integer number which is always 0 in this exercise.
    """
    def mine_the_next_block(self):
        # If the first block has yet to be mined, we consider the special case of generating the 99 length nonce
        # Hash for the first block: SHA256(miner + nonce)
        if not self.blockchain:
            miner = '0'
            nonce = self.generate_nonce(miner)
            self.blockchain.append({"nonce": nonce, "miner": miner})

            # Append the hash to the hash list for the next block to be mined
            combined_string = miner + nonce
            sha256_hash = hashlib.sha256(combined_string.encode()).hexdigest()
            self.hash_list.append(sha256_hash)
        else:
            # The previous hash is needed to mine every block after the first one
            # Hash for every block after the first: SHA256(previous_hash + miner + nonce)
            previous_sha256 = self.hash_list[-1]
            current_miner = '0'
            current_nonce = self.generate_nonce(previous_sha256 + current_miner)
            self.blockchain.append({"nonce": current_nonce, "miner": current_miner})

            # Append the hash to the hash list for the next block to be mined
            combined_string = previous_sha256 + current_miner + current_nonce
            sha256_hash = hashlib.sha256(combined_string.encode()).hexdigest()
            self.hash_list.append(sha256_hash)

    # Verifies a blockchain by computing the hash of each block and verifying that they all start with ‘0000’.
    @staticmethod
    def verify_chain(blockchain):
        # Keep track of the previous hash as it is needed to verify each block
        # There is no previous hash for the first block, so it starts as an empty string
        previous_hash = ""
        for i in range(len(blockchain)):
            current_block = blockchain[i]
            current_miner = current_block["miner"]
            current_nonce = current_block["nonce"]
            combined_string = previous_hash + current_miner + current_nonce
            current_sha256_hash = hashlib.sha256(combined_string.encode()).hexdigest()
            if current_sha256_hash[:4] != "0000":
                return False
            previous_hash = current_sha256_hash
        return True


if __name__ == "__main__":
    test_block = Blockchain()

    test_string = "3"
    test_nonce = test_block.generate_nonce(test_string)
    print("Nonce for the string '3':")
    print(test_nonce)
    print()

    start_time = time.time()
    for i in range(10):
        test_nonce = test_block.generate_nonce(test_string)
    total_time = time.time() - start_time
    average_time = total_time / 10
    print("Average time to find the nonce:")
    print(str(average_time) + " seconds")
    print()

    for i in range(10):
        test_block.mine_the_next_block()
    print("Blockchain:")
    print(test_block.blockchain)
    print()
    print("Blockchain Verification:")
    print(test_block.verify_chain(test_block.blockchain))
