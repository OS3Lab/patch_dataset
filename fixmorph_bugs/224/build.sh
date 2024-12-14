make allyesconfig
make HOSTCC=gcc-4.7 CC=gcc-4.7 -j `nproc` drivers/i2c/busses/i2c-designware-core.o