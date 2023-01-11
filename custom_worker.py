import sys
import time
from rq import Connection, Worker, Queue
from jobs import init_model



def create_worker(qs):
    # Measure the time to load the file
    start_time = time.time()
    init_model()
    end_time = time.time()
    print(f"Time to load the file: {end_time - start_time} seconds")

    with Connection():
        worker = Worker(qs, name=f"{qs[0]}_worker")
        worker.work()


if __name__ == '__main__':
    qs = sys.argv[1:] or ['default']
    create_worker(qs)

