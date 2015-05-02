worker_pool_size = 8
task_count = 8
delay_range = (1, 100) # milliseconds
pause_time = 1 # seconds
start_flag = b"0"
done_msg = b"DONE"
routing_table = {
    "receiver": "tcp://127.0.0.1:7557",
    "sender": "tcp://127.0.0.1:7558",
    "controller": "tcp://127.0.0.1:7559"}
