import random
import time


# generate a large file for testing
def generate_large_file(file_path):
    with open(file_path, "w") as f:
        for i in range(1000000000):
            f.write(str(random.random()) + "\n")


def load_large_file():
    global data
    print("Loading large file into memory...")
    with open("large_file.txt", "r") as f:
        data = f.read()  # Loading the large file into memory


def remove_large_file():
    global data
    data = None
    print("Large file removed from memory.")


def load_file_in_memory_task(file_path):
    global data
    start_time = time.time()
    length = len(data)
    end_time = time.time()
    print(f"File Loaded in {end_time-start_time}s")
    return length