import time

_model = None
large_file_data = 'large_file.txt'


def init_model():
    global __model
    __model = load_file_task(large_file_data)
    print("Model Initialized")
    return "ok"


def load_file_task(file_path):
    start_time = time.time()
    print("Loading file into memory...")
    with open(file_path) as f:
        data = f.read()  # Loading the large file into memory
    end_time = time.time()
    print("File Loaded in {}s".format(end_time - start_time))
    print("Size data file: ", len(data))


def simple_background_task(n):
    delay = 5
    print("Task running")
    print(f"Simulating {delay} second delay")
    time.sleep(delay)
    print(n)
    print("Task Completed")

    return n




