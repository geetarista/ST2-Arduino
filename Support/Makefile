# ORIGINAL: http://www.arduino.cc/playground/uploads/Learning/Makefile

# Makefile for building Arduino sketches with Arduino 1.0.
#
# Makefile-arduino v0.8 by Akkana Peck <akkana@shallowsky.com>
# Adapted from a long-ago Arduino 0011 Makefile by mellis, eighthave, oli.keller
# using contributions from Santiago Reig, Pascal de Bruijn,
# and Bernard Pratz <guyzmo@hackable-devices.org>
#
# This Makefile allows you to build sketches from the command line
# without the Arduino environment (or Java).
#
# Detailed instructions for using this Makefile:
#
#  1. Copy this file into the folder with your sketch.
#     There should be a file with the extension .ino (e.g. blink.ino).
#     cd into this directory. Be sure your the filename and .ino file
#     have the same name, e.g. blink/blink.ino.
#
#  2. Modify the line containg "ARDUINO_DIR" to point to the directory that
#     contains the Arduino installation (for example, under Mac OS X, this
#     might be /Applications/arduino-1.0). If it's in your home directory,
#     you can include $(HOME) as part of the path.
#
#  3. Set MODEL to your Arduino model.
#     Tested so far on uno, atmega328 (several variants), diecimila and mega,
#     but there are lots of other options:
#     Use the "make list" command to know all the available models
#
#     If you want to compile against ATTiny, see ATTINY_DIR below.
#
#     If needed, you can override MODEL on the command line, e.g.
#     MODEL=atmega328 make upload
#     You can also override PORT.
#
#  4. Run "make" to compile/verify your program.
#
#  5. Run "make download" (and reset your Arduino if it requires it)
#     to download your program to the Arduino.
#     If you prefer typing "make upload", you can do that too.
#
# Nota Bene:
# if reset does not work, try adding RESET_MODE='python' or RESET_MODE='perl'
# to your environment or on the command line.
#  * Perl version needs libdevice-serialport-perl
#  * Python version needs python-serial

############################################################################
# Project's settings
############################################################################

VERSION = 0.1

# Standard Arduino libraries it will import, e.g. LiquidCrystal:
ARDLIBS =

# Local user-specified libraries (in ~/sketchbook/libraries/):
USERLIBS =

# Arduino model:
# You can set this to be a string, such as uno, atmega328, diecimila and mega,
#MODEL ?= uno
# Or you can set it to a conditional like this one: this will use an Uno
# if /dev/ttyACM0 is present, otherwise revert to atmega328.
MODEL ?= $(shell if test -e /dev/ttyACM0; then echo uno; else echo atmega328; fi)

############################################################################
# Platform's settings
############################################################################

# Determine operating system environment
ifneq "$(wildcard C:/Windows/)" ""
 UNAME=Windows
else
 UNAME=$(shell uname)
endif

# Name of the program and source .ino file:
ifeq "$(UNAME)" "Windows"
 TARGET = $(shell for %i in $(PWD) do @echo %~nxi) # XXX needs to be tested
else
 TARGET = $(lastword $(shell basename $(CURDIR)))
endif

# Where do you keep the official Arduino software package?
# /usr/local/share/arduino
ARDUINO_DIR = /Applications/Arduino.app/Contents/Resources/Java
HOME_LIB = $(HOME)/sketchbook/libraries

# path to ATTiny files look at http://hlt.media.mit.edu/?p=1695
#ATTINY_DIR=$(ARDUINO_DIR)/hardware/attiny45_85

############################################################################
# Below here nothing should need to be changed. Cross your fingers!
############################################################################

# Where are tools like avr-gcc located on your system?
ifeq "$(UNAME)" "Windows"
  AVR_TOOLS_PATH = $(ARDUINO_DIR)/hardware/tools/avr/bin #XXX needs to be checked !
else
 ifeq "$(UNAME)" "Darwin"
  AVR_TOOLS_PATH = $(ARDUINO_DIR)/hardware/tools/avr/bin
 else
  AVR_TOOLS_PATH = /usr/bin
 endif
endif

ifeq "$(UNAME)" "Windows"
 PORT ?= COM1 #XXX needs to be checked !
else
 ifeq "$(UNAME)" "Darwin"
  ifeq "$(MODEL)" "uno"
   PORT ?= /dev/tty.usbmodem*
  else
   PORT ?= /dev/tty.usbserial*
  endif
 else
  ifeq "$(UNAME)" "Linux"
   ifeq "$(MODEL)" "uno"
    PORT ?= /dev/ttyACM*
   else
    PORT ?= /dev/ttyUSB*
   endif
  endif
 endif
endif

# How to reset the device before downloading a new program.
# These don't always work; if the default one doesn't work,
# try uncommenting one of the others instead.
ifeq "$(RESET_MODE)" "python"
 RESET_DEVICE = python -c "import serial; s = serial.SERIAL('/dev/ttyUSB0', 57600); s.setDTR(True); sleep(1); s.setDTR(False)"
else
 ifeq "$(RESET_MODE)" "perl"
  RESET_DEVICE = perl -MDevice::SerialPort -e 'Device::SerialPort->new("/dev/ttyUSB0")->pulse_dtr_on(1000)'
 else
  ifeq "$(UNAME)" "Windows"
   RESET_DEVICE = echo "CAN'T RESET DEVICE ON WINDOWS !"
  else
   ifeq "$(UNAME)" "Linux"
    RESET_DEVICE = stty -F $(PORT) hupcl
   else
    # BSD uses small f
    RESET_DEVICE = stty -f $(PORT) hupcl
   endif
  endif
 endif
endif

#
# set up attiny boards.txt path
#
ifeq "$(wildcard $(ATTINY_DIR))" ""
 ATTINY_BOARDS=
else
 ATTINY_BOARDS=$(ATTINY_DIR)/boards.txt
endif

#
# Set up values according to what the IDE uses:
#
DOWNLOAD_RATE = $(shell grep "^$(MODEL)\." $(ARDUINO_DIR)/hardware/arduino/boards.txt $(ATTINY_BOARDS) | grep upload.speed | sed 's/.*=//')
MCU = $(shell grep "^$(MODEL)\." $(ARDUINO_DIR)/hardware/arduino/boards.txt $(ATTINY_BOARDS) | grep build.mcu | sed 's/.*=//')
F_CPU = $(shell grep "^$(MODEL)\." $(ARDUINO_DIR)/hardware/arduino/boards.txt $(ATTINY_BOARDS) | grep build.f_cpu | sed 's/.*=//')

# man avrdude says to use arduino, but the IDE mostly uses stk500.
# One rumor says that the difference is that arduino does an auto-reset,
# stk500 doesn't.
# Might want to grep for upload.protocol as with previous 3 values.
AVRDUDE_PROGRAMMER = arduino

# This has only been tested on standard variants. I'm guessing
# at what mega and micro might need; other possibilities are
# leonardo and "eightanaloginputs".
ifeq "$(MODEL)" "mega"
 ARDUINO_VARIANT=$(ARDUINO_DIR)/hardware/arduino/variants/mega
else
 ifeq "$(MODEL)" "micro"
  ARDUINO_VARIANT=$(ARDUINO_DIR)/hardware/arduino/variants/micro
 else
   ifneq (,$(findstring "tiny",$(MODEL)))
    ARDUINO_VARIANT=$(ATTINY_DIR)/cores/attiny45_85
   else
    ARDUINO_VARIANT=$(ARDUINO_DIR)/hardware/arduino/variants/standard
   endif
 endif
endif

ifeq "$(UNAME)" "Windows"
 CWDBASE = $(shell for %i in $(PWD) do @echo %~nxi) # XXX needs to be tested
else
 CWDBASE = $(shell basename $(PWD))
endif
TARFILE = $(TARGET)-$(VERSION).tar.gz

ARDUINO_CORE = $(ARDUINO_DIR)/hardware/arduino/cores/arduino
# $(ARDUINO_DIR)/hardware/arduino/variants/standard/pins_arduino.c
SRC = \
    $(ARDUINO_CORE)/wiring.c \
    $(ARDUINO_CORE)/wiring_analog.c $(ARDUINO_CORE)/wiring_digital.c \
    $(ARDUINO_CORE)/wiring_pulse.c \
    $(ARDUINO_CORE)/wiring_shift.c $(ARDUINO_CORE)/WInterrupts.c \
    $(foreach l,$(USERLIBS),$(wildcard $(HOME)/sketchbook/libraries/$l/*.c)) \
    $(foreach l,$(ARDLIBS),$(wildcard $(ARDUINO_DIR)/libraries/$l/*.c))

# From ARDUINO_CORE we may only need HardwareSerial, WMath, WString, Print
# and occasionally Tone, but grab everything just in case.
CXXSRC = \
    $(wildcard $(ARDUINO_CORE)/*.cpp) \
    $(foreach l,$(USERLIBS),$(wildcard $(HOME)/sketchbook/libraries/$l/*.cpp)) \
    $(foreach l,$(ARDLIBS),$(wildcard $(ARDUINO_DIR)/libraries/$l/*.cpp))

FORMAT = ihex

# Name of this Makefile (used for "make depend").
MAKEFILE = Makefile

# Debugging format.
# Native formats for AVR-GCC's -g are stabs [default], or dwarf-2.
# AVR (extended) COFF requires stabs, plus an avr-objcopy run.
DEBUG = stabs

OPT = s

# Place -D or -U options here
CDEFS = -DF_CPU=$(F_CPU)

# Include directories
CINCS = -I$(ARDUINO_CORE) -I$(ARDUINO_VARIANT) $(patsubst %,-I$(ARDUINO_DIR)/libraries/%,$(ARDLIBS)) $(patsubst %,-I$(HOME)/sketchbook/libraries/%,$(USERLIBS)) $(patsubst %,-I$(HOME_LIB)/%/,$(USERLIBS))

# Compiler flag to set the C Standard level.
# c89   - "ANSI" C
# gnu89 - c89 plus GCC extensions
# c99   - ISO C99 standard (not yet fully implemented)
# gnu99 - c99 plus GCC extensions
#CSTANDARD = -std=gnu99
CDEBUG = -g$(DEBUG)
#CWARN = -Wall -Wstrict-prototypes
CTUNING = -funsigned-char -funsigned-bitfields -fpack-struct -fshort-enums
#CEXTRA = -Wa,-adhlns=$(<:.c=.lst)

# Extra flags to match what the Arduino 1.0 IDE is doing:
# Something about the -ffunction-sections -fdata-sections reduces
# final text size by roughly half!
CEXTRA= -g -Os -Wall -fno-exceptions -ffunction-sections -fdata-sections -DARDUINO=100

CFLAGS = $(CDEBUG) $(CDEFS) $(CINCS) -O$(OPT) $(CWARN) $(CSTANDARD) $(CEXTRA)
CXXFLAGS = $(CDEFS) $(CINCS) -O$(OPT) $(CEXTRA)
#ASFLAGS = -Wa,-adhlns=$(<:.S=.lst),-gstabs
LDFLAGS = -Os -Wl,--gc-sections -mmcu=$(MCU) -lm

# Programming support using avrdude. Settings and variables.
AVRDUDE_WRITE_FLASH = -U flash:w:applet/$(TARGET).hex
ifeq "$(UNAME)" "Darwin"
AVRDUDE_CONF = -V -F -C $(ARDUINO_DIR)/hardware/tools/avr/etc/avrdude.conf
else
AVRDUDE_CONF = -V -F -C /etc/avrdude.conf
endif
AVRDUDE_FLAGS = $(AVRDUDE_CONF) \
    -p $(MCU) -P $(PORT) -c $(AVRDUDE_PROGRAMMER) \
    -b $(DOWNLOAD_RATE)

# Program settings
CC = $(AVR_TOOLS_PATH)/avr-gcc
CXX = $(AVR_TOOLS_PATH)/avr-g++
OBJCOPY = $(AVR_TOOLS_PATH)/avr-objcopy
OBJDUMP = $(AVR_TOOLS_PATH)/avr-objdump
AR  = $(AVR_TOOLS_PATH)/avr-ar
SIZE = $(AVR_TOOLS_PATH)/avr-size
NM = $(AVR_TOOLS_PATH)/avr-nm
AVRDUDE = $(AVR_TOOLS_PATH)/avrdude
REMOVE = rm -f
MV = mv -f

# Define all object files.
OBJ = $(SRC:.c=.o) $(CXXSRC:.cpp=.o) $(ASRC:.S=.o)

# Define all listing files.
LST = $(ASRC:.S=.lst) $(CXXSRC:.cpp=.lst) $(SRC:.c=.lst)

# Combine all necessary flags and optional flags.
# Add target processor to flags.
ALL_CFLAGS = -mmcu=$(MCU) -I. $(CFLAGS)
ALL_CXXFLAGS = -mmcu=$(MCU) -I. $(CXXFLAGS)
ALL_ASFLAGS = -mmcu=$(MCU) -I. -x assembler-with-cpp $(ASFLAGS)

# Default target.
all: applet_files build sizeafter

test:
	@echo CXXSRC = $(CXXSRC)

build: elf hex

#applet_files: $(TARGET).ino

applet/$(TARGET).cpp: $(TARGET).ino
	# Here is the "preprocessing".
	# It creates a .cpp file based with the same name as the .ino file.
	# On top of the new .cpp file comes the WProgram.h header.
	# At the end there is a generic main() function attached,
	# plus special magic to get around the pure virtual error
	# undefined reference to `__cxa_pure_virtual' from Print.o.
	# Then the .cpp file will be compiled. Errors during compile will
	# refer to this new, automatically generated, file.
	# Not the original .ino file you actually edit...
	test -d applet || mkdir applet
	echo '#include "Arduino.h"' > applet/$(TARGET).cpp
	cat $(TARGET).ino >> applet/$(TARGET).cpp
	echo 'extern "C" void __cxa_pure_virtual() { while (1) ; }' >> applet/$(TARGET).cpp
	cat $(ARDUINO_CORE)/main.cpp >> applet/$(TARGET).cpp

elf: applet/$(TARGET).elf
hex: applet/$(TARGET).hex
eep: applet/$(TARGET).eep
lss: applet/$(TARGET).lss
sym: applet/$(TARGET).sym

# Program the device.
download: applet/$(TARGET).hex
	$(RESET_DEVICE)
	$(AVRDUDE) $(AVRDUDE_FLAGS) $(AVRDUDE_WRITE_FLASH)

upload: download

	# Display size of file.
HEXSIZE = $(SIZE) --target=$(FORMAT) applet/$(TARGET).hex
ELFSIZE = $(SIZE)  applet/$(TARGET).elf
sizebefore:
	@if [ -f applet/$(TARGET).elf ]; then echo; echo $(MSG_SIZE_BEFORE); $(HEXSIZE); echo; fi

sizeafter:
	@if [ -f applet/$(TARGET).elf ]; then echo; echo $(MSG_SIZE_AFTER); $(HEXSIZE); echo; fi

# Convert ELF to COFF for use in debugging / simulating in AVR Studio or VMLAB.
COFFCONVERT=$(OBJCOPY) --debugging \
    --change-section-address .data-0x800000 \
    --change-section-address .bss-0x800000 \
    --change-section-address .noinit-0x800000 \
    --change-section-address .eeprom-0x810000

coff: applet/$(TARGET).elf
	$(COFFCONVERT) -O coff-avr applet/$(TARGET).elf $(TARGET).cof


extcoff: $(TARGET).elf
	$(COFFCONVERT) -O coff-ext-avr applet/$(TARGET).elf $(TARGET).cof

.SUFFIXES: .elf .hex .eep .lss .sym

.elf.hex:
	$(OBJCOPY) -O $(FORMAT) -R .eeprom $< $@

.elf.eep:
	-$(OBJCOPY) -j .eeprom --set-section-flags=.eeprom="alloc,load" \
	--change-section-lma .eeprom=0 -O $(FORMAT) $< $@

# Create extended listing file from ELF output file.
.elf.lss:
	$(OBJDUMP) -h -S $< > $@

# Create a symbol table from ELF output file.
.elf.sym:
	$(NM) -n $< > $@

	# Link: create ELF output file from library.
applet/$(TARGET).elf: applet/$(TARGET).o applet/core.a
	$(CC) -o $@ applet/$(TARGET).o -L. applet/core.a $(LDFLAGS)

#applet/$(TARGET).elf: applet/$(TARGET).o applet/core.a
#	$(CC) $(ALL_CFLAGS) -o $@ applet/$(TARGET).cpp -L. applet/core.a $(LDFLAGS)

applet/core.a: $(OBJ)
	@for i in $(OBJ); do echo $(AR) rcs applet/core.a $$i; $(AR) rcs applet/core.a $$i; done

# Compile: create object files from C++ source files.
.cpp.o:
	$(CXX) -c $(ALL_CXXFLAGS) $< -o $@

# Compile: create object files from C source files.
.c.o:
	$(CC) -c $(ALL_CFLAGS) $< -o $@


# Compile: create assembler files from C source files.
.c.s:
	$(CC) -S $(ALL_CFLAGS) $< -o $@


# Assemble: create object files from assembler source files.
.S.o:
	$(CC) -c $(ALL_ASFLAGS) $< -o $@

# Target: clean project.
clean:
	$(REMOVE) -rf applet/ \
	$(REMOVE) $(OBJ) $(LST) $(SRC:.c=.s) $(SRC:.c=.d) $(CXXSRC:.cpp=.s) $(CXXSRC:.cpp=.d)

list:
	# LIST OF ALL THE BOARDS AVAILABLE AS TARGETS FOR $$MODEL ENV VARIABLE
	@cat $(ARDUINO_DIR)/hardware/arduino/boards.txt $(ATTINY_BOARDS) | grep '.name' | sed 's/\(.*\)\.name=\(.*\)/MODEL=\1			-> \2/'

tar: $(TARFILE)

$(TARFILE):
	( cd .. && \
	  tar czvf $(TARFILE) --exclude=applet --owner=root $(CWDBASE) && \
	  mv $(TARFILE) $(CWD) && \
	  echo Created $(TARFILE) \
	)

depend:
	if grep '^# DO NOT DELETE' $(MAKEFILE) >/dev/null; \
	then \
		sed -e '/^# DO NOT DELETE/,$$d' $(MAKEFILE) > \
			$(MAKEFILE).$$$$ && \
		$(MV) $(MAKEFILE).$$$$ $(MAKEFILE); \
	fi
	echo '# DO NOT DELETE THIS LINE -- make depend depends on it.' \
		>> $(MAKEFILE); \
	$(CC) -M -mmcu=$(MCU) $(CDEFS) $(CINCS) $(SRC) $(ASRC) >> $(MAKEFILE)

.PHONY:	all build elf hex eep lss sym program coff extcoff clean depend applet_files sizebefore sizeafter
