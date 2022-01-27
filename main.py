import argparse
import logging

from loader import Dataloader
from odd import Odd
from tow import TOW
from hll import HyperLogLog
from gxbits import GXBits


def get_args():
    parser = argparse.ArgumentParser(description='sketch methods for estimating set difference cardinalities')
    parser.add_argument('--method', default='odd', type=str, help='method name: odd/tow/hll/gxbits')
    parser.add_argument('--dataset', default='synthetic', type=str, help='dataset path or synthetic dataset')
    parser.add_argument('--intersection', default=100, type=int, help='set intersection cardinality')
    parser.add_argument('--difference', default=100, type=int, help='set difference cardinality')
    parser.add_argument('--exp_rounds', default=1, type=int, help='the number of experimental rounds')
    parser.add_argument('--output', default='result/', type=str, help='output directory')

    # odd sketch
    parser.add_argument('--odd_size', default=1000, type=int, help='size of odd sketch')

    # tug of war sketch
    parser.add_argument('--tow_size', default=1000, type=int, help='size of tug of war sketch')

    # hyperloglog sketch
    parser.add_argument('--hll_size', default=1000, type=int, help='size of hyperloglog sketch')

    # gxbits sketch
    parser.add_argument('--gxbits_size', default=1000, type=int, help='size of gxbits sketch')
    parser.add_argument('--probability', default=0.15, type=float, help='parameter of geometric distribution')
    parser.add_argument('--block_truncated', default=0, type=int, help='whether gxbits sketch is block truncated or not')
    parser.add_argument('--num_bits', default=2, type=int, help='the number of bits in each segment')
    parser.add_argument('--num_iterations', default=100, type=int, help='the number of iterations for newton-raphson method')
    parser.add_argument('--exp_error', default=0.001, type=float, help='expected error for early stopping')

    args = parser.parse_args()
    return args


args = get_args()
exp_rounds = args.exp_rounds
for r in range(exp_rounds):
    dataloader = Dataloader(args.dataset, args.intersection, args.difference, r)
    dict_dataset = dataloader.load_dataset()

    if args.method == 'odd':
        odd = Odd(dict_dataset, args.odd_size, args.output, r)
        odd.build_sketch()
        odd.estimate_difference()
    elif args.method == 'tow':
        tow = TOW(dict_dataset, args.tow_size, args.output, r)
        tow.build_sketch()
        tow.estimate_difference()
    elif args.method == 'hll':
        hll = HyperLogLog(dict_dataset, args.hll_size, args.output, r)
        hll.build_sketch()
        hll.estimate_difference()
    elif args.method == 'gxbits':
        gxbits = GXBits(dict_dataset, args.gxbits_size, args.probability, args.block_truncated, args.num_bits,
                        args.num_iterations, args.exp_error, args.output, r)
        gxbits.build_sketch()
        gxbits.estimate_difference()
    else:
        logging.error('Please input the correct method name: odd/tow/hll/gxbits')