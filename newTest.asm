.data
str_nl: .asciz "\n"
.text
L0:   b Lτεστ 
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
      lw t1,-12(sp) 
      li t2,1 
     add t1,t1,t2 
      sw t1,-24(sp) 
L5: 
      lw t1,-24(sp) 
     lw t0,-8(sp)
     sw t1,(t0)
L6: 
      lw ra,-0(sp) 
      jr ra 
Lτεστ: 
L7: 
      addi sp,sp,32 
      mv gp,sp 
L8: 
      li t1,1 
      sw t1,-12(sp) 
L9: 
      li t1,3 
      sw t1,-24(sp) 
L10: 
      addi fp,sp,28 
      lw t0,-24(sp) 
      sw t0,-12(fp) 
L11: 
      addi t0,sp,-16 
      sw t0,-16(fp) 
L12: 
      addi t0,sp,-28 
      sw t0,-8(fp) 
L13: 
      sw sp,-4(fp) 
      addi sp,sp,28 
      jal L1 
      addi sp,sp,-28 
L14: 
      lw t1,-28(sp) 
      sw t1,-20(sp) 
L15: 
     li a0,0
     li a7,93
     ecall
L16: 
