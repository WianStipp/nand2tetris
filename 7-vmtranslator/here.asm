
//D=index
@10
D=A
//Push D to SP
@SP
A=M
M=D
//SP++
@SP
M=M+1
// pop LCL 0
// SP--
@SP
M = M-1
A = M
D = M // D=RAM[SP]
// RAM[LCL+i] = D
@LCL
A = M
A = A+0
M = D


//D=index
@21
D=A
//Push D to SP
@SP
A=M
M=D
//SP++
@SP
M=M+1

//D=index
@22
D=A
//Push D to SP
@SP
A=M
M=D
//SP++
@SP
M=M+1
// pop ARG 2
// SP--
@SP
M = M-1
A = M
D = M // D=RAM[SP]
// RAM[ARG+i] = D
@ARG
A = M
A = A+2
M = D

// pop ARG 1
// SP--
@SP
M = M-1
A = M
D = M // D=RAM[SP]
// RAM[ARG+i] = D
@ARG
A = M
A = A+1
M = D


//D=index
@36
D=A
//Push D to SP
@SP
A=M
M=D
//SP++
@SP
M=M+1
// pop THIS 6
// SP--
@SP
M = M-1
A = M
D = M // D=RAM[SP]
// RAM[THIS+i] = D
@THIS
A = M
A = A+6
M = D


//D=index
@42
D=A
//Push D to SP
@SP
A=M
M=D
//SP++
@SP
M=M+1

//D=index
@45
D=A
//Push D to SP
@SP
A=M
M=D
//SP++
@SP
M=M+1
// pop THAT 5
// SP--
@SP
M = M-1
A = M
D = M // D=RAM[SP]
// RAM[THAT+i] = D
@THAT
A = M
A = A+5
M = D

// pop THAT 2
// SP--
@SP
M = M-1
A = M
D = M // D=RAM[SP]
// RAM[THAT+i] = D
@THAT
A = M
A = A+2
M = D


//D=index
@510
D=A
//Push D to SP
@SP
A=M
M=D
//SP++
@SP
M=M+1
//pop temp i
// SP--
@SP
M = M-1
// D=RAM[SP]
A = M
D = M
// TEMP[i] = D
@5
A = A+6
M = D

//push LCL 0
// LCL i -> D
@LCL
A = M
A = A + 0
D = M
// Put D onto stack
@SP
A = M
M = D
// SP++
@SP
M = M + 1

//push THAT 5
// THAT i -> D
@THAT
A = M
A = A + 5
D = M
// Put D onto stack
@SP
A = M
M = D
// SP++
@SP
M = M + 1

//add
// SP--
@SP
M = M-1
// D = RAM[SP]
A = M
D = M
// M = D + RAM[SP-1]
A = A - 1
M = D + M

//push ARG 1
// ARG i -> D
@ARG
A = M
A = A + 1
D = M
// Put D onto stack
@SP
A = M
M = D
// SP++
@SP
M = M + 1

//sub
// SP--
@SP
M = M-1
// D = RAM[SP]
A = M
D = M
// M = RAM[SP-1] - D
A = A - 1
M = M - D

//push THIS 6
// THIS i -> D
@THIS
A = M
A = A + 6
D = M
// Put D onto stack
@SP
A = M
M = D
// SP++
@SP
M = M + 1

//push THIS 6
// THIS i -> D
@THIS
A = M
A = A + 6
D = M
// Put D onto stack
@SP
A = M
M = D
// SP++
@SP
M = M + 1

//add
// SP--
@SP
M = M-1
// D = RAM[SP]
A = M
D = M
// M = D + RAM[SP-1]
A = A - 1
M = D + M

//sub
// SP--
@SP
M = M-1
// D = RAM[SP]
A = M
D = M
// M = RAM[SP-1] - D
A = A - 1
M = M - D

//push temp i
@5
A = A+6
D = M
// RAM[SP] = D
@SP
A = M
M = D
// SP++
@SP
M = M+1

//add
// SP--
@SP
M = M-1
// D = RAM[SP]
A = M
D = M
// M = D + RAM[SP-1]
A = A - 1
M = D + M

