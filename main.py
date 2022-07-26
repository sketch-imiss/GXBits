import argparse
import logging

from loader import Dataloader
from odd import Odd
from tow import TOW
from hll import HyperLogLog
from gxbits import GXBits
from utils import *


def get_args():
    parser = argparse.ArgumentParser(description='sketch methods for estimating set difference cardinalities')
    parser.add_argument('--method', default='odd', type=str, help='method name: odd/tow/hll/gxbits')
    parser.add_argument('--dataset', default='synthetic', type=str, help='dataset path or synthetic dataset')
    parser.add_argument('--intersection', default=100, type=int, help='set intersection cardinality')
    parser.add_argument('--difference', default=100, type=int, help='set difference cardinality')
    parser.add_argument('--ratio', default=0.5, type=float, help='ratio used to control cardinalities of two sets')
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
    parser.add_argument('--block_truncated', default=0, type=int, help='whether gxbits sketch is block-truncated or not')
    parser.add_argument('--num_bits', default=2, type=int, help='the number of bits in each segment')
    parser.add_argument('--exp_error', default=0.01, type=float, help='expected error for early stopping')
    parser.add_argument('--rate', default=0.01, type=float, help='iteration rate for newton-raphson method')

    args = parser.parse_args()
    return args


args = get_args()
exp_rounds = args.exp_rounds
lst_all_results = list()

for r in range(exp_rounds):
    dataloader = Dataloader(args.dataset, args.intersection, args.difference, args.ratio, r)
    dict_dataset = dataloader.load_dataset()
    print('dataset generation finished!')

    if args.method == 'odd':
        odd = Odd(dict_dataset, args.odd_size, args.output, r)
        odd.build_sketch()
        lst_result = odd.estimate_difference()
        lst_all_results.extend(lst_result)
    elif args.method == 'tow':
        tow = TOW(dict_dataset, args.tow_size, args.output, r)
        tow.build_sketch()
        lst_result = tow.estimate_difference()
        lst_all_results.extend(lst_result)
    elif args.method == 'hll':
        hll = HyperLogLog(dict_dataset, args.hll_size, args.output, r)
        hll.build_sketch()
        lst_result = hll.estimate_difference()
        lst_all_results.extend(lst_result)
    elif args.method == 'gxbits':
        gxbits = GXBits(dict_dataset, args.gxbits_size, args.probability, args.block_truncated, args.num_bits,
                        args.exp_error, args.rate, args.output, r)
        gxbits.build_sketch()
        lst_result = gxbits.estimate_difference()
        lst_all_results.extend(lst_result)
    else:
        logging.error('Please input the correct method name: odd/tow/hll/gxbits')

if args.dataset == 'synthetic':
    rse = compute_rse(lst_all_results)
    print(rse)
else:
    aare = compute_aare(lst_all_results)
    print(aare)