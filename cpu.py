import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001

PUSH = 0b01000101
POP = 0b01000110

MUL = 0b10100010 # Multiplication
ADD = 0b10100000
CMP = 0b10100111 # Comparable

CALL = 0b01010000
RET = 0b00010001
JEQ = 0b01010101
JMP = 0b01010100
JNE = 0b01010110



class CPU:
    def __init__(self):
        self.halted = False
        self.pc = 0
        self.ir = 0
        self.fl = 0
        self.mar = 0
        self.mdr = 0
        self.sp = 7

        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.ram = [0] * 256
        
        self.dispatchable = {
            MUL: self.mul,
            ADD: self.add,
            CMP: self.cmp,
            PRN: self.prn,
            LDI: self.ldi,
            PUSH: self.push,
            POP: self.pop,
            CALL: self.call,
            RET: self.ret,
            JMP: self.jmp,
            JEQ: self.jeq,
            JNE: self.jne
        }
    

    def load(self, file_name):
        address = 0
        with open(file_name, 'r') as file:
            for line in file:
                if line.startswith('#') or line.startswith('\n'):
                    continue
                else:
                    instruction = line.split(' ')[0]
                    self.ram[address] = int(instruction, 2)
                    address += 1
                
    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
        

    def alu(self, op, reg_a, reg_b):
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # if op == SUB:
        #     self.reg[reg_a] -= self.reg[reg_b]
        if op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        # if op == DIV:
        #     self.reg[reg_a] /= self.reg[reg_b]
        if op == "CMP":
            self.fl = 1 if self.reg[reg_a] == self.reg[reg_b] else 0
        else:
            raise Exception("Not an ALU")
    
    def mul(self, reg_a, reg_b):
        self.alu("MUL", reg_a, reg_b)
        self.pc += 3

    def add(self, reg_a, reg_b):
        self.alu("ADD", reg_a, reg_b)
        self.pc += 3

    def cmp(self, reg_a, reg_b):
        self.alu("CMP", reg_a, reg_b)
        self.pc += 3

    def prn(self, reg_a, reg_b):
        print(self.reg[reg_a])
        self.pc += 2

    def ldi(self, reg_a, reg_b):
        self.reg[reg_a] = reg_b
        self.pc += 3

    def push(self, reg_a, reg_b):
        self.sp -= 1
        self.ram_write(self.sp, self.reg[reg_a])
        self.pc += 2

    def pop(self, reg_a, reg_b):
        self.reg[reg_a] = self.ram_read(self.sp)
        self.sp += 1
        self.pc += 2

    def call(self, reg_a, reg_b):
        self.sp -= 1
        self.ram_write(self.sp, self.pc + 2)
        self.pc = self.reg[reg_a]

    def ret(self, reg_a, reg_b):
        self.pc = self.ram_read(self.sp)
        self.sp += 1

    def jmp(self, reg_a, reg_b):
        self.pc = self.reg[reg_a]

    def jeq(self, reg_a, reg_b):
        if self.fl:
            self.jmp(reg_a, reg_b)
        else:
            self.pc += 2

    def jne(self, reg_a, reg_b):
        if not self.fl:
            self.jmp(reg_a, reg_b)
        else:
            self.pc += 2
    def run(self):
        running = True

        while running:
            ir = self.ram_read(self.pc)
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)
            if ir == HLT:
                running = False
            else:
                self.dispatchable[ir](reg_a, reg_b)