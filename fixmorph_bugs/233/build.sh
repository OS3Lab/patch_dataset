make allyesconfig
make HOSTCC=gcc-4.7 CC=gcc-4.7 -j `nproc` drivers/gpu/drm/amd/amdgpu/gmc_v8_0.o