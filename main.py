#!/usr/bin/python
# -*- coding: utf-8 -*-
import gconf
from posixpath import join, basename, splitext
import ConfigParser
from optparse import OptionParser
import glob

usage = """
Usage:
gttweak list_themes
gttweak set <theme>
"""

# Funcions for writing to gnome-terminal settings
def set_value(c, k, v):
    if isinstance(v, str):
        c.set_string(k, v)
    elif isinstance(v, bool):
        c.set_bool(k, v)
    elif isinstance(v, int):
        c.set_int(k, v)
    else:
        raise ValueError('Unknown type for key %s: %s', k, type(v))

def read_config(path):
        config = ConfigParser.RawConfigParser()
        config.read(path)
        section = config.sections()[0]
        return dict(config.items(section))

def set_profile(profile, conf):
    c = gconf.client_get_default()
    value_path = lambda k: join('/apps/gnome-terminal', 'profiles', profile, k)
    for k, v in conf.iteritems():
        set_value(c, value_path(k), v)

# Functions for CLI
def get_theme_list():
    res = []
    for files in glob.glob('themes/*.theme'):
        res.append(splitext(basename(files))[0])
    return res

def set_theme(theme):
    config = read_config('themes/%s.theme' % theme)
    set_profile('Default', config)

def leave():
    print usage
    exit(2)

def main():
    parser = OptionParser(description='Set')
    opts, args = parser.parse_args()

    if not args or len(args) > 2: leave()
    command = args[0]
    if command == 'list_themes':
        if len(args) > 1: leave()
        for theme in get_theme_list():
            print theme
    elif command == 'set':
        if len(args) == 1: leave()
        theme = args[1]
        if theme in get_theme_list(): 
            set_theme(theme)
        else:
            print "Theme does not exits"
    else:
        leave()

if __name__ == '__main__':
    main()