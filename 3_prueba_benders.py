from gams import GamsWorkspace, GamsModifier, UpdateAction, VarType
import gams.transfer as gt
import os
import sys
import pkg
import threading
import math
import pandas as pd
import numpy as np

def get_data_text():
    return '''
sets
t        periodos   /1*13/
r        rows       /1*17/
s        stages     /1*5/
iter     iteraciones /1*5/
snt      sentido    /forward,backward/

MAPSP(s,t)   map s y periods     /
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

MAPSrow(s,r)  map s y periods   /
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

    '''
model_container=gt.Container()

#t=model_container.addSet('t',records=['1','2','3','4','5','6','7','8','9','10','11','12','13'])
t_set_array=['1','2','3','4','5','6','7','8','9','10','11','12','13']
t=gt.Set(model_container,'t',description="set of columns")
t.setRecords(t_set_array)

#r=model_container.addSet('r',records=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17'])
r_set_array=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17']
r=gt.Set(model_container,'r',description="set of rows")
r.setRecords(r_set_array)

#s=model_container.addSet('s',records=['1','2','3','4','5'])
s_set_array=['1','2','3','4','5']
s=gt.Set(model_container,'s',description="stages")
s.setRecords(s_set_array)

#iter=model_container.addSet('iter',records=['1','2','3','4','5'])
iter_set_array=['1','2','3','4','5']
iter=gt.Set(model_container,'iter',description="stages")
iter.setRecords(iter_set_array)

#snt=model_container.addSet('snt',records=['forward','backward'])
snt_set_iter=['forward','backward']
snt=gt.Set(model_container,'snt',description="sntido del recorrido de la descomposicion")
snt.setRecords(snt_set_iter)

#map stage column
mapsp_set_array=[('1','1'),('1','2'),('1','3'),('2','4'),('2','5'),
                ('3','6'),('3','7'),('3','8'),('3','9'),('4','10'),
                ('5','11'),('5','12'),('5','13')]

mapsp=gt.Set(model_container,'MAPSP',[s,t],description="map stage column")
mapsp.setRecords(mapsp_set_array)

#map row stage
mapsrow_set_array=[('1','1'),('1','2'),('1','3'),('2','4'),('2','5'), ('2','6'),
                    ('3','7'), ('3','8'),('3','9'),('4','10'),('4','11'),('4','12'),
                    ('5','13'),('5','14'),('5','15'),('5','16'),('5','17'),]

mapsrow=gt.Set(model_container,'MAPSrow',[s,r],description="map row stage")
mapsrow.setRecords(mapsrow_set_array)                    

#parameters
# c coefficients of object function
c_df_parameter=pd.DataFrame(
        [
            ('1','1',184),
            ('1','2',642),
            ('1','3',312),
            ('2','4',304),
            ('2','5',472),
            ('3','6',305),
            ('3','7',531),
            ('3','8',805),
            ('3','9',516),
            ('4','10',344),
            ('5','11',740),
            ('5','12',764),
            ('5','13',386)
        ],
        columns=['s','t','value']
)

c=gt.Parameter(model_container,'c',[s,t])
c.setRecords(c_df_parameter)

# d coefficients of restrictions
b_df_parameters=pd.DataFrame(
        [
            ('1','1',2105),
            ('1','2',2453),
            ('2','3',4916),
            ('2','4',2564),
            ('2','5',1969),
            ('2','6',1060),
            ('3','7',3951),
            ('3','8',1383),
            ('3','9',2783),
            ('4','10',2667),
            ('4','11',3791),
            ('4','12',1039),
            ('5','13',4756),
            ('5','14',2782),
            ('5','15',2725),
            ('5','16',3235),
            ('5','17',3436)                                 
        ],
        columns=['s','r','value']
)

b=gt.Parameter(model_container,'b',[s,r])
b.setRecords(b_df_parameters)

# table A(s,r,s,t)     coeficientes restricciones master
A_df_parameters=pd.DataFrame(
            [
                ('1','1','1','1',28),
                ('1','1','1','2',38),
                ('1','1','1','3',12),
                ('1','2','1','1',18),
                ('1','2','1','2',82),
                ('1','2','1','3',15),
                ('2','3','1','1',-4),
                ('2','3','1','2',-2),
                ('2','3','1','3',-6),
                ('2','3','2','4',61),
                ('2','3','2','5',74),
                ('2','4','1','1',-1),
                ('2','4','1','2',-2),
                ('2','4','1','3',-5),
                ('2','4','2','4',30),
                ('2','4','2','5',40),
                ('2','5','1','1',-7),
                ('2','5','1','2',-4),
                ('2','5','1','3',-4),
                ('2','5','2','4',50),
                ('2','5','2','5',95),
                ('2','6','1','1',-2),
                ('2','6','1','2',-3),
                ('2','6','1','3',-1),
                ('2','6','2','4',92),
                ('2','6','2','5',70),
                ('3','7','2','4',-9),
                ('3','7','2','5',-7),
                ('3','7','3','6',88),
                ('3','7','3','7',48),
                ('3','7','3','8',26),
                ('3','7','3','9',21),
                ('3','8','2','4',-8),
                ('3','8','2','5',-9),
                ('3','8','3','6',81),
                ('3','8','3','7',19),
                ('3','8','3','8',95),
                ('3','8','3','9',70),
                ('3','9','2','4',-7),
                ('3','9','2','5',-7),
                ('3','9','3','6',55),
                ('3','9','3','7',26),
                ('3','9','3','8',51),
                ('3','9','3','9',24),
                ('4','10','3','6',-8),
                ('4','10','3','7',-7),
                ('4','10','3','8',-6),
                ('4','10','3','9',-1),
                ('4','10','4','10',24),
                ('4','11','3','6',-4),
                ('4','11','3','7',-4),
                ('4','11','3','8',-7),
                ('4','11','3','9',-3),
                ('4','11','4','10',32),
                ('4','12','3','6',-9),
                ('4','12','3','7',-6),
                ('4','12','3','8',-6),
                ('4','12','3','9',-8),
                ('4','12','4','10',70),
                ('5','13','4','10',-3),
                ('5','13','5','11',69),
                ('5','13','5','12',62),
                ('5','13','5','13',99),
                ('5','14','4','10',-8),
                ('5','14','5','11',64),
                ('5','14','5','12',48),
                ('5','14','5','13',26),
                ('5','15','4','10',-5),
                ('5','15','5','11',60),
                ('5','15','5','12',28),
                ('5','15','5','13',16),
                ('5','16','4','10',-6),
                ('5','16','5','11',85),
                ('5','16','5','12',57),
                ('5','16','5','13',99),
                ('5','17','4','10',-3),
                ('5','17','5','11',68),
                ('5','17','5','12',32),
                ('5','17','5','13',91)
            ],
            columns=["s","r","s","t","value"]
            )

A=gt.Parameter(model_container,'A',[s,r,s,t])
A.setRecords(A_df_parameters)
    

def get_model_text():
    return '''
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
$load t r s MAPSP MAPSrow c b A k
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

    '''

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ws = GamsWorkspace(system_directory = sys.argv[1])
    else:
        ws = GamsWorkspace('.')

    #klist = [ 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3 ]
    klist = [ 1 ]
    iter_list = [1,2]
    s_list=[1,2,3,4,5]
    snt_list=['forward','backward']

    # create a new GAMSJob that is initialized from the GAMSCheckpoint

    #Z_inf = -math.inf
    #Z_sup = +math.inf

    Z_inf = -10
    Z_sup = +10
    TOL=0.001

    iter_list=range(1,3)

    for iter_python in iter_list:

        for snt_python in snt_list:

            for s_python in s_list:

                print("\n")
                print(f"*** iteracion: {iter_python} ***")
                print(f"****** sentido: {snt_python} ******")
                print(f"********* escenario: {s_python} *********")

                if iter_python==1 and snt_python=="forward" and s_python==1:

                    k_df_parameter=pd.DataFrame([(str(s_python))],columns=['k'])
                    k=gt.Parameter(model_container,'k')
                    k.setRecords(k_df_parameter)

                    transfer_model=ws.add_job_from_string(get_model_text())
                    opt=ws.add_options()
                    opt.defines["gdxincname"]="gtin.gdx"
                    opt.all_model_types="cplex"
                    opt.gdx="gtout.gdx"

                    model_container.write(os.path.join(ws.working_directory, opt.defines["gdxincname"]))

                    check_point = ws.add_checkpoint()

                    transfer_model.run(gams_options=opt,checkpoint=check_point)                    
                    
                    #transfer_model_out=gt.Container(os.path.join(ws.working_directory, opt.gdx))

                    transfer_model = ws.add_job_from_string("solve multibenders1 using LP minimizing Z;", checkpoint=check_point)

                    transfer_model.run(gams_options=opt,checkpoint=check_point)   

                    transfer_model_out=gt.Container(os.path.join(ws.working_directory, opt.gdx))

                    print("********************************************")
                    print("Scenario k=" + str(s_python) + ":")
                    print("********************************************")

                    #resultados de la simulacion en dataframes
                    job=pkg.export_df_api_python.create_inform_df(transfer_model)
                    dict_variable=job.print_get_varible('x')
                    dict_ecuacion=job.print_get_equation('eq_r1')
                    dict_fo=job.print_get_varible('Z')
                    job.print_get_equation('eq_z1') 

                    #crear el container
                    m_container = gt.Container()                      

                    #preparar la data para que pueda ser incluida en ek container
                    s_mapsp=[]
                    t_mapsp=[]

                    for m in list(transfer_model.out_db["MAPSP"]):
                        print(m.key(0)+"."+m.key(1))
                        if m.key(0)==str(s_python):
                            s_mapsp.append(str(m.key(0)))
                            t_mapsp.append(str(m.key(1)))

                    print(t_mapsp)

                    #preparar set para crear los paremetros x_kk(iter,s,t)
                    s_c=gt.Set(m_container,"s",records=[str(s_python)])
                    t_c=gt.Set(m_container,"t",records=t_mapsp)
                    iter_c=gt.Set(m_container,"iter",records=[str(iter_python)])

                    #preparar la data de los parametros x_kk(iter,s,t)
                    list_keys_0=[list(dict_variable['level'].keys())[i][0] for i in range(len(list(dict_variable['level'].keys())))]
                    list_keys_1=[list(dict_variable['level'].keys())[i][1] for i in range(len(list(dict_variable['level'].keys())))]
                    list_values=[list(dict_variable['level'].values())[i] for i in range(len(list(dict_variable['level'].keys())))]
                    list_iter=[str(iter_python)]*len(list_keys_0)
                    
                    array_xkk=list(zip(list_iter,list_keys_0,list_keys_1,list_values))

                    pd_xkk=pd.DataFrame(array_xkk,columns=["iter","s","t","Value"])

                    array_zkk=[(str(iter_python),str(dict_fo['level']))]  

                    pd_zkk=pd.DataFrame(array_zkk,columns=["iter","value"])
                    
                    #insertar data en el gdx a partir del container
                    x_kk=gt.Parameter(m_container,"x_kk",[iter_c,s_c,t_c])
                    x_kk.setRecords(pd_xkk)

                    z_kk=gt.Parameter(m_container,"z_kk",[iter_c])
                    z_kk.setRecords(pd_zkk)

                    del s_c, t_c, iter_c

                    #escribir el gdx
                    m_container.write("./transfer.gdx")

                elif iter_python==1 and snt_python=="forward" and (s_python>1 or s_python<max(s_list)):

                    iteracion=str(iter)
                    k=str(s)
                    print("gamssolve(multibenders2a)")
                    transfer_model = ws.add_job_from_string(gams_source="k=" + str(k) + ";"
                                                "iteracion="+str(iteracion) + ";"
                                                "solve multibenders2a using LP minimizing Z;", checkpoint=check_point)
                    
                    transfer_model.run(gams_options=opt,checkpoint=check_point)

                    
                    print("********************************************")
                    print("Scenario k=" + str(k) + ":")
                    print("********************************************")

                    #resultados de la simulacion en dataframes
                    job=pkg.export_df_api_python.create_inform_df(transfer_model)
                    dict_variable=job.print_get_varible('x')
                    dict_ecuacion=job.print_get_equation('eq_r1')
                    dict_fo=job.print_get_varible('Z')
                    job.print_get_equation('eq_z1') 

                    #crear el container
                    m_container = gt.Container()                      

                    #preparar la data para que pueda ser incluida en ek container
                    s_mapsp=[]
                    t_mapsp=[]

                    for m in list(transfer_model.out_db["MAPSP"]):
                        if m.key(0)==str(k):
                            s_mapsp.append(str(m.key(0)))
                            t_mapsp.append(str(m.key(1)))

                    #preparar set para crear los paremetros x_kk(iter,s,t)
                    s_c=gt.Set(m_container,"s",records=[str(k)])
                    t_c=gt.Set(m_container,"t",records=t_mapsp)
                    iter_c=gt.Set(m_container,"iter",records=[str(iteracion)])

                    #preparar la data de los parametros x_kk(iter,s,t)
                    list_keys_0=[list(dict_variable['level'].keys())[i][0] for i in range(len(list(dict_variable['level'].keys())))]
                    list_keys_1=[list(dict_variable['level'].keys())[i][1] for i in range(len(list(dict_variable['level'].keys())))]
                    list_values=[list(dict_variable['level'].values())[i] for i in range(len(list(dict_variable['level'].keys())))]
                    list_iter=[str(iteracion)]*len(list_keys_0)
                    
                    array_xkk=list(zip(list_iter,list_keys_0,list_keys_1,list_values))

                    pd_xkk=pd.DataFrame(array_xkk,columns=["iter","s","t","Value"])

                    array_zkk=[(str(iteracion),str(dict_fo['level']))]  

                    pd_zkk=pd.DataFrame(array_zkk,columns=["iter","value"])
                    
                    #insertar data en el gdx a partir del container
                    x_kk=gt.Parameter(m_container,"x_kk",[iter_c,s_c,t_c])
                    x_kk.setRecords(pd_xkk)

                    z_kk=gt.Parameter(m_container,"z_kk",[iter_c])
                    z_kk.setRecords(pd_zkk)

                    #escribir el gdx
                    m_container.write("./transfer.gdx")

                elif iter_python==1 and snt_python=="forward" and s_python==max(s_list):

                    k=s
                    m=s-1
                    print("gamssolve(multibenders2a)")
                    print("\n")
                    pass   

                elif iter_python>1 and snt_python=="forward" and s_python==1:
                          
                    k=s
                    print("gamssolve(multibenders3)")
                    print("\n")
                    pass

                elif iter_python>1 and snt_python=="forward" and (s_python>1 or s_python<max(s_list)):

                    k=s
                    print("gamssolve(multibenders2a)")
                    print("\n")
                    pass

                elif iter_python>1 and snt_python=="forward" and s_python==max(s_list):

                    k=s
                    m=s-1
                    print("gamssolve(multibenders2a)")
                    print("\n")
                    pass 

                elif iter_python>=1 and snt_python=="backward" and (s_python>1 and s_python<max(s_list)):

                    k=max(s_list)-s+1
                    dispb=max(s_list)-2*s+1

                    print("gamssolve(multibenders2a)")
                    print("\n")
                    pass