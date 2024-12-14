make allyesconfig
make HOSTCC=gcc-4.7 CC=gcc-4.7 -j `nproc` drivers/pinctrl/sh-pfc/pfc-r8a7791.o