#include <stdio.h>

int main()
{
int age ;
int income ;
int creditScore ;

L1: 
L2: scanf("%d",&age);
L3: scanf("%d",&creditScore);
L4: scanf("%d",&income);
L5: if (age >= 18) goto L7;
L6: goto L21;
L7: if (age <= 65) goto L9;
L8: goto L21;
L9: if (income >= 2000) goto L11;
L10: goto L13;
L11: if (creditScore >= 650) goto L19;
L12: goto L13;
L13: if (income >= 5000) goto L19;
L14: goto L15;
L15: if (creditScore >= 700) goto L17;
L16: goto L21;
L17: if (income >= 1500) goto L19;
L18: goto L21;
L19: printf("%d\n",1);
L20: goto L22;
L21: printf("%d\n",0);
L22: 
L23: 
}

