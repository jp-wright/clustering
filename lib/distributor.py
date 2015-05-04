import time
import zmq
import democfg

def distribute(tasks):
    context = zmq.Context()
    # Socket to send messages on
    sender = context.socket(zmq.PUSH)
    sender.bind(democfg.routing_table["receiver"])
    # Socket with direct access to the sink used to synchronize start of batch
    syncher = context.socket(zmq.PUSH)
    syncher.connect(democfg.routing_table["sender"])
    # Give 0MQ time to start up
    time.sleep(democfg.pause_time)
    syncher.send(democfg.start_flag)
    for task in tasks:
        sender.send_pyobj(task)
    # Give 0MQ time to deliver message
    time.sleep(democfg.pause_time)
