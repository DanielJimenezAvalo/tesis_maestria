
sets
t        periodos   
r        rows       
s        stages  
snt     forward o backward
iter    iteration index   

MAPSP(s,t)
MAPSrow(s,r)

;

alias(t,t1,t2,t3);
alias(r,r1,r2,r3);
alias(s,s1,s2,s3,s4)
alias(iter,iter_1,iter_2);

parameters
c(s,t)     coeficientes FO 
b(s,r)     cotas restricciones 
A(s,r,s,t)    coeficientes restricciones master    
;

parameters
k valor de periodo 
iteracion valor de iteracion 
TOL tolerancia 
parametro_benders parametro 
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

$if not set gdxincname $abort 'no include file name for data file provided'
$gdxin %gdxincname%
$load t r s MAPSP MAPSrow c b A k iteracion x_kk Z_kk
$gdxin

positive variables
x(s,t)     variables
;

variables
Z      FO
alpha(s)    recursiva
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

    