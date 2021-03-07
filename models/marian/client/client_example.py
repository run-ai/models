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

def run(lines, hostname, port, requests, sentences, connect_per, output, seed):
    random.seed(args.seed)

    ws = None

    def connect():
        nonlocal ws
        ws = create_connection("ws://{}:{}/translate".format(hostname, port))

    def close():
        nonlocal ws
        ws.close()

    if connect_per == 'process':
        connect()

    def translate(batch):
        nonlocal ws

        if connect_per == 'request':
            connect()

        with Timer(f"Process (pid {os.getpid()}) translated a single request of {sentences} sentences", active=(output == 'verbose')):
            ws.send(batch)
            result = ws.recv()
            # print(result.rstrip())

        if connect_per == 'request':
            close()

    with Timer(f"** Process (pid {os.getpid()}) translated {requests} requests", active=(output == 'verbose')):
        request = 0
        while request < requests or requests == -1:
            request += 1

            # build a batch of random sentences
            batch = ""
            for line in random.sample(lines, sentences):
                batch += line.decode('utf-8') if sys.version_info < (3, 0) else line

            # translate the batch
            translate(batch)

    if connect_per == 'process':
        close()

def calculate_metrics(total_ms):
    total_seconds = float(total_ms) / 1000.0
    total_requests = processes * requests
    total_sentences = total_requests * sentences

    # avg latency
    latency_request = total_ms / float(total_requests)
    latency_sentence = total_ms / float(total_sentences)

    # throughput
    throughput_requests = float(total_requests) / total_seconds
    throughput_sentences = float(total_sentences) / total_seconds

    return total_requests, total_sentences, latency_request, latency_sentence, throughput_requests, throughput_sentences

def impl(lines, processes, requests, sentences, args):
    if args.output == 'verbose':
        print(f"Launching {processes} processes; each process will send {requests} requests of {sentences} sentences; connecting per {args.connect_per}.")

    # create child processes
    ps = [Process(target=run, args=(lines, args.hostname, args.port, requests, sentences, args.connect_per, args.output, args.seed)) for _ in range(processes)]

    def text(total_ms):
        total_requests, total_sentences, latency_request, latency_sentence, throughput_requests, throughput_sentences = calculate_metrics(total_ms)

        print('-' * 100)
        print(f"Translated total {total_requests} requests of {sentences} sentences each from {processes} processes (total {total_sentences} sentences)")
        print(f"Total time: {total_ms} ms")
        print("Average latency:")
        print(f"  Request: {latency_request:.2f} ms")
        print(f"  Sentence: {latency_sentence:.2f} ms")
        print("Throughput:")
        print(f"  {throughput_requests:.2f} requests/second")
        print(f"  {throughput_sentences:.2f} sentences/second")

    def csv(total_ms):
        values = [processes, requests, sentences]
        values.extend(calculate_metrics(total_ms))
        print(','.join([str(_) for _ in values]))

    with Timer(csv if args.output == 'csv' else text):
        # start all processes
        for process in ps:
            process.start()

        # wait for all processes
        for process in ps:
            process.join()

if __name__ == "__main__":
    # handle command-line options
    parser = argparse.ArgumentParser()
    parser.add_argument("--hostname", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=8888)
    parser.add_argument("--processes", type=int, default=[5], nargs='*')
    parser.add_argument("--requests", type=int, default=[20], nargs='*')
    parser.add_argument("--sentences", type=int, default=[5], nargs='*')
    parser.add_argument("--connect-per", choices=['process', 'request'], default='request')
    parser.add_argument("--output", choices=['text', 'verbose', 'csv'], default='text')
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    # read text lines
    lines = [line.strip() for line in sys.stdin.readlines() if len(line) > 0]

    if args.output == 'csv':
        print(','.join(['Processes', 'Requests', 'Sentences', 'Total requests', 'Total sentences', 'Avg. request latency', 'Avg. sentence latency', 'Request throughput', 'Sentence throughput']))

    for processes in args.processes:
        for requests in args.requests:
            for sentences in args.sentences:
                impl(lines, processes, requests, sentences, args)
