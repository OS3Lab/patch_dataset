make allyesconfig
make HOSTCC=gcc-4.7 CC=gcc-4.7 -j `nproc` crypto/crypto_user.o