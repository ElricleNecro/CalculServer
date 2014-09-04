#!/usr/bin/env python
# encoding: utf-8

import argparse as ap
import os
import pyinotify as pi
import yaml

from os import path


class EventHandler(pi.ProcessEvent):
    def __init__(self, *args, **kwargs):
        if "cfg" in kwargs:
            self._cs_cfg = kwargs["cfg"]
            del kwargs["cfg"]

        if "conf" in kwargs:
            self._cs_conf = kwargs["conf"]
            del kwargs["conf"]

        if "script" in kwargs:
            self._cs_script = kwargs["script"]
            del kwargs["script"]

        if "output_path" in kwargs:
            self._cs_output_path = kwargs["output_path"]
            del kwargs["output_path"]

        super(EventHandler, self).__init__(*args, **kwargs)

    def process_IN_CLOSE_WRITE(self, event):
        self._cs_conf["input"] = event.pathname
        self._cs_conf["output_name"] = path.join(
                self._cs_output_path,
                path.basename(
                    event.pathname
                )
        )

        with open(self._cs_cfg, "w") as f:
            f.writelines(
                yaml.dump(
                    self._cs_conf,
                )
            )

        # os.system
        print(
            "RENDER_CONFIG=%s blender -b --python %s" % (
                self._cs_cfg,
                self._cs_script,
            )
        )



def arguments():
    parser = ap.ArgumentParser()
    parser.add_argument(
        "-c",
        "--cfg",
        default="cfg",
        type=str,
        help="Rendering configuration file.",
    )
    parser.add_argument(
        "--script",
        default="render_v4.py",
        type=str,
        help="Rendering script.",
    )
    parser.add_argument(
        "--conf",
        default="render.yml",
        type=str,
        help="Template configuration file.",
    )
    parser.add_argument(
        "-o",
        "--output-path",
        default=".",
        type=str,
        help="Ouput directory for images.",
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
        conf=yaml.load(open(args.conf, "r")),
        output_path=args.output_path,
        cfg=args.cfg,
        script=args.script,
    )

    notifier = pi.Notifier(wm, handler)
    wdd = wm.add_watch(args.Watch, mask, rec=True)

    notifier.loop()

