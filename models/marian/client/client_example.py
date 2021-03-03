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
    def __init__(self, msg, active=True):
        self._msg = msg
        self._active = active

    def __enter__(self):
        self._start = datetime.datetime.now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._active:
            end = datetime.datetime.now()
            ms = int((end - self._start).total_seconds() * 1000)
            if isinstance(self._msg, str):
                print(f"{end.strftime('%H:%M:%S.%f')[:-3]}\t{self._msg} in {ms} ms")
            else:
                self._msg(ms)

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

        with Timer(f"Process (pid {os.getpid()}) translated a single request of {args.sentences} sentences", active=args.verbose):
            ws.send(batch)
            result = ws.recv()
            # print(result.rstrip())

        if args.connect_per == 'request':
            close()

    with Timer(f"** Process (pid {os.getpid()}) translated {args.requests} requests", active=args.verbose):
        request = 0
        while request < args.requests or args.requests == -1:
            request += 1

            # build a batch of random sentences
            batch = ""
            for line in random.sample(lines, args.sentences):
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
    parser.add_argument("-b", "--sentences", type=int, default=5)
    parser.add_argument("--processes", type=int, default=5)
    parser.add_argument("--requests", type=int, default=20)
    parser.add_argument("--connect-per", choices=['process', 'request'], default='request')
    parser.add_argument("--verbose", action='store_true')
    args = parser.parse_args()

    # read text lines
    lines = sys.stdin.readlines()

    if args.verbose:
        print(f"Launching {args.processes} processes; each process will send {args.requests} requests of {args.sentences} sentences; connecting per {args.connect_per}.")

    # create child processes
    processes = [Process(target=run, args=(args, lines)) for _ in range(args.processes)]

    def summary(total_ms):
        # total
        total_seconds = float(total_ms) / 1000.0
        total_requests = args.processes * args.requests
        total_sentences = total_requests * args.sentences
        print(f"Translated total {total_requests} requests of {args.sentences} sentences each from {args.processes} processes (total {total_sentences} sentences)")
        print(f"Total time: {total_ms} ms")

        # avg latency
        latency_request = total_ms / float(total_requests)
        latency_sentence = total_ms / float(total_sentences)
        print("Average latency:")
        print(f"  Request: {latency_request:.2f} ms")
        print(f"  Sentence: {latency_sentence:.2f} ms")

        # throughput
        throughput_requests = float(total_requests) / total_seconds
        throughput_sentences = float(total_sentences) / total_seconds
        print("Throughput:")
        print(f"  {throughput_requests:.2f} requests/second")
        print(f"  {throughput_sentences:.2f} sentences/second")

    with Timer(summary):
        # start all processes
        for process in processes:
            process.start()

        # wait for all processes
        for process in processes:
            process.join()
