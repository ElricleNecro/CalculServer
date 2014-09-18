#!/usr/bin/env python3
# encoding: utf-8

import argparse as ap
import os

from os import path
from glob import glob
from time import sleep


def arguments():
    parser = ap.ArgumentParser()
    parser.add_argument(
        "--script",
        default="script.sh",
        type=str,
        help="Script to execute."
    )
    parser.add_argument(
        "--motif",
        default="None_*",
        type=str,
        help="Searched file are given by this motif."
    )
    parser.add_argument(
        "Watch",
        type=str,
        help="Watched directory.",
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = arguments()

    while True:
        lst = sorted(glob(path.join(args.Watch, args.motif)))
        for f in lst:
            ret = os.system(
                args.script + " " + f
            )
        lst = []
        sleep(60)

