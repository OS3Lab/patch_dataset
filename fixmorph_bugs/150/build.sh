make allyesconfig
make HOSTCC=gcc-4.7 CC=gcc-4.7 -j `nproc` drivers/net/wireless/brcm80211/brcmsmac/mac80211_if.o