import threading
from queue import Queue
from func_timeout import func_set_timeout
from Blockchain import Blockchain
import func_timeout

"""
    Exercise 5: Decentralizing the blockchain
"""

# Variable to shut down the threads
stop_threads = False

# Threads dictionary
threads = {}

# The fully mined chain to be printed at the end
completed_chain = []


class MyThread(threading.Thread):

    def __init__(self, queue, thread_id, name):
        super().__init__()
        self.thread_id = thread_id
        self.name = name
        self.queue = queue

    def run(self):
        # Start a new blockchain to mine
        blockchain_obj = Blockchain()
        global stop_threads

        while blockchain_obj.size() < 10:
            # If stop_threads is True, then a thread has finished mining the entire chain
            if stop_threads:
                break

            # The thread will be given 3 seconds to mine a block
            try:
                self.timeout_mine(blockchain_obj)
            except func_timeout.FunctionTimedOut:
                pass

            # Send the blockchain from the current thread to all other threads in the threads dictionary
            global threads
            for thread_id in threads:
                # Doesn't send the blockchain to itself
                if thread_id == self.thread_id:
                    continue
                queue, thread = threads[thread_id]
                queue.put(blockchain_obj)
            # If a blockchain is in the queue, it will be checked
            if not self.queue.empty():
                received_chain = self.queue.get(block=False)
                if Blockchain.verify_chain(received_chain.blockchain) and received_chain.size() > blockchain_obj.size():
                    blockchain_obj.set_chain(received_chain.blockchain)
                    blockchain_obj.set_hash_list(received_chain.hash_list)

            # If an entire chain of length 10 has been mined, set the global variable and let all the threads know
            # to stop.
            if blockchain_obj.size() == 10:
                global completed_chain
                completed_chain = blockchain_obj.blockchain
                stop_threads = True

    # Function used to mine with a time constraint, currently set to 3 seconds
    @func_set_timeout(3)
    def timeout_mine(self, blockchain_obj):
        blockchain_obj.mine_the_next_block(str(self.thread_id))


if __name__ == "__main__":
    # Create K number of threads
    for i in range(10):
        try:
            thread_name = "Thread-" + str(i)
            q = Queue()
            thread = MyThread(q, i, thread_name)
            thread.start()
            threads[i] = (q, thread)
        except Exception as e:
            print("An error occurred while creating threads.")
            print(str(e))

    print("Threads Started")

    # Obtain thread from the dictionary
    thread0 = threads[0][1]

    # Wait for all threads to finish before continuing
    thread0.join()

    for chain in completed_chain:
        print(chain)
    print("Threads Shut Down")
    print("Exiting Main Thread")
