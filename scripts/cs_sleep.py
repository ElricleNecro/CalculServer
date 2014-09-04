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
        "--host-path",
        default="/UMA/tmp/",
        type=str,
    )
    parser.add_argument(
        "--host",
        default="medoc",
        type=str,
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
        lst = sorted(glob(path.join(args.Watch, "None_*")))
        for f in lst:
            ret = os.system(
                "scp %s %s:%s" % (
                    f,
                    args.host,
                    args.host_path,
                )
            )
            if ret == 0:
                os.remove(f)
        lst = []
        sleep(60)

