# ST2 Arduino

Sublime Text 2 plugin for Arduino.

## Notes

Currently, this plugin is only tested and optimized (read works) for OS X. I don't have access to Windows or Linux, so feel free to fork and add that functionality.

## Prerequisites

Dealing with a Makefile on my own was proving too cumbersome, so I've now opted to use the `ino` tool instead.

The best way to install ino is to build from source:

```bash
git clone git://github.com/amperka/ino.git && cd ino
make install
```

However you install ino, make sure that its location is available in your $PATH so this plugin can find it.

Please visit [ino's website](http://inotool.org/) for more information.

## Installation

Download and extract to Sublime Text 2 Packages folder

1. Download a [zipball](https://github.com/geetarista/ST2-Arduino/zipball/master) or [tarball](https://github.com/geetarista/ST2-Arduino/tarball/master)
2. Extract the plugin
3. Copy it to your packages directory:
  * Mac OS X: ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/
  * Linux: ~/.config/sublime-text-2/Packages
  * Windows: %APPDATA%\Sublime Text 2\Packages
4. Rename to Arduino.

## License

MIT. See `LICENSE`.
