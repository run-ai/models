from __future__ import print_function, unicode_literals, division

import os
import datetime
import sys
import argparse
from multiprocessing import Process

# pip install websocket_client
from websocket import create_connection

class Timer:
    def __init__(self, msg):
        self._msg = msg

    def __enter__(self):
        self._start = datetime.datetime.now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = datetime.datetime.now()
        print(f"{self._msg} in {int((end - self._start).total_seconds() * 1000)} ms")

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

        with Timer(f"Process {os.getpid()} translated batch of {args.batch_size} sentences"):
            ws.send(batch)
            result = ws.recv()
            # print(result.rstrip())

        if args.connect_per == 'request':
            close()

    count = 0
    batch = ""
    request = 0

    with Timer(f"** Process {os.getpid()} translated {args.requests} requests"):
        while request < args.requests or args.requests == -1:
            for line in lines:
                count += 1
                batch += line.decode('utf-8') if sys.version_info < (3, 0) else line
                if count == args.batch_size:
                    # translate the batch
                    translate(batch)

                    count = 0
                    batch = ""

            if count:
                # translate the remaining sentences
                translate(batch)

            request += 1

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

    print(f"Launching {args.processes} processes with {args.requests} requests each; connecting per {args.connect_per}.")

    # create child processes
    processes = [Process(target=run, args=(args, lines)) for _ in range(args.processes)]

    with Timer(('-' * 40) + '\n' + f"Translated total {args.processes * args.requests} requests of {args.batch_size} sentences each"):
        # start all processes
        for process in processes:
            process.start()

        # wait for all processes
        for process in processes:
            process.join()
