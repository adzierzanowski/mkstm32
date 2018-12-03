This script simply calls the neccesary programs
regarding specific task during the development
of STM32 projects that make use of Makefiles
generated with STM32CubeMX.

It (hopefully) saves keystrokes and some mental pain.

Following programs are required to be included in `$PATH`:

* python3
* make
* [arm-none-eabi-\*](https://developer.arm.com/open-source/gnu-toolchain/gnu-rm/downloads) binaries
* [texane/stlink](https://github.com/texane/stlink) binaries (`st-flash`,
`st-util`, `st-info`)

Should work on macOS and linux. Windows requires certain
modifications but all the necessary software is available
for that OS.

# examples

Compiling:

    $ mkstm32 -c

Generating C++ Makefile from default one, compiling and uploading:

    $ mkstm32 -cux

Starting a debug session using `st-util` and GDB:

    $ mkstm32 -d

Resetting the MCU:

    $ mkstm32 -r
    
Getting information about the ST-Link connection:

    $ mkstm32 -i   
