make allyesconfig
make HOSTCC=gcc-4.7 CC=gcc-4.7 -j `nproc` sound/pci/hda/hda_intel.o