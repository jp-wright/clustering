import multiprocessing, random, time
import zmq
import collector, democfg, distributor, worker

def main(tasks):
    # Initialize random number generator
    random.seed()
    print("Starting task workers ...")
    for worker_id in range(democfg.worker_pool_size):
        worker_proc = multiprocessing.Process(
            target=worker.work, args=[worker_id])
        worker_proc.start()
    print("Starting task collector ...")
    collector_proc = multiprocessing.Process(target=collector.collect)
    collector_proc.start()
    time.sleep(democfg.pause_time)
    print("Starting task distributor ...")
    distributor.distribute(tasks)

if __name__ == "__main__":
    tasks = [1e8 / democfg.task_count] * democfg.task_count
    main(tasks)
