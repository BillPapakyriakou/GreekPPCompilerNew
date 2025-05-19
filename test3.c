#include <stdio.h>

int main()
{
int income ;
int tax ;
int T_0 ;
int T_1 ;
int T_2 ;
int T_3 ;
int T_4 ;
int T_5 ;
int T_6 ;
int T_7 ;
int T_8 ;
int T_9 ;
int T_10 ;
int T_11 ;
int T_12 ;
int T_13 ;
int T_14 ;

L1: 
L2: scanf("%d",&income);
L3: if (income <= 1000) goto L5;
L4: goto L7;
L5: tax=0;
L6: goto L31;
L7: if (income <= 3000) goto L9;
L8: goto L13;
L9: T_0=income-1000;
L10: T_1=T_0/10;
L11: tax=T_1;
L12: goto L31;
L13: if (income <= 7000) goto L15;
L14: goto L22;
L15: T_2=3000-1000;
L16: T_3=T_2/10;
L17: T_4=income-3000;
L18: T_5=T_4/5;
L19: T_6=T_3+T_5;
L20: tax=T_6;
L21: goto L31;
L22: T_7=3000-1000;
L23: T_8=T_7/10;
L24: T_9=7000-3000;
L25: T_10=T_9/5;
L26: T_11=T_8+T_10;
L27: T_12=income-7000;
L28: T_13=T_12/2;
L29: T_14=T_11+T_13;
L30: tax=T_14;
L31: printf("%d\n",tax);
L32: 
L33: 
}

