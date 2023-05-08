from gams import GamsWorkspace
import os
import sys
import pkg
import threading

def get_data_text():
    return '''
    sets
    i        variables master        /i1*i13/
    m        restricciones           /m1*m17/
    ;

    parameters
    C(i)     coeficientes FO   /
    i1        184
    i2        642
    i3        312
    i4        304
    i5        472
    i6        305
    i7        531
    i8        805
    i9        516
    i10        344
    i11        740
    i12        764
    i13        386
    /


    B(m)     cotas restricciones
    /
    m1        2105
    m2        2453
    m3        4916
    m4        2564
    m5        1969
    m6        1060
    m7        3951
    m8        1383
    m9        2783
    m10        2667
    m11        3791
    m12        1039
    m13        4756
    m14        2782
    m15        2725
    m16        3235
    m17        3436
    /

    ;
    table A(m,i)     coeficientes restricciones master
               i1        i2        i3        i4        i5        i6        i7        i8        i9       i10       i11       i12       i13
     m1        28        38        12         0         0         0         0         0         0         0         0         0         0
     m2        18        82        15         0         0         0         0         0         0         0         0         0         0
     m3        -4        -2        -6        61        74         0         0         0         0         0         0         0         0
     m4        -1        -2        -5        30        40         0         0         0         0         0         0         0         0
     m5        -7        -4        -4        50        95         0         0         0         0         0         0         0         0
     m6        -2        -3        -1        92        70         0         0         0         0         0         0         0         0
     m7         0         0         0        -9        -7        88        48        26        21         0         0         0         0
     m8         0         0         0        -8        -9        81        19        95        70         0         0         0         0
     m9         0         0         0        -7        -7        55        26        51        24         0         0         0         0
    m10         0         0         0         0         0        -8        -7        -6        -1        24         0         0         0
    m11         0         0         0         0         0        -4        -4        -7        -3        32         0         0         0
    m12         0         0         0         0         0        -9        -6        -6        -8        70         0         0         0
    m13         0         0         0         0         0         0         0         0         0        -3        69        62        99
    m14         0         0         0         0         0         0         0         0         0        -8        64        48        26
    m15         0         0         0         0         0         0         0         0         0        -5        60        28        16
    m16         0         0         0         0         0         0         0         0         0        -6        85        57        99
    m17         0         0         0         0         0         0         0         0         0        -3        68        32        91

    ;  

    '''
    

def get_model_text():
    return '''
sets
    i        variables master       
    m        restricciones           
    ;

    parameters
    C(i)     coeficientes FO 
    B(m)     cotas restricciones
    A(m,i)    coeficientes restricciones master    
    ;

Scalar bmult  demand multiplier /1/;  

$if not set gdxincname $abort 'no include file name for data file provided'
$gdxin %gdxincname%
$load i m C B A
$gdxin

positive variables
x(i)     variables
;

variables
Z      FO
;

equations
eq_z      funcion objetivo master
eq_r1(m)  ecuaciones
;

eq_z..           sum[i, c(i)*x(i)]   =e= Z  ;

eq_r1(m)..       sum[i, A(m,i)*x(i)] =g= bmult*B(m);


model multibenders /all/

    '''

def run_scenario(workspace, checkpoint, io_lock, bhombre):
    t6 = workspace.add_job_from_string("bmult=" + str(b) + "; solve multibenders using LP minimizing Z;", checkpoint)
    t6.run()
    #t6.run(gams_options=opt,checkpoint=cp)
    io_lock.acquire() #function of class threads
    print("*****************************************************")
    print("Scenario bmult=" + str(b) + ":")
    print("*****************************************************")

    job=pkg.export_df_api_python.create_inform_df(t6)
    job.print_get_varible('x')
    job.print_get_equation('eq_r1')
    job.print_get_varible('Z')
    job.print_get_equation('eq_z')  
    print("\n")

    io_lock.release() #function of class threads


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ws = GamsWorkspace(system_directory = sys.argv[1])
    else:
        ws = GamsWorkspace('.')

    
    #call of data and creation of gdx file
    t6 = ws.add_job_from_string(get_data_text())
    t6.run()
    t6.out_db.export(os.path.join(ws.working_directory, "tdata.gdx"))
    #complete the model
    t6 = ws.add_job_from_string(get_model_text())
    #insert gdx file as an option
    opt = ws.add_options()
    opt.defines["gdxincname"] = "tdata.gdx"
    opt.all_model_types = "cplex"

    # initialize a GAMSCheckpoint by running a GAMSJob
    cp = ws.add_checkpoint()

    t6.run(gams_options=opt,checkpoint=cp)

    bmultlist = [ 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3 ]

    #bmultlist = [ 0.6, 0.7]

    # run multiple parallel jobs using the created GAMSCheckpoint
    io_lock  = threading.Lock()
    threads = {}
    for b in bmultlist:
        threads[b] = threading.Thread(target=run_scenario, args=(ws, cp, io_lock, b))
        threads[b].start()
    for b in bmultlist:
        threads[b].join()
              