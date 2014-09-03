#!/usr/bin/env python3
# encoding: utf-8

import argparse as ap
import os
import pyinotify as pi


class EventHandler(pi.ProcessEvent):
    def __init__(self, *args, **kwargs):
        if "host" in kwargs:
            self._cs_host = kwargs["host"]
            del kwargs["host"]
        if "path" in kwargs:
            self._cs_path = kwargs["path"]
            del kwargs["path"]

        super(EventHandler, self).__init__(*args, **kwargs)

    def process_IN_CLOSE_WRITE(self, event):
        print("End Writing:", event.pathname)
        print("scp %s %s:%s" % (
                event.pathname,
                self._cs_host,
                self._cs_path,
            )
        )


def arguments():
    parser = ap.ArgumentParser()
    parser.add_argument(
        "--host-path",
        default="/UMA/tmp/",
    )
    parser.add_argument(
        "--host",
        default="medoc",
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = arguments()

    wm = pi.WatchManager()
    mask = pi.IN_CLOSE_WRITE

    handler = EventHandler(
        path= args.host_path,
        host = args.host,
    )

    notifier = pi.Notifier(wm, handler)
    wdd = wm.add_watch("/tmp/test", mask, rec=True)

    notifier.loop()
