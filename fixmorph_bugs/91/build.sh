make allyesconfig
make HOSTCC=gcc-4.7 CC=gcc-4.7 -j `nproc` fs/ncpfs/ncplib_kernel.o