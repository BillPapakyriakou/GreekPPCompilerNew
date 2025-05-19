#include <stdio.h>

int main()
{
int a ;
int b ;
int i ;
int T_0 ;
int t ;
int T_1 ;
int pi ;
int T_2 ;
int T_3 ;

L1: 
L2: a=0;
L3: b=1;
L4: i=0;
L5: if (i <= 10) goto L7;
L6: goto L15;
L7: printf("%d\n",a);
L8: T_0=a+b;
L9: t=T_0;
L10: a=b;
L11: b=t;
L12: T_1=i+1;
L13: i=T_1;
L14: goto L5;
L15: pi=1;
L16: i=1;
L17: printf("%d\n",pi);
L18: T_2=pi*i;
L19: pi=T_2;
L20: T_3=i+1;
L21: i=T_3;
L22: if (i > 7) goto L24;
L23: goto L17;
L24: 
L25: 
}

