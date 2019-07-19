#!/usr/bin/python

"""
Test /dev/cskmem
"""

from __future__ import print_function

import os, sys, mmap
import pagemap

def get_kernel_address():
    """
    Get the VA of the kernel, the first entry in kallsyms.
    """
    f = open("/proc/kallsyms")
    for ln in f:
        ln.strip()
        addr = int(ln.split()[0], 16)
        break
    f.close()
    return addr


def get_page_size():
    return os.sysconf("SC_PAGE_SIZE")


def round_down(a):
    return a & ~(get_page_size() - 1)


def adjust(a):
    # convert an absolute address into something that can convert to an off_t
    #if a >= 0x8000000000000000:
    #    a &= 0x7fffffffffffffff
    return a


def test(m, va):
    print("VA %x has PA..." % va)
    pa = m.pa(va)
    print("%x PA = 0x%x" % (va, pa))

    kmem_file = open("/dev/cskmem", "rb")
    raddr = adjust(round_down(va))
    print("  mapping at offset 0x%x" % raddr)
    kmem_mmap = mmap.mmap(kmem_file.fileno(), get_page_size(), mmap.MAP_SHARED, mmap.PROT_READ, offset=raddr)
    for i in range(0, 16):
        print("%02x" % ord(kmem_mmap[i]), sep=" ")
    print()
    kmem_mmap.close()
    kmem_file.close()


if __name__ == "__main__":
    kaddr = get_kernel_address()
    print("testing address 0x%x" % kaddr)
    m = pagemap.PAMap()
    test(m, kaddr)

