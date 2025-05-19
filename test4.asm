.data
str_nl: .asciz "\n"
.text
L0:   b Lτεστ 
Lτεστ: 
L1: 
      addi sp,sp,24 
      mv gp,sp 
L2: 
     li a7,5
     ecall
      sw a0,-12(sp) 
L3: 
     li a7,5
     ecall
      sw a0,-16(sp) 
L4: 
     li a7,5
     ecall
      sw a0,-20(sp) 
L5: 
      lw t1,-12(sp) 
      li t2,18 
     bge t1,t2,L7 
L6: 
      b L21 
L7: 
      lw t1,-12(sp) 
      li t2,65 
     ble t1,t2,L9 
L8: 
      b L21 
L9: 
      lw t1,-20(sp) 
      li t2,2000 
     bge t1,t2,L11 
L10: 
      b L13 
L11: 
      lw t1,-16(sp) 
      li t2,650 
     bge t1,t2,L19 
L12: 
      b L13 
L13: 
      lw t1,-20(sp) 
      li t2,5000 
     bge t1,t2,L19 
L14: 
      b L15 
L15: 
      lw t1,-16(sp) 
      li t2,700 
     bge t1,t2,L17 
L16: 
      b L21 
L17: 
      lw t1,-20(sp) 
      li t2,1500 
     bge t1,t2,L19 
L18: 
      b L21 
L19: 
      li a0,1 
     li a7,1
     ecall
     la a0,str_nl
     li a7,4
     ecall
L20: 
      b L22 
L21: 
      li a0,0 
     li a7,1
     ecall
     la a0,str_nl
     li a7,4
     ecall
L22: 
     li a0,0
     li a7,93
     ecall
L23: 
