from gams import GamsWorkspace, GamsModifier, UpdateAction, VarType
import os
import sys
import pkg
import threading

def get_data_text():
    return '''
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
    

def get_model_text():
    return '''
sets
t        periodos   
r        rows       
s        stages     

MAPSP(s,t)
MAPSrow(s,r)

;

alias(s,ss);

parameters
c(s,t)     coeficientes FO 
b(s,r)     cotas restricciones
A(s,r,s,t)    coeficientes restricciones master    
;

Scalar bmult  demand multiplier /1/;  

$if not set gdxincname $abort 'no include file name for data file provided'
$gdxin %gdxincname%
$load t r s MAPSP MAPSrow c b A
$gdxin

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

eq_rk(s,r)..    sum[(ss,t)$MAPSP(ss,t),A(s,r,ss,t)*x(ss,t)]=g= bmult*b(s,r) ;


model multibenders /all/

    '''

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ws = GamsWorkspace(system_directory = sys.argv[1])
    else:
        ws = GamsWorkspace('.')

    
    #call of data and creation of gdx file
    t7 = ws.add_job_from_string(get_data_text())
    t7.run()
    t7.out_db.export("./tdata.gdx")
    #complete the model
    t7 = ws.add_job_from_string(get_model_text())
    #insert gdx file as an option
    opt = ws.add_options()
    opt.defines["gdxincname"] = "tdata.gdx"
    opt.all_model_types = "cplex"

    # initialize a GAMSCheckpoint by running a GAMSJob
    cp = ws.add_checkpoint()

    t7.run(gams_options=opt,checkpoint=cp)


    #create a GAMSModelInstance and solve it multiple times with different scalar bmult
    mi=cp.add_modelinstance()
    bmult=mi.sync_db.add_parameter("bmult",0,"demand multiplier")
    opt=ws.add_options()
    opt.all_model_types = "cplex"

    #instantiate the GAMSModelInstance and pass a model definition and GAMSModifier to declare bmult mutable
    mi.instantiate("multibenders use lp minimizing Z", GamsModifier(bmult), opt)

    bmult.add_record().value=1
    bmultlist = [ 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3 ]
    #bmultlist = [ 0.6, 0.7]

    # create a new GAMSJob that is initialized from the GAMSCheckpoint
    for b in bmultlist:
        bmult.first_record().value=b
        mi.solve()
        #t7 = ws.add_job_from_string(gams_source="bmult=" + str(b) + "; solve multibenders using LP minimizing Z;", checkpoint=cp)
        #t7.run(gams_options=opt)
        #t7.run(gams_options=opt,checkpoint=cp)
        print("********************************************")
        print("Scenario bmult=" + str(b) + ":")
        print("********************************************")

        print("obj: "+str(mi.sync_db.get_variable("Z").find_record().level)) 
        print("\n") 


    #create a GAMSModelInstance and solve it with single links in the network blocked
    
    mi=cp.add_modelinstance()

    x=mi.sync_db.add_variable(identifier="x",
                              dimension=2,
                              vartype=VarType.Positive)
    
    xup=mi.sync_db.add_parameter(identifier="xup",
                                 dimension=2,
                                 explanatory_text="upper bound on x")

    #instantiate the GAMSModelInstance and pass a model definition and GAMSModifier to declare upper bound of X mutable
    mi.instantiate("multibenders use lp min z", GamsModifier(x,UpdateAction.Upper,xup))
    mi.solve()

    s_mapsp=[]
    t_mapsp=[]
    for m in t7.out_db["MAPSP"]:
        s_mapsp.append(m.key(0))
        t_mapsp.append(m.key(1))

    for s,t in list(zip(s_mapsp,t_mapsp)):
        xup.clear()
        xup.add_record((s,t)).value=0
        mi.solve()
        print("********************************************")
        print("Scenario x("+ s + "," + t+")=0")
        print("********************************************")

        #print("obj: "+str(mi.sync_db["Z"].find_record().level)) 
        print("obj: "+str(mi.sync_db.get_variable("Z").find_record().level)) 

        #t5.run(gams_options=opt,checkpoint=cp)
        print("********************************************")
        
        #for rec in mi.sync_db.get_variable('x'):
        #    print(rec.level)

        dict_output={}
        for criteria in ['level','marginal','upper','lower']:
            dict_output[criteria]={}
            for rec in mi.sync_db.get_variable('x'):
                match criteria:
                    case 'level':
                        dict_output[criteria][tuple(rec.keys)]= str(rec.level)
                    case 'marginal':
                        dict_output[criteria][tuple(rec.keys)]= str(rec.marginal)
                    case 'upper':
                        dict_output[criteria][tuple(rec.keys)]= str(rec.upper)
                    case 'lower':
                        dict_output[criteria][tuple(rec.keys)]= str(rec.lower)
        print(dict_output)    
        print("\n")         