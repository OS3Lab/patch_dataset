make allyesconfig
make HOSTCC=gcc-4.7 CC=gcc-4.7 -j `nproc` sound/core/seq/oss/seq_oss_init.o