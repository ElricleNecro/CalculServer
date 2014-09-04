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
        ret = os.system(
            "scp %s %s:%s" % (
                event.pathname,
                self._cs_host,
                self._cs_path,
            )
        )
        if ret == 0:
            os.remove(event.pathname)

        # print("End Writing:", event.pathname)
        # print("scp %s %s:%s" % (
                # event.pathname,
                # self._cs_host,
                # self._cs_path,
            # )
        # )


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

    wm = pi.WatchManager()
    mask = pi.IN_CLOSE_WRITE

    handler = EventHandler(
        path= args.host_path,
        host = args.host,
    )

    notifier = pi.Notifier(wm, handler)
    wdd = wm.add_watch(args.Watch, mask, rec=True)

    notifier.loop()
