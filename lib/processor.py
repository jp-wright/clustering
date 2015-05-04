import time
import zmq
import democfg

def process(receiver):
    return get_results(receiver)

def get_results(receiver):
    data = []
    # Process results from the workers
    for _ in range(democfg.task_count):
        result = receiver.recv_pyobj()
        print("Processing result: {}".format(result))
        data.append(result)
    # Calculate final result
    print("Final result: {}".format(sum(data)/len(data)))
    return data
