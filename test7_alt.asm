.data
str_nl: .asciz "\n"
.text
L0:   b Lκυρίως 
L1: 
      sw ra,-0(sp) 
L2: 
      lw t1,-16(gp) 
      sw t1,-20(gp) 
L3: 
      lw t0,-4(sp) 
      addi t0,t0,-12 
      lw t1,(t0) 
      sw t1,-16(gp) 
L4: 
      lw ra,-0(sp) 
      jr ra 
L5: 
      sw ra,-0(sp) 
L6: 
      li t1,2 
      sw t1,-16(gp) 
L7: 
      addi fp,sp,20 
      sw sp,-4(fp) 
      addi sp,sp,12 
      jal L1 
      addi sp,sp,-12 
L8: 
      lw ra,-0(sp) 
      jr ra 
Lκυρίως: 
L9: 
      addi sp,sp,36 
      mv gp,sp 
L10: 
      li t1,3 
      sw t1,-12(sp) 
L11: 
      li t1,4 
      sw t1,-16(sp) 
L12: 
      addi fp,sp,20 
      lw t0,-12(sp) 
      sw t0,-12(fp) 
L13: 
      addi t0,sp,-16 
      sw t0,-16(fp) 
L14: 
      addi t0,sp,-28 
      sw t0,-8(fp) 
L15: 
      sw sp,-4(fp) 
      addi sp,sp,20 
      jal L5 
      addi sp,sp,-20 
L16: 
      lw t1,-28(sp) 
      li t2,2 
     add t1,t1,t2 
      sw t1,-32(sp) 
L17: 
      lw t1,-32(sp) 
      sw t1,-12(sp) 
L18: 
      lw a0,-16(sp) 
     li a7,1
     ecall
     la a0,str_nl
     li a7,4
     ecall
L19: 
      lw a0,-20(sp) 
     li a7,1
     ecall
     la a0,str_nl
     li a7,4
     ecall
L20: 
     li a0,0
     li a7,93
     ecall
L21: 
