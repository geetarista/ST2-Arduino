import sublime
import sublime_plugin

import os
import thread
import subprocess
import sys

PLUGIN_DIRECTORY = os.getcwd().replace(os.path.normpath(os.path.join(os.getcwd(), '..', '..')) + os.path.sep, '').replace(os.path.sep, '/')
PLUGIN_PATH = os.getcwd().replace(os.path.join(os.getcwd(), '..', '..') + os.path.sep, '').replace(os.path.sep, '/')

packages_dir = sublime.packages_path()
arduino_dir = '/Applications/Arduino.app/Contents/Resources/Java/'
make_path = '%shardware/tools/avr/bin/make' % arduino_dir
user_dir = '${HOME}/Documents/Arduino/'

def plugin_file(name):
    return os.path.join(PLUGIN_PATH, name)

class NewSketchCommand(sublime_plugin.WindowCommand):
    def run(self):
        template = open(plugin_file('sketch_template'), 'r').read()
        file = self.window.new_file()
        edit = file.begin_edit()
        file.insert(edit, 0, template)
        file.end_edit(edit)

class OpenArduinoDirectory(sublime_plugin.WindowCommand):
    def run(self):
        if sys.platform == 'darwin':
            path = arduino_dir
            subprocess.check_call(['open', '--', path])

class OpenArduinoLibraries(sublime_plugin.WindowCommand):
    def run(self):
        if sys.platform == 'darwin':
            path = '%slibraries/' % arduino_dir
            subprocess.check_call(['open', '--', path])

class OpenArduinoExamples(sublime_plugin.WindowCommand):
    def run(self):
        if sys.platform == 'darwin':
            path = '%sexamples/' % arduino_dir
            subprocess.check_call(['open', '--', path])

class OpenUserArduinoDirectory(sublime_plugin.WindowCommand):
    def run(self):
        path = os.getenv('HOME') + '/Documents/Arduino'
        subprocess.check_call(['open', '--', path])

class OpenUserArduinoLibraries(sublime_plugin.WindowCommand):
    def run(self):
        path = os.getenv('HOME') + '/Documents/Arduino/libraries'
        subprocess.check_call(['open', '--', path])
