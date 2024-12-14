make allyesconfig
make HOSTCC=gcc-4.7 CC=gcc-4.7 -j `nproc` drivers/gpu/drm/amd/amdkfd/kfd_topology.o