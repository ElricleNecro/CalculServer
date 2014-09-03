#!/usr/bin/env python3
# encoding: utf-8

import pyinotify as pi


class EventHandler(pi.ProcessEvent):
    def process_IN_CREATE(self, event):
        print("Creating:", event.pathname)

    def process_IN_CLOSE_WRITE(self, event):
        print("Creating:", event.pathname)

if __name__ == '__main__':
    wm = pi.WatchManager()
    mask = pi.IN_CREATE | pi.IN_CLOSE_WRITE

    handler = EventHandler()

    notifier = pi.Notifier(wm, handler)
    wdd = wm.add_watch("/tmp/test", mask, rec=True)

    notifier.loop()
