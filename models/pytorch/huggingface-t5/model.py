import argparse
import os
import time

from datasets import load_dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default='t5-3b', choices=['t5-small', 't5-base', 't5-large', 't5-3b'])
    parser.add_argument('--split', default='test', choices=['train', 'test', 'validation'])
    parser.add_argument('--split-percents', default=10, type=int)
    parser.add_argument('--verbose', action='store_true', default=False)
    parser.add_argument('--time-window', default=5)
    args = parser.parse_args()

    dataset = load_dataset("wmt14", 'de-en', split=f'{args.split}[:{args.split_percents}%]')

    tokenizer = T5Tokenizer.from_pretrained(args.model)
    model = T5ForConditionalGeneration.from_pretrained(args.model)

    model = model.cuda()

    total_start = time.time()

    measure_start = total_start
    measure_sentences = 1

    for index, sample in enumerate(dataset):
        en = sample['translation']['en']
        inputs = tokenizer(en, return_tensors='pt').to('cuda')
        input_ids = inputs.input_ids
        outputs = model.generate(input_ids)
        de = tokenizer.decode(outputs[0], skip_special_tokens=True)

        if args.verbose:
            print(en)
            print(de)
            print()
        else:
            measure_seconds = time.time() - measure_start

            msg = f'Sample: {index + 1}/{len(dataset)}; Throughput: {measure_sentences/measure_seconds:.2f} sentences/second'
            if index > 0:
                msg = f'\r{msg}'
            print(msg, end='')

            if measure_seconds > args.time_window:
                measure_start = time.time()
                measure_sentences = 1
            else:
                measure_sentences += 1

    total_seconds = time.time() - total_start
    total_sentences = len(dataset)

    print()
    print(f'Total time: {total_seconds:.2f} seconds')
    print(f'Throughput: {total_sentences/total_seconds:.2f} sentences/second')
