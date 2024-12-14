make allyesconfig
make HOSTCC=gcc-4.7 CC=gcc-4.7 -j `nproc` drivers/net/wireless/brcm80211/brcmfmac/cfg80211.o