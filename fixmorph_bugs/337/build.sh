make allyesconfig
make HOSTCC=gcc-4.7 CC=gcc-4.7 -j `nproc` net/openvswitch/flow_netlink.o