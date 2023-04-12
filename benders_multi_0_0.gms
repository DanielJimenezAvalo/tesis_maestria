*modelado de algoritmos de descomposicion con GAMS
*descomposicion de benders multietapa
*27 de enero de 2016
*Ing. Daniel Jimenez
*  min z = 8x1+10x2+12x3+16x4
*          2x1                   = 50
*        +12x1+15x2              = 60
*              13x2+9x3          = 70
*                  +3x3+32x4     = 80

$INCLUDE ./input.DAT

positive variables
x(i)     variables
;

variables
Z      FO
*x(i)     variables
;

equations
eq_z      funcion objetivo master
eq_r1(m)  ecuaciones
;

eq_z..           sum[i, c(i)*x(i)]   =e= Z  ;

eq_r1(m)..       sum[i, A(m,i)*x(i)] =g= B(m);


model multibenders /all/

solve multibenders using LP minimizing Z;

execute_unload 'data_final.gdx';

FILE RESULTADO_FINAL /salida.put/;
PUT RESULTADO_FINAL;
RESULTADO_FINAL.nd = 2;
RESULTADO_FINAL.nj = 2;
RESULTADO_FINAL.pw = 5000;

PUT "i    ",PUT "x"/;
PUT /
LOOP(i,
        PUT i.tl:7,PUT x.l(i);
        PUT ""/;
);
PUT ""/

