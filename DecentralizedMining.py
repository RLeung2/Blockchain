import threading
from queue import Queue
import time
from Blockchain import Blockchain

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
        blockchain = Blockchain()
        global stop_threads

        while blockchain.size() < 10:
            # If stop_threads is True, then a thread has finished mining the entire chain
            if stop_threads:
                break

            # The thread will be given 6 seconds to mine a block
            blockchain.mine_the_next_block(str(self.thread_id))
            time.sleep(6)

            # Send the blockchain from the current thread to all other threads in the threads dictionary
            global threads
            for thread_id in threads:
                # Doesn't send the blockchain to itself
                if thread_id == self.thread_id:
                    continue
                queue, thread = threads[thread_id]
                queue.put(blockchain)
            # If a blockchain is in the queue, it will be checked
            if not self.queue.empty():
                received_chain = self.queue.get(block=False)
                if Blockchain.verify_chain(received_chain.blockchain) and received_chain.size() > blockchain.size():
                    blockchain.set_chain(received_chain.blockchain)

            # If an entire chain of length 10 has been mined, set the global variable and let all the threads know
            # to stop.
            if blockchain.size() == 10:
                global completed_chain
                completed_chain = blockchain.blockchain
                stop_threads = True


if __name__ == "__main__":
    # Create K number of threads
    for i in range(7):
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

    # Obtain threads from the dictionary
    thread0 = threads[0][1]
    thread1 = threads[1][1]
    thread2 = threads[2][1]
    thread3 = threads[3][1]
    thread4 = threads[4][1]
    thread5 = threads[5][1]
    thread6 = threads[6][1]

    # Wait for all threads to finish before continuing
    thread0.join()
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
    thread6.join()

    for chain in completed_chain:
        print(chain)
    print("Threads Shut Down")
    print("Exiting Main Thread")
