make allyesconfig
make HOSTCC=gcc-4.7 CC=gcc-4.7 -j `nproc` drivers/staging/media/pulse8-cec/pulse8-cec.o