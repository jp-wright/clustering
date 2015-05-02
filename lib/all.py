import multiprocessing, random, sys, time
import zmq
import democfg

def run_task(task_data):
    in_circle = 0
    for _ in range(int(task_data)):
        (x, y) = (random.random(), random.random())
        if (x ** 2 + y ** 2) <= 1:
            in_circle += 1
    return 4 * in_circle / task_data

def process_results(receiver):
    data = []
    # Process results from the workers
    for _ in range(democfg.task_count):
        result = receiver.recv_pyobj()
        print("Processing result: {}".format(result))
        data.append(result)
    # Calculate final result
    print("Final result: {}".format(sum(data)/len(data)))

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
            result = run_task(task_data)
            sender.send_pyobj(result)
        if is_done(socks, controller):
            run_loop = False

def sink():
    context = zmq.Context()
    # Socket to receive messages on (collect results from worker)
    receiver = context.socket(zmq.PULL)
    receiver.bind(democfg.routing_table["sender"])
    # Socket for worker control
    controller = context.socket(zmq.PUB)
    controller.bind(democfg.routing_table["controller"])
    # Wait for start signal
    assert receiver.recv() == b"0"
    process_results(receiver)
    # Let workers know that all results have been processed
    controller.send(democfg.done_msg)
    # Finished
    time.sleep(5 * democfg.pause_time)  # Give 0MQ time to deliver

def vent(tasks):
    context = zmq.Context()
    # Socket to send messages on
    sender = context.socket(zmq.PUSH)
    sender.bind(democfg.routing_table["receiver"])
    # Socket with direct access to the sink used to syncronize start of batch
    syncher = context.socket(zmq.PUSH)
    syncher.connect(democfg.routing_table["sender"])
    # Socket for control input
    controller = context.socket(zmq.SUB)
    controller.connect(democfg.routing_table["controller"])
    controller.setsockopt(zmq.SUBSCRIBE, b"")
    # Give 0MQ time to start up
    time.sleep(democfg.pause_time)
    syncher.send(b"0")
    poller = zmq.Poller()
    poller.register(controller, zmq.POLLIN)
    for task in tasks:
        sender.send_pyobj(task)
    # Give 0MQ time to deliver message
    time.sleep(democfg.pause_time)

def main(tasks):
    # Initialize random number generator
    random.seed()
    print("Starting workers ...")
    for worker_id in range(democfg.worker_pool_size):
        worker = multiprocessing.Process(target=work, args=[worker_id])
        worker.start()
    print("Starting sink ...")
    sinker = multiprocessing.Process(target=sink)
    sinker.start()
    time.sleep(democfg.pause_time)
    print("Starting ventilator ...")
    vent(tasks)

if __name__ == "__main__":
    count = range(democfg.task_count)
    tasks = [1e8 / democfg.task_count for _ in count]
    main(tasks)
