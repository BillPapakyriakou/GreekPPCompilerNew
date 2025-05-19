.data
str_nl: .asciz "\n"
.text
L0:   b Lτεστ 
Lτεστ: 
L1: 
      addi sp,sp,48 
      mv gp,sp 
L2: 
      li t1,0 
      sw t1,-12(sp) 
L3: 
      li t1,1 
      sw t1,-16(sp) 
L4: 
      li t1,0 
      sw t1,-20(sp) 
L5: 
      lw t1,-20(sp) 
      li t2,10 
     ble t1,t2,L7 
L6: 
      b L15 
L7: 
      lw a0,-12(sp) 
     li a7,1
     ecall
     la a0,str_nl
     li a7,4
     ecall
L8: 
      lw t1,-12(sp) 
      lw t2,-16(sp) 
     add t1,t1,t2 
      sw t1,-32(sp) 
L9: 
      lw t1,-32(sp) 
      sw t1,-24(sp) 
L10: 
      lw t1,-16(sp) 
      sw t1,-12(sp) 
L11: 
      lw t1,-24(sp) 
      sw t1,-16(sp) 
L12: 
      lw t1,-20(sp) 
      li t2,1 
     add t1,t1,t2 
      sw t1,-36(sp) 
L13: 
      lw t1,-36(sp) 
      sw t1,-20(sp) 
L14: 
      b L5 
L15: 
      li t1,1 
      sw t1,-28(sp) 
L16: 
      li t1,1 
      sw t1,-20(sp) 
L17: 
      lw a0,-28(sp) 
     li a7,1
     ecall
     la a0,str_nl
     li a7,4
     ecall
L18: 
      lw t1,-28(sp) 
      lw t2,-20(sp) 
     mul t1,t1,t2 
      sw t1,-40(sp) 
L19: 
      lw t1,-40(sp) 
      sw t1,-28(sp) 
L20: 
      lw t1,-20(sp) 
      li t2,1 
     add t1,t1,t2 
      sw t1,-44(sp) 
L21: 
      lw t1,-44(sp) 
      sw t1,-20(sp) 
L22: 
      lw t1,-20(sp) 
      li t2,7 
     bgt t1,t2,L24 
L23: 
      b L17 
L24: 
     li a0,0
     li a7,93
     ecall
L25: 
