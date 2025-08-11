#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Rotating 3D box wireframe & color dithering.

Adapted from:
http://codentronix.com/2011/05/12/rotating-3d-cube-using-python-and-pygame/
"""

import sys
import math
from operator import itemgetter
from demo_opts import get_device
from luma.core.render import canvas
from luma.core.sprite_system import framerate_regulator

import time
from pathlib import Path
from datetime import datetime
from PIL import ImageFont
import psutil
import subprocess as sp
import socket
from collections import OrderedDict

from smbus2 import SMBus


def radians(degrees):
    return degrees * math.pi / 180


class point(object):

    def __init__(self, x, y, z):
        self.coords = (x, y, z)
        self.xy = (x, y)
        self.z = z

    def rotate_x(self, angle):
        x, y, z = self.coords
        rad = radians(angle)
        c = math.cos(rad)
        s = math.sin(rad)
        return point(x, y * c - z * s, y * s + z * c)

    def rotate_y(self, angle):
        x, y, z = self.coords
        rad = radians(angle)
        c = math.cos(rad)
        s = math.sin(rad)
        return point(z * s + x * c, y, z * c - x * s)

    def rotate_z(self, angle):
        x, y, z = self.coords
        rad = radians(angle)
        c = math.cos(rad)
        s = math.sin(rad)
        return point(x * c - y * s, x * s + y * c, z)

    def project(self, size, fov, viewer_distance):
        x, y, z = self.coords
        factor = fov / (viewer_distance + z)
        return point(x * factor + size[0] / 2, -y * factor + size[1] / 2, z)


def sine_wave(min, max, step=1):
    angle = 0
    diff = max - min
    diff2 = diff / 2
    offset = min + diff2
    while True:
        yield angle, offset + math.sin(radians(angle)) * diff2
        angle += step


def get_temp():
    temp = float(sp.getoutput("vcgencmd measure_temp").split("=")[1].split("'")[0])
    return temp


def get_cpu():
    return psutil.cpu_percent()


def get_mem():
    return psutil.virtual_memory().percent


def get_disk_usage():
    usage = psutil.disk_usage("/")
    return usage.used / usage.total * 100


def get_uptime():
    uptime = ("%s" % (datetime.now() - datetime.fromtimestamp(psutil.boot_time()))).split(".")[0]
    return "UpTime: %s" % (uptime)


def find_single_ipv4_address(addrs):
    for addr in addrs:
        if addr.family == socket.AddressFamily.AF_INET:  # IPv4
            return addr.address


def get_ipv4_address(interface_name=None):
    if_addrs = psutil.net_if_addrs()

    if isinstance(interface_name, str) and interface_name in if_addrs:
        addrs = if_addrs.get(interface_name)
        address = find_single_ipv4_address(addrs)
        return address if isinstance(address, str) else ""
    else:
        if_stats = psutil.net_if_stats()
        # remove loopback
        if_stats_filtered = {key: if_stats[key] for key, stat in if_stats.items() if "loopback" not in stat.flags}
        # sort interfaces by
        # 1. Up/Down
        # 2. Duplex mode (full: 2, half: 1, unknown: 0)
        if_names_sorted = [stat[0] for stat in sorted(if_stats_filtered.items(), key=lambda x: (x[1].isup, x[1].duplex), reverse=True)]
        if_addrs_sorted = OrderedDict((key, if_addrs[key]) for key in if_names_sorted if key in if_addrs)

        for _, addrs in if_addrs_sorted.items():
            address = find_single_ipv4_address(addrs)
            if isinstance(address, str):
                return address

        return ""


def get_ip(network_interface_name):
    return "IP: %s" % (get_ipv4_address(network_interface_name))


def format_percent(percent):
    return "%5.1f" % (percent)


def draw_text(draw, margin_x, line_num, text):
    draw.text((margin_x, margin_y_line[line_num]), text, font=font_default, fill="white")


def draw_bar(draw, line_num, percent):
    top_left_y = margin_y_line[line_num] + bar_margin_top
    draw.rectangle((margin_x_bar, top_left_y, margin_x_bar + bar_width, top_left_y + bar_height), outline="white")
    draw.rectangle((margin_x_bar, top_left_y, margin_x_bar + bar_width * percent / 100, top_left_y + bar_height), fill="white")


def draw_bar_full(draw, line_num):
    top_left_y = margin_y_line[line_num] + bar_margin_top
    draw.rectangle((margin_x_bar, top_left_y, margin_x_bar + bar_width_full, top_left_y + bar_height), fill="white")
    draw.text((65, top_left_y - 2), "100 %", font=font_full, fill="black")


def stats(device):
    with canvas(device) as draw:
        temp = get_temp()
        draw_text(draw, 0, 0, "Temp")
        draw_text(draw, margin_x_figure, 0, "%s'C" % (format_percent(temp)))

        cpu = get_cpu()
        draw_text(draw, 0, 1, "CPU")
        if cpu < 100:
            draw_text(draw, margin_x_figure, 1, "%s %%" % (format_percent(cpu)))
            draw_bar(draw, 1, cpu)
        else:
            draw_bar_full(draw, 1)

        mem = get_mem()
        draw_text(draw, 0, 2, "Mem")
        if mem < 100:
            draw_text(draw, margin_x_figure, 2, "%s %%" % (format_percent(mem)))
            draw_bar(draw, 2, mem)
        else:
            draw_bar_full(draw, 2)

        disk = get_disk_usage()
        draw_text(draw, 0, 3, "Disk")
        if disk < 100:
            draw_text(draw, margin_x_figure, 3, "%s %%" % (format_percent(disk)))
            draw_bar(draw, 3, disk)
        else:
            draw_bar_full(draw, 3)

        if datetime.now().second % (toggle_interval_seconds * 2) < toggle_interval_seconds:
            draw_text(draw, 0, 4, get_uptime())
        else:
            draw_text(draw, 0, 4, get_ip(network_interface_name))


font_size = 12
font_size_full = 10
margin_y_line = [0, 13, 25, 38, 51]
margin_x_figure = 78
margin_x_bar = 31
bar_width = 52
bar_width_full = 95
bar_height = 8
bar_margin_top = 3
toggle_interval_seconds = 4


# None : find suitable IPv4 address among all network interfaces
# or specify the desired interface name as string.
network_interface_name = None


device = get_device()
font_default = ImageFont.truetype(str(Path(__file__).resolve().parent.joinpath("fonts", "DejaVuSansMono.ttf")), font_size)
font_full = ImageFont.truetype(str(Path(__file__).resolve().parent.joinpath("fonts", "DejaVuSansMono.ttf")), font_size_full)

address = 0x70
# channel   76543210
channel2 = 0b00001000 # channel 1
channel3 = 0b00010000
bus = SMBus(1)

def box_main(num_iterations=sys.maxsize):

    regulator = framerate_regulator(fps=30)

    vertices = [
        point(-1, 1, -1),
        point(1, 1, -1),
        point(1, -1, -1),
        point(-1, -1, -1),
        point(-1, 1, 1),
        point(1, 1, 1),
        point(1, -1, 1),
        point(-1, -1, 1)
    ]

    faces = [
        ((0, 1, 2, 3), "red"),
        ((1, 5, 6, 2), "green"),
        ((0, 4, 5, 1), "blue"),
        ((5, 4, 7, 6), "magenta"),
        ((4, 0, 3, 7), "yellow"),
        ((3, 2, 6, 7), "cyan")
    ]

    a, b, c = 0, 0, 0

    for angle, dist in sine_wave(8, 40, 1.5):
        bus.write_byte(address, channel3)
        time.sleep(0.005)
        stats(device)
        bus.write_byte(address, channel2)
        time.sleep(0.005)
        with regulator:
            num_iterations -= 1
            if num_iterations == 0:
                break

            t = [v.rotate_x(a).rotate_y(b).rotate_z(c).project(device.size, 256, dist)
                for v in vertices]

            depth = []
            for idx, face in enumerate(faces):
                v1, v2, v3, v4 = face[0]
                avg_z = (t[v1].z + t[v2].z + t[v3].z + t[v4].z) / 4.0
                depth.append((idx, avg_z))

            with canvas(device, dither=True) as draw:
                for idx, depth in sorted(depth, key=itemgetter(1), reverse=True)[3:]:
                    (v1, v2, v3, v4), color = faces[idx]

                    if angle // 720 % 2 == 0:
                        fill, outline = color, color
                    else:
                        fill, outline = "black", "white"

                    draw.polygon(t[v1].xy + t[v2].xy + t[v3].xy + t[v4].xy, fill, outline)

            a += 0.3
            b -= 1.1
            c += 0.85


if __name__ == "__main__":
    bus.write_byte(address, channel2)
    try:
        box_main()
    except KeyboardInterrupt:
        pass


