import sublime
import sublime_plugin

import os
import thread
import subprocess

class NewSketchCommand(sublime_plugin.WindowCommand):
  def run(self):
    template = open(sublime.packages_path() + '/Arduino/sketch_template', 'r').read()
    file = self.window.new_file()
    edit = file.begin_edit()
    file.insert(edit, 0, template)
    file.end_edit(edit)
