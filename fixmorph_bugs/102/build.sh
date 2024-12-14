make allyesconfig
make HOSTCC=gcc-4.7 CC=gcc-4.7 -j `nproc` arch/arm/mach-imx/clk-vf610.o