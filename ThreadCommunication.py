import threading
from queue import Queue
import time

"""
    Exercise 4: Inter-thread communication
"""

# Variable to shut down the threads
stop_threads = False


class MyThread(threading.Thread):
    def __init__(self, queue, thread_id, name):
        super().__init__()
        self.thread_id = thread_id
        self.name = name
        self.queue = queue

    def run(self):
        readbuffer = ""
        while True:
            global stop_threads
            if stop_threads:
                break
            # If a new message is in the queue, it will be read and printed out
            if not self.queue.empty():
                readbuffer = self.queue.get(block=False)
                print(self.name + " received message " + readbuffer)

    # Method to send a message from the current thread to all other threads in the thread_dict parameter
    def send_message(self, thread_dict, message):
        print(self.name + " sending message " + message + " to all other threads.")
        for thread_id in thread_dict:
            # Doesn't send the message to itself
            if thread_id == self.thread_id:
                continue
            queue, thread = thread_dict[thread_id]
            queue.put(message)


if __name__ == "__main__":

    # Threads dictionary
    # The thread id is the key, and it stores both the thread object and a queue that can be used to talk to the
    # other threads in the dictionary.
    threads = {}

    # Create K number of threads
    for i in range(3):
        try:
            thread_name = "Thread-" + str(i)
            q = Queue()
            thread = MyThread(q, i, thread_name)
            thread.start()
            threads[i] = (q, thread)
        except Exception as e:
            print("An error occurred while creating threads.")
            print(str(e))

    # Obtain threads from the dictionary
    thread0 = threads[0][1]
    thread1 = threads[1][1]
    thread2 = threads[2][1]

    # Send a message from each thread to all other threads
    thread0.send_message(threads, "HELLO THIS IS THREAD-0")
    thread1.send_message(threads, "HOWDY THIS IS THREAD-1")
    thread2.send_message(threads, "HI THIS IS THREAD-2")

    # Shut down all the threads
    time.sleep(1)
    stop_threads = True

    print("Threads Shut Down")
    print("Exiting Main Thread")



