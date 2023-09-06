#!/usr/bin/env python3

import sys
import re

REGISTERS = {
    "ra": "000",
    "rb": "001",
    "rc": "010",
    "rd": "011",
    "re": "100",
    "rf": "101",
    "rg": "110",
    "rh": "111",
}

INSTRUCTIONS = {
    "MOV": ["reg", "int"],
    "MOV2": ["reg", "reg"],
    "JMP": [],
    "ADD": ["reg", "reg"],
    "SUB": ["reg", "reg"],
    "AND": ["reg", "reg"],
    "OR": ["reg", "reg"],
    "JNEG": ["reg", "reg"],
    "JGT": ["reg", "reg"],
    "JGE": ["reg", "reg"],
    "JLT": ["reg", "reg"],
    "JLE": ["reg", "reg"],
    "JEQ": ["reg", "reg"],
    "JNE": ["reg", "reg"],
    "STORE": ["reg"],
    "LOAD": ["reg"],
}

INSTRUCTIONS_OPCODES = {
    "MOV": "0000",
    "MOV2": "0001",
    "ADD": "0010",
    "SUB": "0011",
    "AND": "0100",
    "OR": "0101",
    "JMP": "0110",
    "JNEG": "0111",
    "JGT": "1000",
    "JGE": "1001",
    "JLT": "1010",
    "JLE": "1011",
    "JEQ": "1100",
    "JNE": "1101",
    "STORE": "1110",
    "LOAD": "1111",
}

DIRECTIVES = {"const": "int", "asciz": "str"}

file_instructions = []
labels = {}
consts = {}


class Instruction:
    def __init__(self, opcode, loper, roper=None):
        self.opcode = opcode
        self.loper = loper
        self.roper = roper

    def to_binary(self):
        ins = ""
        ins += INSTRUCTIONS_OPCODES[self.opcode]

        if self.loper != None and self.loper.isdigit():
            ins += bin(self.loper)[2:]
        elif self.loper == None:
            ins += "0" * 3
        else:
            ins += REGISTERS[self.loper]

        if self.roper is None:
            ins += "0" * 9
        else:
            if self.roper in labels.keys():
                ins_len = 9 - len(bin(int(labels[self.roper]))[2:])
                ins += "0" * ins_len
                ins += bin(int(labels[self.roper]))[2:]
            elif self.roper in consts.keys():
                self.roper = consts[self.roper]
                ins_len = 9 - len(bin(int(self.roper))[2:])
                ins += "0" * ins_len
                ins += bin(int(self.roper))[2:]
            elif self.roper.isdigit():
                ins_len = 9 - len(bin(int(self.roper))[2:])
                ins += "0" * ins_len
                ins += bin(int(self.roper))[2:]
            else:
                ins += REGISTERS[self.roper]
                ins += "0" * 6

        return ins


class Parser:
    def __init__(self, input_file):
        self.input_file = input_file
        self.binary = []
        self.hex = []
        self.line_num = 1
        self.directive_line = 0
        self.parse()

    def validate_instruction_tokens(self, instruction, tokens):
        expected_types = INSTRUCTIONS[instruction]
        for token, expected in zip(tokens, expected_types):
            if expected == "reg" and token not in REGISTERS.keys():
                raise TypeError(instruction, token, "Not a register?")
            elif expected == "int":
                if token in labels.keys():
                    pass
                elif token in consts.keys():
                    pass
                elif not token.isdigit():
                    raise TypeError(instruction, token, "Not a number?")

    def validate_directive_value(self, directive, value):
        expected_type = DIRECTIVES[directive]
        value = value.replace(" ", "")
        if expected_type == "int" and not value.isdigit():
            raise TypeError(
                directive, value, f"Wrong {directive} type, expected {expected_type}"
            )
        if expected_type == "reg" and value not in REGISTERS.keys():
            raise TypeError(
                directive, value, f"Wrong {directive} type, expected {expected_type}"
            )
        if expected_type == "str" and type(value) is not str:
            raise TypeError(
                directive, value, f"Wrong {directive} type, expected {expected_type}"
            )

    def check_skipable_line(self, line):
        if self.get_is_label(line) or self.get_is_directive(line):
            return True

        return False

    def get_is_directive(self, line):
        if "%" in line:
            line = line.split()
            directive = line[0]
            if directive.strip("%") in DIRECTIVES.keys():
                return True

    def set_directive(self, line, dryRun=False):
        if "%const" in line:
            const_name, const_value = line.split()[1:]
            consts[const_name] = const_value

        if "%asciz" in line:
            if '"' in line:
                line = line.replace('"', '')
            text = line.split()

            if not dryRun:
                asciz_name = text[1]

            text = text[2:]
            text = ' '.join(text)
            
            ascii_hex = [hex(ord(char)) for char in text]

            if not dryRun:
                consts[asciz_name] = len(ascii_hex)
                file_instructions.append(Instruction('MOV', 'rc', str(1)))

            for ascii_character_code in ascii_hex:
                if not dryRun:
                    file_instructions.append(Instruction('MOV', 'rb', str(int(ascii_character_code, 16))))
                    file_instructions.append(Instruction('STORE', 'rb'))
                    file_instructions.append(Instruction('ADD', 'rh', 'rc'))
                self.directive_line += 3

    def get_is_label(self, line):
        if line:
            if line[-1] == ":":
                return True

    def set_label(self, line):
        label = line[:-1]
        labels[label] = self.line_num + self.directive_line

    def parse(self):
        ### LABELS
        self.input_file.seek(0)
        for line in self.input_file:
            self.set_directive(line, dryRun=True)
            line = line.strip()
            if ';' in line:
                continue

            if '%' in line:
                continue

            if self.get_is_label(line):
                self.set_label(line)
                continue

            if line:
                if ';' not in line or '%' not in line:
                    self.line_num += 1
        else:
            self.directive_line = 0

        ### INSTRUCTIONS
        self.line_num = 0
        self.input_file.seek(0)
        for line in self.input_file:
            line = line.strip()

            if ";" in line:
                line = line.split(";")[0].strip()

            if "%" in line:
                self.set_directive(line)

            if line and not self.check_skipable_line(line):
                if len(line.split()) >= 2:
                    instruction, operands = line.split(maxsplit=1)
                    tokens = re.split(r"[\s,]", operands)
                    tokens = [token for token in tokens if token != ""]

                    self.validate_instruction_tokens(instruction, tokens)

                    if len(tokens) == 2:
                        file_instructions.append(
                            Instruction(instruction, tokens[0], tokens[1])
                        )
                    else:
                        file_instructions.append(Instruction(instruction, tokens[0]))
                else:
                    instruction = line.split()[0]
                    file_instructions.append(Instruction(instruction, None, None))
            if line:
                self.line_num += 1

    def assemble(self):
        for instruction in file_instructions:
            self.binary.append(instruction.to_binary())
            self.hex = [hex(int(binary, 2))[2:] for binary in self.binary]



        hex_ins = ""
        line_num = 0
        for ins in self.hex:
            hex_ins += ins + ' '
        else:
            print(hex_ins)

        hex_ins = ""
        line_num = 0
        for ins in self.hex:
            instruction = file_instructions[line_num]
            instruction = instruction.opcode + ' ' + str(instruction.loper) + ' ' + str(instruction.roper)

            hex_ins += str(line_num) + ': ' + ins + ': ' + instruction + '\n'
            line_num += 1
        else:
            print(hex_ins)


        print ('---CONSTS---')
        for const, key in consts.items():
            print(key, const)
       
        print ('---LABELS---')
        for label, key in labels.items():
            print(key, label)
        # print(labels, consts)


def main():
    with open(sys.argv[1], "r") as file:
        parser = Parser(file)
        parser.assemble()


if __name__ == "__main__":
    main()
