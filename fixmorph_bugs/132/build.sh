make allyesconfig
make HOSTCC=gcc-4.7 CC=gcc-4.7 -j `nproc` drivers/ntb/hw/intel/ntb_hw_intel.o