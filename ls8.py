from cpu import *
import sys

cpu = CPU()

try:
    cpu.load(sys.argv[1])
    cpu.run()
except IndexError:
    print("filename needed")