make allyesconfig
make HOSTCC=gcc-4.7 CC=gcc-4.7 -j `nproc` drivers/net/wireless/rtlwifi/rtl8192se/sw.o