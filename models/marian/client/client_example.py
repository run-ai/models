from __future__ import print_function, unicode_literals, division

import os
import datetime
import sys
import random
import argparse
from multiprocessing import Process

# pip install websocket_client
from websocket import create_connection

class Timer:
    def __init__(self, msg, timestamp=True):
        self._msg = msg
        self._timestamp = timestamp

    def __enter__(self):
        self._start = datetime.datetime.now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = datetime.datetime.now()
        ms = int((end - self._start).total_seconds() * 1000)
        msg = f"{self._msg} in {ms} ms" if isinstance(self._msg, str) else self._msg(ms)
        if self._timestamp:
            msg = f"{end.strftime('%H:%M:%S.%f')[:-3]}\t{msg}"
        print(msg)

def run(args, lines):
    ws = None

    def connect():
        nonlocal ws
        ws = create_connection("ws://{}:{}/translate".format(args.hostname, args.port))

    def close():
        nonlocal ws
        ws.close()

    if args.connect_per == 'process':
        connect()

    def translate(batch):
        nonlocal ws

        if args.connect_per == 'request':
            connect()

        with Timer(f"Process (pid {os.getpid()}) translated a single request of {args.batch_size} sentences"):
            ws.send(batch)
            result = ws.recv()
            # print(result.rstrip())

        if args.connect_per == 'request':
            close()

    with Timer(f"** Process (pid {os.getpid()}) translated {args.requests} requests"):
        request = 0
        while request < args.requests or args.requests == -1:
            request += 1

            # build a batch of random sentences
            batch = ""
            for line in random.sample(lines, args.batch_size):
                batch += line.decode('utf-8') if sys.version_info < (3, 0) else line

            # translate the batch
            translate(batch)

    if args.connect_per == 'process':
        close()

if __name__ == "__main__":
    # handle command-line options
    parser = argparse.ArgumentParser()
    parser.add_argument("--hostname", type=str, default="localhost")
    parser.add_argument("-p", "--port", type=int, default=8888)
    parser.add_argument("-b", "--batch-size", type=int, default=5)
    parser.add_argument("--processes", type=int, default=5)
    parser.add_argument("--requests", type=int, default=20)
    parser.add_argument("--connect-per", choices=['process', 'request'], default='request')
    args = parser.parse_args()

    # read text lines
    lines = sys.stdin.readlines()

    print(f"Launching {args.processes} processes; each process will send {args.requests} requests of {args.batch_size} sentences; connecting per {args.connect_per}.")

    # create child processes
    processes = [Process(target=run, args=(args, lines)) for _ in range(args.processes)]

    with Timer(lambda ms: ('-' * 80) + '\n' + f"Translated total {args.processes * args.requests} requests of {args.batch_size} sentences each in {ms} ms ({(float(args.processes * args.requests * args.batch_size) / (float(ms) / 1000.0)):.2f} sentences/second)", timestamp=False):
        # start all processes
        for process in processes:
            process.start()

        # wait for all processes
        for process in processes:
            process.join()
