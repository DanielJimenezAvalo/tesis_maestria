*modelado de algoritmos de descomposicion con GAMS
*descomposicion de benders multietapa
*27 de enero de 2016
*Ing. Daniel Jimenez
*  min z = 8x1+10x2+12x3+16x4
*          2x1                   = 50
*        +12x1+15x2              = 60
*              13x2+9x3          = 70
*                  +3x3+32x4     = 80

*$INCLUDE ./input.DAT
*$INCLUDE ./original.txt
Option Limrow=17;

sets
t        periodos   /1*13/
r        rows       /1*17/
s        stages     /1*5/



MAPSP(s,t)   map stage y periods     /
 1.1
 1.2
 1.3
 2.4
 2.5
 3.6
 3.7
 3.8
 3.9
4.10
5.11
5.12
5.13
/

MAPSrow(s,r)  map stage y periods   /
 1.1
 1.2
 2.3
 2.4
 2.5
 2.6
 3.7
 3.8
 3.9
4.10
4.11
4.12
5.13
5.14
5.15
5.16
5.17
/
;

alias(s,ss);

parameters
c(s,t)     coeficientes FO  /
 1.1        184
 1.2        642
 1.3        312
 2.4        304
 2.5        472
 3.6        305
 3.7        531
 3.8        805
 3.9        516
4.10        344
5.11        740
5.12        764
5.13        386
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
 3.7        3951
 3.8        1383
 3.9        2783
4.10        2667
4.11        3791
4.12        1039
5.13        4756
5.14        2782
5.15        2725
5.16        3235
5.17        3436
/
;


table A(s,r,s,t)     coeficientes restricciones master
           1.1       1.2       1.3       2.4       2.5       3.6       3.7       3.8       3.9      4.10      5.11      5.12      5.13
 1.1        28        38        12         0         0         0         0         0         0         0         0         0         0
 1.2        18        82        15         0         0         0         0         0         0         0         0         0         0
 2.3        -4        -2        -6        61        74         0         0         0         0         0         0         0         0
 2.4        -1        -2        -5        30        40         0         0         0         0         0         0         0         0
 2.5        -7        -4        -4        50        95         0         0         0         0         0         0         0         0
 2.6        -2        -3        -1        92        70         0         0         0         0         0         0         0         0
 3.7         0         0         0        -9        -7        88        48        26        21         0         0         0         0
 3.8         0         0         0        -8        -9        81        19        95        70         0         0         0         0
 3.9         0         0         0        -7        -7        55        26        51        24         0         0         0         0
4.10         0         0         0         0         0        -8        -7        -6        -1        24         0         0         0
4.11         0         0         0         0         0        -4        -4        -7        -3        32         0         0         0
4.12         0         0         0         0         0        -9        -6        -6        -8        70         0         0         0
5.13         0         0         0         0         0         0         0         0         0        -3        69        62        99
5.14         0         0         0         0         0         0         0         0         0        -8        64        48        26
5.15         0         0         0         0         0         0         0         0         0        -5        60        28        16
5.16         0         0         0         0         0         0         0         0         0        -6        85        57        99
5.17         0         0         0         0         0         0         0         0         0        -3        68        32        91
;

positive variables
x(s,t)     variables
;

variables
Z      FO
*x(i)     variables
;

equations
eq_z      funcion objetivo master
eq_rk(s,r)  ecuaciones
;

eq_z..          sum[(s,t),c(s,t)*x(s,t)]   =e= Z  ;

eq_rk(s,r)..    sum[(ss,t)$MAPSP(ss,t),A(s,r,ss,t)*x(ss,t)]=g= b(s,r) ;


model multibenders /all/

solve multibenders using LP minimizing Z;

execute_unload 'data_final.gdx';