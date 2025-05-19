.data
str_nl: .asciz "\n"
.text
L0:   b Lτεστ 
Lτεστ: 
L1: 
      addi sp,sp,80 
      mv gp,sp 
L2: 
     li a7,5
     ecall
      sw a0,-12(sp) 
L3: 
      lw t1,-12(sp) 
      li t2,1000 
     ble t1,t2,L5 
L4: 
      b L7 
L5: 
      li t1,0 
      sw t1,-16(sp) 
L6: 
      b L31 
L7: 
      lw t1,-12(sp) 
      li t2,3000 
     ble t1,t2,L9 
L8: 
      b L13 
L9: 
      lw t1,-12(sp) 
      li t2,1000 
     sub t1,t1,t2 
      sw t1,-20(sp) 
L10: 
      lw t1,-20(sp) 
      li t2,10 
     div t1,t1,t2 
      sw t1,-24(sp) 
L11: 
      lw t1,-24(sp) 
      sw t1,-16(sp) 
L12: 
      b L31 
L13: 
      lw t1,-12(sp) 
      li t2,7000 
     ble t1,t2,L15 
L14: 
      b L22 
L15: 
      li t1,3000 
      li t2,1000 
     sub t1,t1,t2 
      sw t1,-28(sp) 
L16: 
      lw t1,-28(sp) 
      li t2,10 
     div t1,t1,t2 
      sw t1,-32(sp) 
L17: 
      lw t1,-12(sp) 
      li t2,3000 
     sub t1,t1,t2 
      sw t1,-36(sp) 
L18: 
      lw t1,-36(sp) 
      li t2,5 
     div t1,t1,t2 
      sw t1,-40(sp) 
L19: 
      lw t1,-32(sp) 
      lw t2,-40(sp) 
     add t1,t1,t2 
      sw t1,-44(sp) 
L20: 
      lw t1,-44(sp) 
      sw t1,-16(sp) 
L21: 
      b L31 
L22: 
      li t1,3000 
      li t2,1000 
     sub t1,t1,t2 
      sw t1,-48(sp) 
L23: 
      lw t1,-48(sp) 
      li t2,10 
     div t1,t1,t2 
      sw t1,-52(sp) 
L24: 
      li t1,7000 
      li t2,3000 
     sub t1,t1,t2 
      sw t1,-56(sp) 
L25: 
      lw t1,-56(sp) 
      li t2,5 
     div t1,t1,t2 
      sw t1,-60(sp) 
L26: 
      lw t1,-52(sp) 
      lw t2,-60(sp) 
     add t1,t1,t2 
      sw t1,-64(sp) 
L27: 
      lw t1,-12(sp) 
      li t2,7000 
     sub t1,t1,t2 
      sw t1,-68(sp) 
L28: 
      lw t1,-68(sp) 
      li t2,2 
     div t1,t1,t2 
      sw t1,-72(sp) 
L29: 
      lw t1,-64(sp) 
      lw t2,-72(sp) 
     add t1,t1,t2 
      sw t1,-76(sp) 
L30: 
      lw t1,-76(sp) 
      sw t1,-16(sp) 
L31: 
      lw a0,-16(sp) 
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
