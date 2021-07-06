import threading
import time

"""
    Exercise 3: Multithreading
"""

# Variable to shut down the threads
stop_threads = False


class MyThread (threading.Thread):

    def __init__(self, thread_id, name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.time = time.ctime(time.time())
        self.print_count = 0

    def run(self):
        # Thread runs until stopped by the main thread
        while True:
            global stop_threads
            # Print the information only once while the thread runs
            if self.print_count <= 0:
                print(self.name + ": [" + str(self.thread_id) + "] -- time: " + self.time)
                self.print_count += 1
            if stop_threads:
                break


if __name__ == "__main__":
    # Create new threads
    thread0 = MyThread(0, "Thread-0")
    thread1 = MyThread(1, "Thread-1")
    thread2 = MyThread(2, "Thread-2")
    thread3 = MyThread(3, "Thread-3")

    # Start new threads
    thread0.start()
    thread1.start()
    thread2.start()
    thread3.start()

    # Shut down all the threads
    time.sleep(1)
    stop_threads = True
    thread0.join()
    thread1.join()
    thread2.join()
    thread3.join()

    print("Threads Shut Down")
    print("Exiting Main Thread")
