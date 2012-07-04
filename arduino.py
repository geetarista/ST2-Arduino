import os
import subprocess
import sublime
import sublime_plugin

def compile():
    /Applications/Arduino.app/Contents/Resources/Java/hardware/tools/avr/bin/make -e -f "$TM_BUNDLE_SUPPORT/Makefile"

def new_sketch():
    template="""
    /*
      ${TM_NEW_FILE_BASENAME}
      Created by ${TM_FULLNAME}
    */

    void setup () {
        //
    }

    void loop() {
        //
    }
    """
    file = new_file()
    edit = file.begin_edit()
    insert(edit, 0, template)


def local_help():
    #!/usr/bin/env ruby

tm_word = STDIN.read
html_file = nil

arduino_dir = "/Applications/Arduino.app/Contents/Resources/Java"
reference_dir = "#{arduino_dir}/reference"
keywords_file = "#{arduino_dir}/lib/keywords.txt"
css_file = "#{reference_dir}/arduinoUno.css"

keywords = open(keywords_file).each_line.map {|line| line.split}
keywords.reject! do |kw|
    kw.size &lt; 2 or kw.first == "#"
end
keywords.each {|kw| html_file = "#{reference_dir}/#{kw.last}.html" if tm_word == kw.first }

if html_file
    begin
        html = open(html_file).read
        css = open(css_file).read + &lt;&lt;-NEWCSS
            #wikitext p:first-child,
            #pageheader,
            #pagenav,
            #pagefooter {
                display: none;
            }

            #page {
                width: 100%;
            }

NEWCSS
        puts html.sub! /<link.*arduino.*\.css.*?&gt;/mi, "<style type='text/css'>#{css}</style>"

    rescue Errno::ENOENT
        # do nothing
    end

    exit
end

puts "No documentation found for '#{tm_word}'!"











def open_arduino_libraries():
    open /Applications/Arduino.app/Contents/Resources/Java/libraries/

def upload():
    /Applications/Arduino.app/Contents/Resources/Java/hardware/tools/avr/bin/make -e -f "$TM_BUNDLE_SUPPORT/Makefile" upload

def watch_serial_port():
    osascript -e 'tell application "Terminal" to do script "\"${TM_BUNDLE_SUPPORT}/Monitor\""'
