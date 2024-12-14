make allyesconfig
make HOSTCC=gcc-4.7 CC=gcc-4.7 -j `nproc` drivers/net/ethernet/hisilicon/hns3/hns3pf/hns3_enet.o