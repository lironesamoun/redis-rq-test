# RQ Test Loading 


## 🛠️ Installation    
- Create first a virtual env, then install all the dependencies
```bash
pip3 install -r requirements.txt
```


## 🧑🏻‍💻 Usage

1. **Init one or multiple workers** - For the purpose of testing, init two workers with two bash terminal

```bash
# Create a worker with the name of default for handling "default" queue
python3 custom_worker.py default  
# Create a worker with the name of big_file for handling "big_file" queue
python3 custom_worker.py big_file  
```
The particularity of those custom workers is the fact that they load at their initialization a big file of about 3 go named `large_file.txt` which should be present for testing.

Otherwise you can generate it by doing first:
```bash
python3 app.py  
```

2. **Execute the Flask app server**
```bash
flask run 
```

3. **Use the predefined routes to run multiple jobs**


#### A route for putting on the queue the task of loading the big file `large_file.txt`   
It requires the *big_file worker* for executing the process.

*note*: the big file has been already loaded with the worker but here it's just to simulate how much time it take for a job to be executed

```http
GET /init_model
```

#### A route for putting on the default queue multiple simple tasks
It requires the *default worker* for executing the process.
```http
GET /task?n=[int]
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `n` | `int` | **Required**. Number of simple tasks you want to add to the default queue|
        
#### A route for putting on the big_file queue multiple simple tasks
It requires the *big_file worker* for executing the process.
```http
GET /tasks?n=[int]
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `n` | `int` | **Required**. Number of simple tasks you want to add to the default queue|
        


## Conclusion
        
- When the worker init, it inits at the same time a big file `large_file.txt` of about 3go. it takes about on average 4s but it will be **available for all the next steps.**
- The need to reload the file would be needed if the worker shut down
- Another solution would be to store the big file or model to redis cache 
- 


## Worker lifecycle

From the doc:

The Worker Lifecycle
The life-cycle of a worker consists of a few phases:

- **Boot**. Loading the Python environment.
- **Birth registration**. The worker registers itself to the system so it knows of this worker.
- **Start listening.** A job is popped from any of the given Redis queues. If all queues are empty and the worker is running in burst mode, quit now. Else, wait until jobs arrive.
- **Prepare job execution**. The worker tells the system that it will begin work by setting its status to busy and registers job in the StartedJobRegistry.
- **Fork a child process**. A child process (the “work horse”) is forked off to do the actual work in a fail-safe context.
- Process work. This performs the actual job work in the work horse.
- **Cleanup job execution**. The worker sets its status to idle and sets both the job and its result to expire based on result_ttl. Job is also removed from StartedJobRegistry and added to to FinishedJobRegistry in the case of successful execution, or FailedJobRegistry in the case of failure.
- **Loop**. Repeat from step 3.

Basically the rq worker shell script is a simple fetch-fork-execute loop. When a lot of your jobs do lengthy setups, or they all depend on the same set of modules, you pay this overhead each time you run a job (since you’re doing the import after the moment of forking). This is clean, because RQ won’t ever leak memory this way, but also slow.

A pattern you can use to improve the throughput performance for these kind of jobs can be to import the necessary modules before the fork. There is no way of telling RQ workers to perform this set up for you, but you can do it yourself before starting the work loop.

That's why here, the big file is loaded at the init of the worker.