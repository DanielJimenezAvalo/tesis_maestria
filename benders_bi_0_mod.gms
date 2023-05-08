*modelado de algoritmos de descomposicion con GAMS
*descomposicion de benders multietapa
*24 de setiembre de 2018
*Ing. Daniel Jimenez
Option Limrow=17;

sets
t        periodos  /1*13/
r        rows  /1*17/
s        stages  /1*2/
ss(s)    subconjunto dinamico
kk(s)    subconjunto dinamico 2
ssb(s)    subconjunto dinamico
kkb(s)    subconjunto dinamico 2
mmb(s)    subconjunto dinamico 3
snt      sentido de la descomposicion            /forwardpass, backwardpass/
iter     iteraciones de benders                  /1*5/
dyniter(iter)    subconjunto dinamico iteraciones
MAPSP(s,t)   map stage y periods     /
 1.1
 1.2
 1.3
 2.4
 2.5
/

MAPSrow(s,r)  map stage y periods   /
 1.1
 1.2
 2.3
 2.4
 2.5
 2.6
/

;

alias(t,t1,t2,t3);
alias(r,r1,r2,r3);
alias(s,s1,s2,s3,s4)
alias(iter,iter_1,iter_2);

parameters
c(s,t)     coeficientes FO  /
 1.1        184
 1.2        642
 1.3        312
 2.4        304
 2.5        472
/

;


parameters
b(s,r)     cotas restricciones   /
 1.1        2105
 1.2        2453
 2.3        4916
 2.4        2564
 2.5        1969
 2.6        1060
/

;


table A(s,r,s,t)     coeficientes restricciones master
           1.1       1.2       1.3       2.4       2.5      
 1.1        28        38        12         0         0        
 1.2        18        82        15         0         0        
 2.3        -4        -2        -6        61        74       
 2.4        -1        -2        -5        30        40        
 2.5        -7        -4        -4        50        95         
 2.6        -2        -3        -1        92        70         

;


positive variables
x(s,t)     variables

;

variables
Z        FO
alpha(s)    recursiva
;

parameters
k valor de periodo /1/
iteracion valor de iteracion /1/
TOL tolerancia /0.001/
*parametro_benders parametro /0.46496/
*parametro_benders parametro /2.1507/
parametro_benders parametro /0.000001/
dispb          parametro de desplazamiento

x_k(s,t)           variable perido previo
x_k_b(s,t)         variable perido previo
x_k_m(s,t)         variable perido previo
x_k_m_f(s,t)       variable perido previo
Z_k(s)           fo periodo previo
theta_k(s)       funcion recursiva
pi_k(s,r)          marginal de ecuacion
deltha_k(s)      factibilidad (0 0 1)

x_kk(iter,s,t)     variable perido previo
x_kk_b(iter,s,t)   variable perido previo
x_kk_m(iter,s,t)   variable perido previo
x_kk_m_f(iter,s,t) variable perido previo
Z_kk(iter,s)     fo periodo previo
Z_kk_b(iter,s)           fo periodo previo
theta_kk(iter,s)       funcion recursiva
alpha_kk(iter,s)       funcion recursiva
alpha_b_kk(iter,s)       funcion recursiva
pi_kk(iter,s,r)          marginal de ecuacion
pi_kk_f(iter,s,r)          marginal de ecuacion
mu_kk(iter,s)        dual del corte
betha_kk(iter,s)     cota del corte
deltha_kk(iter,s)        factibilidad (0 0 1)
Z_inferior(iter)    cota inferior
Z_inferior_1(iter)    cota inferior
Z_inferior_2(iter)    cota inferior
Z_inferior_3(iter)    cota inferior
Z_superior(iter)    cota superior
Z_inf    cota inferior
Z_sup    cota superior
GAP(iter) diferencias entre cotas
;

equations
eq_z1            funcion objetivo master primera iteracion benders
eq_zk            funcion objetivo master j iteracion benders
eq_zk1            funcion objetivo master j iteracion benders
eq_r1(s,r)         ecuaciones
eq_rk(iter,s,r)         ecuaciones
eq_rkb(iter,s)        ecuaciones
eq_rkf(iter,s)        ecuaciones
;

eq_z1..  sum[(s1,t1)$[ord(s1)=1],c(s1,t1)*x(s1,t1)]   =e= Z  ;

eq_zk1.. sum[(s1,t1)$[ord(s1)=k],c(s1,t1)*x(s1,t1)]   =e= Z  ;

eq_zk..  sum[(s1,t1)$[ord(s1)=k],c(s1,t1)*x(s1,t1)] + sum[s1$[ord(s1)=k],alpha(s1)]  =e= Z  ;

eq_r1(s2,r2)$[ord(s2)=k]..   sum[(s1,t1)$[MAPSP(s1,t1) and (ord(s1)=1)],A(s2,r2,s1,t1)*x(s1,t1)] =g= b(s2,r2);

eq_rk(iter_1,s2,r2)${[ord(s2)=k] and
                     [ord(iter_1) = iteracion   ]}..    sum[(s1,t1)$[MAPSP(s1,t1) and
                                                                         (ord(s1)=k)      ],A(s2,r2,s1,t1)*x(s1,t1)]
                                                           =g=
                                                           b(s2,r2)
                                                           -sum[(s1,t1)$[MAPSP(s1,t1) and
                                                                         (ord(s1)=k-1)    ],A(s2,r2,s1,t1)*x_kk(iter_1,s1,t1)]
                                                           ;

eq_rkf(iter_1,s2)$[(ord(s2)=k) and
                   (ord(iter_1)= iteracion-1 )]..    sum[s1$[ord(s1)=k],deltha_kk(iter_1,s1)*alpha(s1)-theta_kk(iter_1,s1)]
                                                     =g=
                                                     sum[(s1,r1,t2)$[MAPSROW(s1,r1) and
                                                                    (ord(s1)=k+1)   and
                                                                     MAPSP(s2,t2)   and
                                                                    (ord(s2)=k)        ], pi_kk(iter_1,s1,r1)*A(s1,r1,s2,t2)*{x_kk(iter_1,s2,t2)-x(s2,t2)}]
                                                     ;

eq_rkb(iter_1,s2)$[(ord(s2)=k) and
                   (ord(iter_1)= iteracion   )]..     sum[s1$[ord(s1)=k],deltha_kk(iter_1,s1)*alpha(s1)-theta_kk(iter_1,s1)]
                                                     =g=
                                                     sum[(s1,r1,t2)$[MAPSROW(s1,r1) and
                                                                    (ord(s1)=k+1)   and
                                                                     MAPSP(s2,t2)   and
                                                                    (ord(s2)=k)        ], pi_kk(iter_1,s1,r1)*A(s1,r1,s2,t2)*{x_kk(iter_1,s2,t2)-x(s2,t2)}]
                                                     ;

model multibenders1  /eq_z1, eq_r1/ ;
model multibenders2a /eq_zk1, eq_rk/ ;
model multibenders2  /eq_zk, eq_rk/ ;
model multibenders3  /eq_zk, eq_r1, eq_rkf/ ;
model multibenders4a /eq_zk, eq_rk, eq_rkf/ ;
model multibenders4  /eq_zk, eq_rk, eq_rkb/ ; 


ss(s)=no;
kk(s)=no;
dyniter(iter)=no;
Z_inferior(iter) = -inf;
Z_superior(iter) = inf;
Z_inf = -inf;
Z_sup = inf;


$onecho > cplex.opt
preind 0
scaind -1
lpmethod 1
$offecho

multibenders1.optfile=1 ;
multibenders2a.optfile=1 ;
multibenders2.optfile=1  ;
multibenders3.optfile=1  ;
multibenders4a.optfile=1  ;
multibenders4.optfile=1  ;

loop{iter${ABS(1-Z_inf/Z_sup) > TOL},
         iteracion=ord(iter);
         dyniter(iter)=yes;
         loop{snt,
                 if{ord(snt)=1,
                         loop {s,
                                 if{ord(iter)=1,
                                         if {ord(s)=1,
                                                K=ord(s);
                                                ss(s3)=yes$(ord(s3)=K);
                                                X.LO(ss,t)  =  0 ;
                                                X.UP(ss,t)  =  INF ;
                                                
*                                                multibenders1.savepoint=2;
                                                solve multibenders1 using LP minimizing Z;
                                                
*                                                execute_unload 'data_daniel.gdx';
                                                                                                

                                                 x_kk(dyniter,ss,t)=x.l(ss,t);
                                                 Z_kk(dyniter,ss)=Z.l;
                                                 pi_kk_f(dyniter,ss,r)=eq_r1.m(ss,r);
                                                 display Z_kk,ss;

                                         elseif ((ord(s)>1) and (ord(s)<card(s))),
                                                 K=ord(s);
                                                 ss(s3)=yes$(ord(s3)=K);
                                                 X.LO(ss,t)  =  0 ;
                                                 X.UP(ss,t)  =  INF ;
                                                 
                                                 multibenders2a.savepoint=2;

                                                 solve multibenders2a using LP minimizing Z;

                                                 x_kk(dyniter,ss,t)=x.l(ss,t);
                                                 Z_kk(dyniter,ss)=Z.l;
                                                 pi_kk_f(dyniter,ss,r)=eq_rk.m(iter,ss,r);
                                                 display Z_kk,ss;
                                         else
                                                 K=ord(s);
                                                 ss(s3)=yes$(ord(s3)=K);
                                                 kk(s3)=yes$(ord(s3)=K-1);
                                                 X.LO(ss,t)  =  0 ;
                                                 X.UP(ss,t)  =  INF ;
                                                 
                                                 multibenders2a.savepoint=2;

                                                 solve multibenders2a using LP minimizing Z;

                                                 if {multibenders2a.modelstat=4,
                                                         deltha_kk(dyniter,kk)=0;
                                                         theta_kk(dyniter,kk)=multibenders2a.suminfes;
                                                         

                                                 else
                                                         deltha_kk(dyniter,kk)=1;
                                                         theta_kk(dyniter,kk)=Z.l;
                                                 };

                                                 x_kk(dyniter,ss,t)=x.l(ss,t);
                                                 Z_kk(dyniter,ss)=Z.l;
                                                 pi_kk(dyniter,ss,r)=eq_rk.m(iter,ss,r);
                                                 Z_kk_b(dyniter,ss)=Z.l;
                                                 mu_kk(dyniter,ss)=0;
                                                 betha_kk(dyniter,ss)=0;

                                                 display theta_kk,ss,kk;
                                         };
                                 else
                                        if {ord(s)=1,
                                                 K=ord(s);
                                                 ss(s3)=yes$(ord(s3)=K);
                                                 X.LO(ss,t)  =  0 ;
                                                 X.UP(ss,t)  =  INF ;
                                                 alpha.LO(ss) =  -INF ;
                                                 alpha.UP(ss) =  INF ;
                                                 
                                                 multibenders3.savepoint=2;

                                                 solve multibenders3 using LP minimizing Z;

                                                 if{multibenders3.modelstat=3,
                                                         alpha.lo(ss)=sum[iter_2$[ord(iter_2)=iteracion-1],theta_kk(iter_2,ss)]*parametro_benders;
*                                                         alpha.lo(tt)=0
                                                         multibenders3.savepoint=2;

                                                         solve multibenders3 using LP minimizing Z;
                                                 };

                                                 x_kk(dyniter,ss,t)=x.l(ss,t);
                                                 Z_kk(dyniter,ss)=Z.l;
                                                 alpha_kk(dyniter,ss)=alpha.l(ss) ;
                                                 pi_kk_f(dyniter,ss,r)=eq_r1.m(ss,r);

                                                 display Z_kk,ss;

                                         elseif {(ord(s)>1) and (ord(s)<card(s))},
                                                 K=ord(s);
                                                 ss(s3)=yes$(ord(s3)=K);
                                                 X.LO(ss,t)  =  0 ;
                                                 X.UP(ss,t)  =  INF ;
                                                 alpha.LO(ss) =  -INF ;
                                                 alpha.UP(ss) =  INF ;
                                                 
                                                 multibenders4a.savepoint=2;

                                                 solve multibenders4a using LP minimizing Z;

                                                 if{multibenders4a.modelstat=3,
                                                         alpha.lo(ss)=sum[iter_2$[ord(iter_2)=iteracion-1],theta_kk(iter_2,ss)]*parametro_benders;
*                                                         alpha.lo(tt)=0

                                                         multibenders4a.savepoint=2;
                                                         solve multibenders4a using LP minimizing Z;
                                                 };

                                                 x_kk(dyniter,ss,t)=x.l(ss,t);
                                                 Z_kk(dyniter,ss)=Z.l;
                                                 alpha_kk(dyniter,ss)=alpha.l(ss) ;
                                                 pi_kk_f(dyniter,ss,r)=eq_rk.m(iter,ss,r);

                                                 display Z_kk,ss;

                                         else
                                                 K=ord(s);
                                                 ss(s3)=yes$(ord(s3)=K);
                                                 kk(s3)=yes$(ord(s3)=K-1);
                                                 X.LO(ss,t)  =  0 ;
                                                 X.UP(ss,t)  =  INF ;
                                                 alpha.LO(ss) = -INF ;
                                                 alpha.UP(ss) = INF ;
                                                    
                                                 multibenders2a.savepoint=2;

                                                 solve multibenders2a using LP minimizing Z;

                                                 if{multibenders2a.modelstat=3,
                                                         alpha.lo(ss)=sum[iter_2$[ord(iter_2)=iteracion-1],theta_kk(iter_2,ss)]*parametro_benders;
*                                                         alpha.lo(tt)=0

                                                         multibenders2a.savepoint=2;
                                                         solve multibenders2a using LP minimizing Z;
                                                 };

                                                 if {multibenders2a.modelstat=4,
                                                         deltha_kk(dyniter,kk)=0;
                                                         theta_kk(dyniter,kk)=multibenders2a.suminfes;
                                                 else
                                                         deltha_kk(dyniter,kk)=1;
                                                         theta_kk(dyniter,kk)=Z.l;
                                                 };

                                                 x_kk(dyniter,ss,t)=x.l(ss,t);
                                                 Z_kk(dyniter,ss)=Z.l;
                                                 pi_kk(dyniter,ss,r)=eq_rk.m(iter,ss,r);
                                                 Z_kk_b(dyniter,ss)=Z.l;
                                                 mu_kk(dyniter,ss)=eq_rkf.m(iter,ss);
                                                 betha_kk(dyniter,ss)=0;

                                                 display Z_kk,ss,kk;
                                         };
                                 };
                         };
                 else
                         loop {s$[(ord(s)>1) and (ord(s)<card(s))],
                                 K=card(s)-ord(s)+1;
                                 dispb= card(s) - 2*ord(s) + 1;

                                 ssb(s3)=yes$(ord(s3)=ord(s)+dispb);
                                 kkb(s3)=yes$(ord(s3)=ord(s)+dispb-1);
                                 mmb(s3)=yes$(ord(s3)=ord(s) +dispb+1);


                                 X.LO(ssb,t)  =  0 ;
                                 X.UP(ssb,t)  =  INF ;
                                 alpha.LO(ssb) = -INF ;
                                 alpha.UP(ssb) = INF ;
                                 
                                 multibenders4.savepoint=2;

                                 solve multibenders4 using LP minimizing Z;

                                 if{multibenders4.modelstat=3,
                                 alpha.lo(ssb)= theta_kk(iter,ssb)*parametro_benders;
*                                 alpha.lo(ttb)= 0;
                                 multibenders4.savepoint=2;
                                 solve multibenders4 using LP minimizing Z;
                                 };
                                 if {multibenders4.modelstat=4,
                                         deltha_kk(dyniter,kkb)=0;
                                         theta_kk(dyniter,kkb)=multibenders4.suminfes;

                                 else
                                         deltha_kk(dyniter,kkb)=1;
                                         theta_kk(dyniter,kkb)=Z.l;
                                 };

                                 alpha_b_kk(dyniter,ssb)=alpha.l(ssb) ;
                                 pi_kk(dyniter,ssb,r)=eq_rk.m(iter,ssb,r);
                                 x_kk_b(dyniter,ssb,t)=x.l(ssb,t);
                                 Z_kk_b(dyniter,ssb)=Z.l;
                                 mu_kk(dyniter,ssb)=eq_rkb.m(iter,ssb);
                                 betha_kk(dyniter,ssb)=sum[(s4,r)$(ord(s4)=k+1),pi_kk(iter,s4,r)*b(s4,r)]+
                                                       sum[s4$(ord(s4)=k+1),mu_kk(iter,s4)     ]*sum[s4$(ord(s4)=k+1),betha_kk(iter,s4)];
                                 display Z_kk_b,ssb,kkb;

                         };

                 };
         };
         if {ord(iter)=1,
                 Z_inferior(iter)=sum[t,c("1",t)*x_kk(iter,"1",t)];
                 Z_inf = sum[t,c("1",t)*x_kk(iter,"1",t)];
         else
                 Z_inferior(iter)  = sum[t,c("1",t)*x_kk(iter,"1",t)] + sum[(s2,r2)$[MAPSROW(s2,r2) and (ord(s2)=2)],pi_kk(iter,s2,r2)*[b(s2,r2)-sum[(s1,t1)$[MAPSP(s1,t1) and (ord(s1)=1)],A(s2,r2,s1,t1)*x_kk(iter,s1,t1)]]]+mu_kk(iter,"2")*betha_kk(iter,"2");
                 Z_inferior_1(iter)= sum[t,c("1",t)*x_kk(iter,"1",t)] + theta_kk(iter,"1");
                 Z_inferior_2(iter)= sum[t,c("1",t)*x_kk(iter,"1",t)] + alpha_kk(iter,"1");
                 Z_inf = alpha_kk(iter,"1");
         };
         Z_superior(iter)=sum[(s,t)$MAPSP(s,t),c(s,t)*x_kk(iter,s,t)];
         Z_sup=sum[(s,t)$[(ord(s)>1) and MAPSP(s,t)],c(s,t)*x_kk(iter,s,t)];
         GAP(iter)=ABS(1-Z_inf/Z_sup)

         display x_kk, x_kk_b,pi_kk, pi_kk_f,deltha_kk,theta_kk, alpha_b_kk,alpha_kk, mu_kk, betha_kk, Z_kk, Z_kk_b,Z_inferior, Z_inferior_1,Z_inferior_2,Z_superior, Z_sup, Z_inf,GAP,dyniter;
         dyniter(iter)=no;
};
