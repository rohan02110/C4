CC ?= gcc
CFLAGS ?= -O0 -fstack-protector-all -pie -fPIE -Wl,-z,now -Wl,-z,relro -Wall -Wextra

all: antahkaranam

antahkaranam: antahkaranam.c
	$(CC) $(CFLAGS) antahkaranam.c -o antahkaranam

clean:
	rm -f antahkaranam
