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
      sw t1,-12(sp) 
L4: 
      lw t1,-12(sp) 
      li t2,1 
     add t1,t1,t2 
      sw t1,-24(sp) 
L5: 
      lw t1,-24(sp) 
      lw t0,-16(sp) 
      sw t1,(t0) 
L6: 
      lw ra,-0(sp) 
      jr ra 
L7: 
      sw ra,-0(sp) 
L8: 
      addi fp,sp,28 
      lw t0,-12(sp) 
      sw t0,-12(fp) 
L9: 
      addi t0,sp,-20 
      sw t0,-8(fp) 
L10: 
      sw sp,-4(fp) 
      addi sp,sp,28 
      jal L1 
      addi sp,sp,-28 
L11: 
      lw t1,-20(sp) 
      lw t0,-16(sp) 
      sw t1,(t0) 
L12: 
      lw ra,-0(sp) 
      jr ra 
Lτεστ: 
L13: 
      addi sp,sp,28 
      mv gp,sp 
L14: 
      li t1,1 
      sw t1,-12(sp) 
L15: 
      addi fp,sp,24 
      lw t0,-12(sp) 
      sw t0,-16(fp) 
L16: 
      addi t0,sp,-24 
      sw t0,-8(fp) 
L17: 
      sw sp,-4(fp) 
      addi sp,sp,24 
      jal L7 
      addi sp,sp,-24 
L18: 
      lw t1,-24(sp) 
      sw t1,-20(sp) 
L19: 
     li a0,0
     li a7,93
     ecall
L20: 
