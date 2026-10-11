CC ?= gcc
CFLAGS ?= -O1 -fno-stack-protector -Wall -Wextra

all: shalya_whisper

shalya_whisper: shalya_whisper.c
	$(CC) $(CFLAGS) -static shalya_whisper.c -o shalya_whisper

clean:
	rm -f shalya_whisper
