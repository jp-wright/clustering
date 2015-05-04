import time
import zmq
import democfg, processor

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
    processor.process(receiver)
    # Let workers know that all results have been processed
    controller.send(democfg.done_msg)
    # Finished, but give 0MQ time to deliver
    time.sleep(5 * democfg.pause_time)
