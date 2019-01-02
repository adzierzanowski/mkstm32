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

# usage

    usage: mkstm32 [-h] [-u] [-d] [-v VERBOSITY] [-c] [-p DIR] [-s] [-x] [-z] [-i]
               [-r]

    Upload, debug and compile STM32CubeMX Makefile projects

    optional arguments:
    -h, --help            show this help message and exit

    Common operations:
    -u, --upload
    -d, --debug           Start GDB session
    -v VERBOSITY, --verbosity VERBOSITY
                            Verbosity level (0-3)

    Project operations:
    -c, --compile         Call make with appropriate Makefile
    -p DIR, --project-dir DIR
                            Defaults to current dir
    -s, --size            Print size of built binaries
    -x, --cpp             Use C++ rather than C
    -z, --clean           Clean (remove) build directory

    ST-Link operations:
    -i, --probe           Print ST-Link connection information
    -r, --reset           Reset the microcontroller

# examples

Say we want to compile, upload and debug a project in directory `F042_test`.

    mkstm32 -zxcudp F042_Test

* `-z` switch removes build directory.
* `-x` is a flag that tells the script to convert Cube Makefile to C++ Makefile.
* `-c` stands for compile.
* `-u` uploads compiled project to the microcontroller.
* `-d` starts a GDB debugging session after compilation and upload.
* `-p` specifies the project directory.

Et voilà.
