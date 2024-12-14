make allyesconfig
make HOSTCC=gcc-4.7 CC=gcc-4.7 -j `nproc` drivers/gpu/drm/i915/intel_dp.o