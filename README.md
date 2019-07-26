# mkstm32

This script simply calls neccesary programs in order to compile, upload
and debug STM32 projects. The thing depends on a specific toolchain:

    STM32CubeMX -> Makefile -> ARM GCC -> st-link -> ARM GDB

If that suits your needs, that's cool. It hopefully may save you some
keystrokes and mental pain.

The following programs are required to be included in `$PATH`:

* make
* [arm-none-eabi-\*](https://developer.arm.com/open-source/gnu-toolchain/gnu-rm/downloads) binaries
* [texane/stlink](https://github.com/texane/stlink) binaries (`st-flash`,
`st-util`, `st-info`)
* [dfu-util](http://dfu-util.sourceforge.net/)

# features

* calling make
* uploading via ST-Link or USB bootloader
* setting up a GDB server and running the debugger
* running a serial port monitor 

# setup 

    git clone https://github.com/adzierzanowski/mkstm32.git
    pip3 install ./mkstm32

# examples

Say we want to compile, upload and debug a project in a directory called `F042_test`.

    mkstm32 -zxcudp F042_Test

* `-z` switch removes build directory.
* `-x` is a flag that tells the script to convert Cube Makefile to C++ Makefile.
* `-c` stands for compile.
* `-u` uploads compiled project to the microcontroller.
* `-d` starts a GDB debugging session after compilation and upload.
* `-p` specifies the project directory.

Et voilà.

# usage

    usage: mkstm32 [-h] [-u] [-d] [-M UPLOAD_METHOD] [-v V] [-V] [-c] [-p DIR]
               [-s] [-x] [-z] [-b BAUD_RATE] [-i] [-l] [-m] [-P PORT] [-r]
               [--uart-reset-time UART_RESET_TIME]

    Upload, debug and compile STM32CubeMX Makefile projects

    optional arguments:
    -h, --help            show this help message and exit

    Common operations:
    -u, --upload
    -d, --debug           Start GDB session
    -M UPLOAD_METHOD, --upload-method UPLOAD_METHOD
    -v V, --verbosity V   Verbosity level from -1 (completely silent) to 2
                            (fully verbose, default)
    -V, --version         Print version

    Project operations:
    -c, --compile         Call make with appropriate Makefile
    -p DIR, --project-dir DIR
                            Defaults to current dir
    -s, --size            Print size of built binaries
    -x, --cpp             Use C++ rather than C
    -z, --clean           Clean (remove) build directory

    ST-Link operations:
    -b BAUD_RATE, --baud-rate BAUD_RATE
                            Baud rate for serial monitor
    -i, --probe           Print ST-Link connection information
    -l, --list-ports      List serial ports
    -m, --monitor         Serial monitor
    -P PORT, --port PORT
    -r, --reset           Reset the microcontroller
    --uart-reset-time UART_RESET_TIME
                            Sleep time before resetting the connection on error


# zsh completions

    compdef _gnu_generic mkstm32

should work just fine.

# todo

* .gdbinit creation from config

# Windows things

I tried to make this script as platform independent as I could.
All of the required software is available for Windows.
You should be able to run this script after:

* installing python3
* making sure you have added all the neccessary programs to `PATH`
* making sure all of those programs are named properly (e.g. if you're
using mingw32, you should use `make.exe` from `MinGW\msys\1.0\bin` rather
than `mingw32-make.exe` from `MinGW\bin` or rename `mingw32-make.exe` to `make.exe`).

For some strange reason, this works when you type something along those lines:

    >python3 mkstm32

But the script installed with pip fails throwing `ModuleNotFoundError`.
What makes it even stranger, when you open the Python interpreter
and type in the import that failed, it magically works.

Well, anyway, it does eventually work on Windows after some hassle.

If you are using `cmd.exe`, I recommend using [ansicon](https://github.com/adoxa/ansicon)
for colorful messages. It's way easier to skim through the output.
