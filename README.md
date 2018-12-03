This script simply calls the neccesary programs
regarding specific task during the development
of STM32 projects that make use of Makefiles
generated with STM32CubeMX.

It (hopefully) saves keystrokes and some mental pain.

Following programs are required to be included in `$PATH`:

* make
* [arm-none-eabi-\*](https://developer.arm.com/open-source/gnu-toolchain/gnu-rm/downloads)

* [texane/stlink](https://github.com/texane/stlink)
* * st-util
* * st-flash
* * st-info

Should work on macOS or linux. Windows requires certain
modifications but all the necessary software is available.
