import sublime
import sublime_plugin

import os
import thread
import subprocess
import sys
# import re

PLUGIN_DIRECTORY = os.getcwd().replace(os.path.normpath(os.path.join(os.getcwd(), '..', '..')) + os.path.sep, '').replace(os.path.sep, '/')
PLUGIN_PATH = os.getcwd().replace(os.path.join(os.getcwd(), '..', '..') + os.path.sep, '').replace(os.path.sep, '/')
RESULT_VIEW_NAME = 'monitor_result_view'

PACKAGES_DIR = sublime.packages_path()
ARDUINO_DIR = '/Applications/Arduino.app/Contents/Resources/Java'
REFERENCE_DIR = '%s/reference' % ARDUINO_DIR
KEYWORDS_FILE = '%s/lib/keywords.txt' % ARDUINO_DIR
CSS_FILE = "%s/arduinoUno.css" % REFERENCE_DIR
USER_DIR = '${HOME}/Documents/Arduino/'

def plugin_file(name):
    return os.path.join(PLUGIN_PATH, name)

class CompileCommand(sublime_plugin.WindowCommand):
    """ Compile the current file """
    def run(self):
        self.window.run_command('set_build_system', {
          'file': "%s/Arduino-Compile.sublime-build" % PLUGIN_PATH
        })
        self.window.run_command('build')

class UploadCommand(sublime_plugin.WindowCommand):
    """ Upload the current sketch to the board """
    def run(self):
        self.window.run_command('set_build_system', {
          'file': "%s/Arduino-Upload.sublime-build" % PLUGIN_PATH
        })
        self.window.run_command('build')

class CompileUploadCommand(sublime_plugin.WindowCommand):
    """ Upload and compile the current sketch to the board """
    def run(self):
        self.window.run_command('set_build_system', {
          'file': "%s/Arduino-Compile-Upload.sublime-build" % PLUGIN_PATH
        })
        self.window.run_command('build')

class CleanCommand(sublime_plugin.WindowCommand):
    """ Clean the current file """
    def run(self):
        self.window.run_command('set_build_system', {
          'file': "%s/Arduino-Clean.sublime-build" % PLUGIN_PATH
        })
        self.window.run_command('build')

class NewSketchCommand(sublime_plugin.WindowCommand):
    """ Create new sketch file from template """
    def run(self):
        template = open(plugin_file('sketch_template'), 'r').read()
        file = self.window.new_file()
        edit = file.begin_edit()
        file.insert(edit, 0, template)
        file.end_edit(edit)

class OpenArduinoDirectoryCommand(sublime_plugin.WindowCommand):
    """ Open Arduino's application directory """
    def run(self):
        if sys.platform == 'darwin':
            path = ARDUINO_DIR
            subprocess.check_call(['open', '--', path])

class OpenArduinoLibrariesCommand(sublime_plugin.WindowCommand):
    """ Open Arduino's built-in libraries """
    def run(self):
        if sys.platform == 'darwin':
            path = '%s/libraries' % ARDUINO_DIR
            subprocess.check_call(['open', '--', path])

class OpenArduinoExamplesCommand(sublime_plugin.WindowCommand):
    """ Open Arduino's example sketches directory """
    def run(self):
        if sys.platform == 'darwin':
            path = '%s/examples' % ARDUINO_DIR
            subprocess.check_call(['open', '--', path])

class OpenUserArduinoDirectoryCommand(sublime_plugin.WindowCommand):
    """ Open user's arduino directory """
    def run(self):
        path = os.getenv('HOME') + '/Documents/Arduino'
        subprocess.check_call(['open', '--', path])

class OpenUserArduinoLibrariesCommand(sublime_plugin.WindowCommand):
    """ Open user's library files """
    def run(self):
        path = os.getenv('HOME') + '/Documents/Arduino/libraries'
        subprocess.check_call(['open', '--', path])

# class WatchSerialPortCommand(sublime_plugin.WindowCommand):
#     """ Watch serial port for activity """
#     def run(self):
#         script = plugin_file('Support/Monitor')
#         subprocess.call([script], shell=True)

class LocalHelpCommand(sublime_plugin.TextCommand):
    """ Open Arduino help for currently selected word """
    def run(self, edit):
        loop = 'loop'
        sel = self.view.sel()[0]
        if not sel.empty():
            word = self.view.substr(sel)
        else:
            word = ""

        lines = [line.split() for line in open(KEYWORDS_FILE)]
        keywords = [l for l in lines if ((len(l) >= 2) or (l and l[0] != "#"))]
        for kw in keywords:
            if word == kw[0]:
                html_file = '%s/%s.html' % (REFERENCE_DIR, kw[-1])

        if 'html_file' in locals():
            try:
                subprocess.check_call(['open', html_file])
                # Will add this if sublime ever gets formatted output window
                # html = open(html_file).read()
                # css = open(CSS_FILE).read() + """
                #     #wikitext p:first-child,
                #     #pageheader,
                #     #pagenav,
                #     #pagefooter {
                #         display: none;
                #     }
                #     #page {
                #         width: 100%;
                #     }
                # """
                # html = re.sub('<link.*arduino.*\.css.*?>', "<style type='text/css'>#{css}</style>", html, re.S|re.I)
            except Exception, e:
                print "failed to open html"
        else:
            print 'No documentation found for "%s"' % word
