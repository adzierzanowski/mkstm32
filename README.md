This script simply calls the neccesary programs
regarding specific task during the development
of STM32 projects that make use of Makefiles
generated with STM32CubeMX.

It (hopefully) saves some keystrokes and mental pain.

Following programs are required to be included in `$PATH`:

* make
* [arm-none-eabi-\*](https://developer.arm.com/open-source/gnu-toolchain/gnu-rm/downloads) binaries
* [texane/stlink](https://github.com/texane/stlink) binaries (`st-flash`,
`st-util`, `st-info`)

Should work on macOS and linux.

You should be able to run this script under Windows after:

* adding the extension to the script file: `mkstm32.py`
* making sure you have added all the neccessary programs to `PATH`
enviroment variable (inlcuding this script)
* making sure all of those programs are named properly (e.g. if you're
using mingw32, you should use `make.exe` from `MinGW\msys\1.0\bin` rather
than `mingw32-make.exe` from `MinGW\bin` or rename `mingw32-make.exe` to `make.exe`).

# examples

Compiling:

    $ mkstm32 -c

Cleaning build directory, generating C++ Makefile from the default one, compiling and uploading:

    $ mkstm32 -zcxu

Starting a debug session using `st-util` and GDB:

    $ mkstm32 -d

Resetting the MCU:

    $ mkstm32 -r
    
Getting information about the ST-Link connection:

    $ mkstm32 -i   
