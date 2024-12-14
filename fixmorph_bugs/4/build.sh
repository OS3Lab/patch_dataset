make allyesconfig
make HOSTCC=gcc-4.7 CC=gcc-4.7 -j `nproc` drivers/mmc/host/sdhci-of-arasan.o