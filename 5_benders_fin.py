from gams import GamsWorkspace
import os
import sys
import pkg

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
    t5 = ws.add_job_from_string(get_data_text())
    t5.run()
    #t5.out_db.export(os.path.join(ws.working_directory, "tdata.gdx"))
        
    #complete the model
    t5 = ws.add_job_from_string(get_model_text())
    #insert gdx file as an option
    opt = ws.add_options()
    opt.defines["gdxincname"] = "tdata.gdx"
    opt.all_model_types = "cplex"

    # initialize a GAMSCheckpoint by running a GAMSJob
    cp = ws.add_checkpoint()

    t5.run(gams_options=opt,checkpoint=cp)

    #bmultlist = [ 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3 ]
    bmultlist = [ 0.8, 1.0, 1.2]

    # create a new GAMSJob that is initialized from the GAMSCheckpoint
    for b in bmultlist:
        t5 = ws.add_job_from_string(gams_source="bmult=" + str(b) + "; solve multibenders using LP minimizing Z;", checkpoint=cp)
        t5.run(gams_options=opt)
        #t5.run(gams_options=opt,checkpoint=cp)
        print("********************************************")
        print("Scenario bmult=" + str(b) + ":")
        print("********************************************")

        job=pkg.export_df_api_python.create_inform_df(t5)
        job.print_get_varible('x')
        job.print_get_equation('eq_rk')
        job.print_get_varible('Z')
        job.print_get_equation('eq_z')   
        print("\n") 