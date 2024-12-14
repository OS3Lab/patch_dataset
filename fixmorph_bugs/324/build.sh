make allyesconfig
make HOSTCC=gcc-4.7 CC=gcc-4.7 -j `nproc` drivers/net/ethernet/mellanox/mlx5/core/lib/mpfs.o