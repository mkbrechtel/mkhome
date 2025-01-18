PATH:=/usr/sbin:/usr/bin
export PATH

default: clean image
image:
	mkosi build

run:
	mkosi qemu

clean:
	mkosi clean
