import random
import zmq
import democfg

def task(task_data):
    in_circle = 0
    for _ in range(int(task_data)):
        (x, y) = (random.random(), random.random())
        if (x ** 2 + y ** 2) <= 1:
            in_circle += 1
    return 4 * in_circle / task_data
