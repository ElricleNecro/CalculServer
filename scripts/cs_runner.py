#!/usr/bin/env python
# encoding: utf-8

import argparse as ap
import os
import pyinotify as pi


class EventHandler(pi.ProcessEvent):
    def __init__(self, *args, **kwargs):
        if "script" in kwargs:
            self._cs_script = kwargs["script"]
            del kwargs["script"]

        super(EventHandler, self).__init__(*args, **kwargs)

    def process_IN_CLOSE_WRITE(self, event):
        ret = os.system(
            self._cs_script + " " + event.pathname
        )
        if ret == 0:
            os.remove(event.pathname)



def arguments():
    parser = ap.ArgumentParser()
    parser.add_argument(
        "--script",
        default="script.sh",
        type=str,
        help="Rendering script.",
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
    )

    notifier = pi.Notifier(wm, handler)
    wdd = wm.add_watch(args.Watch, mask, rec=True)

    notifier.loop()

