import random
import zmq
import democfg, tasker

def is_done(socks, controller):
    if (socks.get(controller) == zmq.POLLIN and
        controller.recv() == democfg.done_msg):
        return True
    return False

def work(worker_id):
    context = zmq.Context()
    # Socket to receive messages on
    receiver = context.socket(zmq.PULL)
    receiver.connect(democfg.routing_table["receiver"])
    # Socket to send messages to
    sender = context.socket(zmq.PUSH)
    sender.connect(democfg.routing_table["sender"])
    # Socket for control input
    controller = context.socket(zmq.SUB)
    controller.connect(democfg.routing_table["controller"])
    controller.setsockopt(zmq.SUBSCRIBE, b"")
    # Process messages from receiver and controller
    poller = zmq.Poller()
    poller.register(receiver, zmq.POLLIN)
    poller.register(controller, zmq.POLLIN)
    # Process messages from both sockets
    run_loop = True
    while run_loop:
        socks = dict(poller.poll())
        if socks.get(receiver) == zmq.POLLIN:
            task_data = receiver.recv_pyobj()
            # Process task data
            result = tasker.task(task_data)
            sender.send_pyobj(result)
        if is_done(socks, controller):
            run_loop = False
