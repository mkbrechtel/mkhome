PATH:=/usr/sbin:/usr/bin
export PATH

default: clean image
image:
	mkdir -p mkosi.cache mkosi.builddir
	mkosi build

run:
	mkosi qemu

clean:
	mkosi clean
