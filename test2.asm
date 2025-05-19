.data
str_nl: .asciz "\n"
.text
L0:   b Lτεστ2 
Lτεστ2: 
L1: 
      addi sp,sp,44 
      mv gp,sp 
L2: 
      li t1,1 
      sw t1,-12(sp) 
L3: 
      lw t1,-12(sp) 
      li t2,10 
     blt t1,t2,L5 
L4: 
      b L8 
L5: 
      lw t1,-12(sp) 
      li t2,1 
     add t1,t1,t2 
      sw t1,-20(sp) 
L6: 
      lw t1,-20(sp) 
      sw t1,-12(sp) 
L7: 
      b L3 
L8: 
      lw a0,-12(sp) 
     li a7,1
     ecall
     la a0,str_nl
     li a7,4
     ecall
L9: 
      lw t1,-12(sp) 
      sw t1,-16(sp) 
L10: 
      lw t1,-16(sp) 
      li t2,1 
     add t1,t1,t2 
      sw t1,-24(sp) 
L11: 
      lw t1,-24(sp) 
      sw t1,-16(sp) 
L12: 
      lw t1,-16(sp) 
      li t2,2 
     sub t1,t1,t2 
      sw t1,-28(sp) 
L13: 
      lw t1,-28(sp) 
      sw t1,-16(sp) 
L14: 
      lw t1,-16(sp) 
      li t2,0 
     beq t1,t2,L16 
L15: 
      b L10 
L16: 
      lw a0,-16(sp) 
     li a7,1
     ecall
     la a0,str_nl
     li a7,4
     ecall
L17: 
      li t1,0 
      li t2,1 
     sub t1,t1,t2 
      sw t1,-32(sp) 
L18: 
      lw t1,-16(sp) 
      lw t2,-32(sp) 
     ble t1,t2,L20 
L19: 
      b L23 
L20: 
      li t1,0 
      li t2,1 
     sub t1,t1,t2 
      sw t1,-36(sp) 
L21: 
      lw t1,-36(sp) 
      sw t1,-12(sp) 
L22: 
      b L25 
L23: 
      li t1,0 
      li t2,2 
     sub t1,t1,t2 
      sw t1,-40(sp) 
L24: 
      lw t1,-40(sp) 
      sw t1,-12(sp) 
L25: 
      lw a0,-12(sp) 
     li a7,1
     ecall
     la a0,str_nl
     li a7,4
     ecall
L26: 
      lw t1,-12(sp) 
      lw t2,-16(sp) 
     blt t1,t2,L28 
L27: 
      b L30 
L28: 
      li t1,1 
      sw t1,-12(sp) 
L29: 
      b L31 
L30: 
      li t1,2 
      sw t1,-12(sp) 
L31: 
      lw a0,-12(sp) 
     li a7,1
     ecall
     la a0,str_nl
     li a7,4
     ecall
L32: 
     li a0,0
     li a7,93
     ecall
L33: 
