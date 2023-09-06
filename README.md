# cpuB

This repository contains the design of a CPU created using Logisim and Verilog. Here are a few key points regarding this design:

- This CPU employs a unique one-cycle instruction approach, limiting the instruction set to a mere 16 instructions. While this is influenced by the one-cycle design, it promotes a form of restricted programming, which can be seen as an interesting challenge for programmers.
- Instead of using traditional bussing or dedicated memory locations, the architecture is designed to utilize two specialized registers, specifically for each I/O device. This is complemented by distinct ROM, RAM, and VRAM hardware modules.
- While the design has its quirks, it has been iteratively improved upon, especially as programming challenges for the computer were addressed. Notably, the absence of a MUL operation in the ALU means multiplication tasks take longer. Furthermore, due to the constraints of one-cycle instructions, the MOV reg, val instruction is confined to 9 bits.
- To keep the design streamlined, immediate values were intentionally excluded from the assembler. However, it's worth noting that this does introduce a layer of complexity when drafting programs.
- The instruction set utilizes 0000 as a particular instruction, with bits in the instruction acting as register selectors. As a result, it's essential to reset the A register whenever it's not in use, preventing any residual data from causing execution errors.
- While the initial intention behind this project was a light-hearted exploration into CPU design, and certain features may seem rudimentary, the process has been an invaluable learning experience. The challenges faced in both the CPU design and accompanying software (including the assembler) offer numerous insights into the complexities of hardware design.

Note: Comments in the programs are primarily for internal clarification and may contain personal anecdotes or reminders.


| Instruction | Opcode | Description |
| :---: | :---: | :--- |
| MOV reg, val | 0000 | Move the value val into the register reg |
| MOV2 reg1, reg2 | 0001 | Move the value from the register reg2 into reg1 |
| ADD reg1, reg2 | 0010 | Add the value from the register reg2 to reg1 and store result in reg1 |
| SUB reg1, reg2 | 0011 | Subtract the value in the register reg2 from reg1 and store result in reg1 |
| AND reg1, reg2 | 0100 | Perform a bitwise AND of reg1 and reg2 and store result in reg1 |
| OR reg1, reg2 | 0101 | Perform a bitwise OR of reg1 and reg2 and store result in reg1 |
| JMP | 0110 | Jump to the address stored in the jump register (rg) |
| JNEG reg1, reg2 | 0111 | Jump to the address stored in the jump register (rg) if reg1 is negative |
| JGT reg1, reg2 | 1000 | Jump to the address stored in the jump register (rg) if reg1 > reg2 |
| JGE reg1, reg2 | 1001 | Jump to the address stored in the jump register (rg) if reg1 >= reg2 |
| JLT reg1, reg2 | 1010 | Jump to the address stored in the jump register (rg) if reg1 < reg2 |
| JLE reg1, reg2 | 1011 | Jump to the address stored in the jump register (rg) if reg1 <= reg2 |
| JE reg1, reg2 | 1100 | Jump to the address stored in the jump register (rg) if reg1 = reg2 |
| JNE reg1, reg2 | 1101 | Jump to the address stored in the jump register (rg) if reg1 != reg2 |
| STORE reg | 1110 | Store the value in the register reg at the memory address in register H |
| LOAD reg | 1111 | Load the value at memory address in register H into reg |

## Register Index
| Register | Index | Description                       |
| :------: | :---: | --------------------------------- |
| A        |   0   | General Purpose Register          |
| B        |   1   | General Purpose Register          |
| C        |   2   | General Purpose Register          |
| D        |   3   | General Purpose Register          |
| E        |   4   | Special I/O Register              |
| F        |   5   | Special I/O Register              |
| G        |   6   | Jump Register                     |
| H        |   7   | Memory Access Register            |

## Included programs
- tty - write to tty and accept user input, ideally will eventually turn into a copy of wozmon that might reside in ROM permanently
- 2draw_image - display an image on an RGB screen from VRAM
- multiply - MUL alternative
