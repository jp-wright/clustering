import time
import zmq
import democfg

def process_results(receiver):
    data = []
    # Process results from the workers
    for _ in range(democfg.task_count):
        result = receiver.recv_pyobj()
        print("Processing result: {}".format(result))
        data.append(result)
    # Calculate final result
    print("Final result: {}".format(sum(data)/len(data)))

def collect():
    context = zmq.Context()
    # Socket to receive messages on (collect results from worker)
    receiver = context.socket(zmq.PULL)
    receiver.bind(democfg.routing_table["sender"])
    # Socket for worker control
    controller = context.socket(zmq.PUB)
    controller.bind(democfg.routing_table["controller"])
    # Wait for start signal
    assert receiver.recv() == democfg.start_flag
    process_results(receiver)
    # Let workers know that all results have been processed
    controller.send(democfg.done_msg)
    # Finished
    time.sleep(5 * democfg.pause_time)  # Give 0MQ time to deliver
