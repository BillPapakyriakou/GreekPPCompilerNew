.data
str_nl: .asciz "\n"
.text
L0:   b Lκυρίως 
L1: 
      sw ra,-0(sp) 
L2: 
      lw t1,-12(sp) 
      li t2,1 
     add t1,t1,t2 
      sw t1,-20(sp) 
L3: 
      lw t1,-20(sp) 
      lw t0,-16(sp) 
      sw t1,(t0) 
L4: 
      li t1,4 
      sw t1,-20(gp) 
L5: 
      lw t0,-16(sp) 
      lw t1,(t0) 
     lw t0,-8(sp)
     sw t1,(t0)
L6: 
      lw ra,-0(sp) 
      jr ra 
Lκυρίως: 
L7: 
      addi sp,sp,28 
      mv gp,sp 
L8: 
      li t1,1 
      sw t1,-12(sp) 
L9: 
      addi fp,sp,24 
      lw t0,-12(sp) 
      sw t0,-12(fp) 
L10: 
      addi t0,sp,-16 
      sw t0,-16(fp) 
L11: 
      addi t0,sp,-24 
      sw t0,-8(fp) 
L12: 
      sw sp,-4(fp) 
      addi sp,sp,24 
      jal L1 
      addi sp,sp,-24 
L13: 
      lw t1,-24(sp) 
      sw t1,-20(sp) 
L14: 
      lw a0,-20(sp) 
     li a7,1
     ecall
     la a0,str_nl
     li a7,4
     ecall
L15: 
      lw a0,-16(sp) 
     li a7,1
     ecall
     la a0,str_nl
     li a7,4
     ecall
L16: 
     li a0,0
     li a7,93
     ecall
L17: 
