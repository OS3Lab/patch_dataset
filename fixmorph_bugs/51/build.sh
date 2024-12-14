make allyesconfig
make HOSTCC=gcc-4.7 CC=gcc-4.7 -j `nproc` kernel/cgroup_pids.o