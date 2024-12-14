make allyesconfig
make HOSTCC=gcc-4.7 CC=gcc-4.7 -j `nproc` arch/x86/vdso/vdso32-setup.o