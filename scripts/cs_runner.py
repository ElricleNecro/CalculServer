#!/usr/bin/env python
# encoding: utf-8

import argparse as ap
import logging as log
import pyinotify as pi
import subprocess as sp

# from CalculServer import Ordonanceur as ordo
from queue import Queue
from threading import Thread


def CreateLog(thread_nb, loglvl):
    _Runner_logger = log.getLogger('Runner_%d' % thread_nb)

    ch = log.StreamHandler()
    ch.setFormatter(
        log.Formatter(
            '%(name)s::%(asctime)s::%(levelname)s: %(message)s',
            "%d-%m-%Y %H:%M:%S"
        )
    )

    _Runner_logger.addHandler(ch)
    _Runner_logger.setLevel(loglvl)

    return _Runner_logger


def Cmd(q, lg):
    while True:
        key = q.get()
        cmd = sp.Popen(
            key
        )
        ret = cmd.wait()
        if ret != 0:
            lg.warn("Command ", cmd, "failed with returned code ", ret)


class EventHandler(pi.ProcessEvent):
    def __init__(self, *args, **kwargs):
        if "loglvl" in kwargs:
            loglvl = kwargs["loglvl"]
            del kwargs["loglvl"]
        else:
            loglvl = log.WARNING

        if "nb_proc" in kwargs:
            nb_proc = kwargs["nb_proc"]
            del kwargs["nb_proc"]
        else:
            nb_proc = 4

        if "script" in kwargs:
            self._cs_script = kwargs["script"]
            del kwargs["script"]

        self._cs_q = Queue()
        for i in range(nb_proc):
            t = Thread(
                target = Cmd(),
                args=[self._cs_q, CreateLog(i, loglvl)],
            )
            t.start()

        super(EventHandler, self).__init__(*args, **kwargs)

    def process_IN_CLOSE_WRITE(self, event):
        self._cs_q.put([self._cs_script, event.pathname])



def arguments():
    parser = ap.ArgumentParser()
    parser.add_argument(
        "--script",
        default="script.sh",
        type=str,
        help="Rendering script.",
    )
    parser.add_argument(
        "--log",
        default="WARNING",
        type=str,
        help="Log level.",
    )
    parser.add_argument(
        "--nb-proc",
        default=4,
        type=int,
        help="Number of thread to use.",
    )
    parser.add_argument(
        "Watch",
        type=str,
        help="Watched directory.",
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = arguments()

    wm = pi.WatchManager()
    mask = pi.IN_CLOSE_WRITE

    handler = EventHandler(
        script=args.script,
        nb_proc=args.nb_proc,
        loglvl=getattr(
            log,
            args.log.upper(),
            None
        )
    )

    notifier = pi.Notifier(wm, handler)
    wdd = wm.add_watch(args.Watch, mask, rec=True)

    notifier.loop()

