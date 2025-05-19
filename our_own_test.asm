.data
str_nl: .asciz "\n"
.text
L0:   b LΤεστ_Συντακτικού 
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
      lw ra,-0(sp) 
      jr ra 
L5: 
      sw ra,-0(sp) 
L6: 
      lw t1,-12(sp) 
      li t2,1 
     add t1,t1,t2 
      sw t1,-16(sp) 
L7: 
      lw t1,-16(sp) 
      li t2,3 
     mul t1,t1,t2 
      sw t1,-20(sp) 
L8: 
      lw a0,-20(sp) 
     li a7,1
     ecall
     la a0,str_nl
     li a7,4
     ecall
L9: 
      lw ra,-0(sp) 
      jr ra 
LΤεστ_Συντακτικού: 
L10: 
      addi sp,sp,68 
      mv gp,sp 
L11: 
      li t1,10 
      sw t1,-28(sp) 
L12: 
      lw a0,-28(sp) 
     li a7,1
     ecall
     la a0,str_nl
     li a7,4
     ecall
L13: 
      lw t1,-28(sp) 
      li t2,5 
     bgt t1,t2,L15 
L14: 
      b L19 
L15: 
      lw t1,-28(sp) 
      li t2,20 
     blt t1,t2,L17 
L16: 
      b L19 
L17: 
      li a0,0 
     li a7,1
     ecall
     la a0,str_nl
     li a7,4
     ecall
L18: 
      b L20 
L19: 
      li a0,1 
     li a7,1
     ecall
     la a0,str_nl
     li a7,4
     ecall
L20: 
      lw t1,-28(sp) 
      li t2,15 
     ble t1,t2,L27 
L21: 
      b L22 
L22: 
      lw t1,-28(sp) 
      li t2,1 
     add t1,t1,t2 
      sw t1,-32(sp) 
L23: 
      lw t1,-32(sp) 
      sw t1,-28(sp) 
L24: 
      lw t1,-28(sp) 
      li t2,1 
     mul t1,t1,t2 
      sw t1,-36(sp) 
L25: 
      lw a0,-36(sp) 
     li a7,1
     ecall
     la a0,str_nl
     li a7,4
     ecall
L26: 
      b L20 
L27: 
      lw t1,-28(sp) 
      li t2,1 
     sub t1,t1,t2 
      sw t1,-40(sp) 
L28: 
      lw t1,-40(sp) 
      sw t1,-28(sp) 
L29: 
      lw t1,-28(sp) 
      li t2,1 
     sub t1,t1,t2 
      sw t1,-44(sp) 
L30: 
      lw a0,-44(sp) 
     li a7,1
     ecall
     la a0,str_nl
     li a7,4
     ecall
L31: 
      lw t1,-28(sp) 
      li t2,10 
     beq t1,t2,L33 
L32: 
      b L27 
L33: 
      li t1,1 
      sw t1,-24(sp) 
L34: 
      lw t1,-24(sp) 
      li t2,5 
     ble t1,t2,L_ 
L35: 
      b L40 
L36: 
      lw a0,-24(sp) 
     li a7,1
     ecall
     la a0,str_nl
     li a7,4
     ecall
L37: 
      lw t1,-24(sp) 
      li t2,1 
     add t1,t1,t2 
      sw t1,-48(sp) 
L38: 
      lw t1,-48(sp) 
      sw t1,-24(sp) 
L39: 
      b L34 
L40: 
     li a7,5
     ecall
      sw a0,-20(sp) 
L41: 
      lw a0,-20(sp) 
     li a7,1
     ecall
     la a0,str_nl
     li a7,4
     ecall
L42: 
      addi fp,sp,24 
      lw t0,-28(sp) 
      sw t0,-12(fp) 
L43: 
      addi t0,sp,-16 
      sw t0,-16(fp) 
L44: 
      addi t0,sp,-52 
      sw t0,-8(fp) 
L45: 
      sw sp,-4(fp) 
      addi sp,sp,24 
      jal L1 
      addi sp,sp,-24 
L46: 
      lw t1,-52(sp) 
      sw t1,-20(sp) 
L47: 
      addi fp,sp,24 
      lw t0,-28(sp) 
      sw t0,-20(fp) 
L48: 
      lw t0,-20(sp) 
      sw t0,-24(fp) 
L49: 
      addi t0,sp,-56 
      sw t0,-8(fp) 
L50: 
      sw sp,-4(fp) 
      addi sp,sp,24 
      jal L1 
      addi sp,sp,-24 
L51: 
      lw t1,-56(sp) 
      sw t1,-12(sp) 
L52: 
     li a7,5
     ecall
      sw a0,-16(sp) 
L53: 
      lw a0,-16(sp) 
     li a7,1
     ecall
     la a0,str_nl
     li a7,4
     ecall
L54: 
      addi fp,sp,24 
      lw t0,-28(sp) 
      sw t0,-12(fp) 
L55: 
      sw sp,-4(fp) 
      addi sp,sp,24 
      jal L5 
      addi sp,sp,-24 
L56: 
     li a7,5
     ecall
      sw a0,-16(sp) 
L57: 
      lw t1,-16(sp) 
      li t2,2 
     mul t1,t1,t2 
      sw t1,-60(sp) 
L58: 
      lw t1,-60(sp) 
      sw t1,-16(sp) 
L59: 
      li t1,0 
      li t2,120 
     sub t1,t1,t2 
      sw t1,-64(sp) 
L60: 
      lw t1,-16(sp) 
      lw t2,-64(sp) 
     ble t1,t2,L62 
L61: 
      b L57 
L62: 
     li a0,0
     li a7,93
     ecall
L63: 
