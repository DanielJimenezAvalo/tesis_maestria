from gams import GamsWorkspace
import os
import sys
from pprint import pprint

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
eq_r1(s,r)  ecuaciones
;

eq_z..          sum[(s,t),c(s,t)*x(s,t)]   =e= Z  ;

eq_r1(s,r)..    sum[(ss,t)$MAPSP(ss,t),A(s,r,ss,t)*x(ss,t)]=g= bmult*b(s,r) ;


model multibenders /all/

solve multibenders using LP minimizing Z;
  
    '''


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ws = GamsWorkspace(system_directory = sys.argv[1])
    else:
        ws = GamsWorkspace('.')
        
      
    #call of data and creation of gdx file
    t2 = ws.add_job_from_string(get_data_text())
    t2.run()
    #t5.out_db.export(os.path.join(ws.working_directory, "tdata.gdx"))
    t2.out_db.export("./tdata.gdx")
    #complete the model
    t2 = ws.add_job_from_string(get_model_text())
    #insert gdx file as an option
    opt = ws.add_options()
    opt.defines["gdxincname"] = "tdata.gdx"
    opt.all_model_types = "cplex"

    # initialize a GAMSCheckpoint by running a GAMSJob
    cp = ws.add_checkpoint()

    t2.run(gams_options=opt,checkpoint=cp)



    print('························')
    print("t2.out_db")
    print(t2.out_db,"\n",
          t2.out_db.__len__(),"\n",
          list(t2.out_db),"\n",
          list(t2.out_db).__len__(),"\n")
    
    print('························')
    print("t2.out_db.get_variable('x')")
    print(t2.out_db.get_variable('x'),"\n",
          t2.out_db.get_variable('x').__len__(),"\n",
          list(t2.out_db.get_variable('x')),"\n",
          list(t2.out_db.get_variable('x')).__len__(),"\n")
    
    array_column_variable=['level','marginal','upper','lower']
    dict_variables_values={}
    dict_variables_marginal={}
    dict_variables_upper={}
    for rec in list(t2.out_db.get_variable('x')):
        #print(type(rec))
        #print(type(rec.keys))
        #print(rec.keys)
        #print(len(rec.keys))
        
        dict_variables_values[tuple(rec.keys)]= str(rec.level)
        dict_variables_marginal[tuple(rec.keys)]= str(rec.marginal)
        dict_variables_upper[tuple(rec.keys)]=str(rec.upper)
    
    print(dict_variables_values)
    print(dict_variables_marginal)
    print(dict_variables_upper)

    print('························')
    print("t2.out_db.get_variable('Z')")
    print(t2.out_db.get_variable('Z'),"\n",
          t2.out_db.get_variable('Z').__len__(),"\n",
          list(t2.out_db.get_variable('Z')),"\n",
          list(t2.out_db.get_variable('Z')).__len__(),"\n")
    
    array_column_variable=['level','marginal','upper','lower']
    dict_variables_values={}
    dict_variables_marginal={}
    dict_variables_upper={}
    dict_variables_values['level']= str(t2.out_db.get_variable('Z').find_record().level)
    dict_variables_marginal['marginal']= str(t2.out_db.get_variable('Z').find_record().marginal)
    dict_variables_upper['lower']=str(t2.out_db.get_variable('Z').find_record().lower)
    
    print(dict_variables_values)
    print(dict_variables_marginal)
    print(dict_variables_upper)
    
    print('························')
    print("t2.out_db['x']")
    print(t2.out_db['x'],"\n",
          t2.out_db['x'].__len__(),"\n",
          list(t2.out_db['x']),"\n",
          list(t2.out_db['x']).__len__(),"\n")
    
    
    
    print('························')
    print("t2.out_db.get_equation('eq_r1')")
    print(t2.out_db.get_equation('eq_r1'),"\n",
          t2.out_db.get_equation('eq_r1').__len__(),"\n",
          list(t2.out_db.get_equation('eq_r1')),"\n",
          list(t2.out_db.get_equation('eq_r1')).__len__(),"\n")
    
    array_column_equation=['level','marginal','upper','lower']
    dict_equation_values={}
    dict_equation_marginal={}
    dict_equation_upper={}
    for rec in t2.out_db.get_equation('eq_r1'):
        dict_equation_values[rec.key(0)]= str(rec.level)
        dict_equation_marginal[rec.key(0)]= str(rec.marginal)
        dict_equation_upper[rec.key(0)]=str(rec.upper)
        
    print(dict_equation_values)
    print(dict_equation_marginal)
    print(dict_equation_upper)
    
    print('························')
    print("t2.out_db['eq_r1']")
    print(t2.out_db['eq_r1'],"\n",
          t2.out_db['eq_r1'].__len__(),"\n",
          list(t2.out_db['eq_r1']),"\n",
          list(t2.out_db['eq_r1']).__len__(),"\n")
    
    
    #print(list(t2.out_db['x']))
    #print(t2.out_db['x'].__len__())
    #print(str(t2.out_db['x']))
    
    
    #print(type(t2.out_db.get_variable('x')))
    #print(list(t2.out_db.get_variable('x')))
    
    #print(t2.out_db)
    #print(list(t2.out_db.get_set('i')))
    #print(list(t2.out_db.get_set('i'))[0].__str__())
    #print(t2.out_db.get_variable('x'))
    #print(type(list(t2.out_db.get_equation('eq_r1'))[1].__str__()))
    m=t2.out_db.get_equation('eq_r1').__dict__
    #print(m)
    m1=t2.out_db.get_equation('eq_z').__len__()
    #print(m1)
    
    r=t2.out_db.__dict__
    rr=r['_workspace'].__dict__
    rrr=rr['_gams_databases']
    #print(rrr)
    
    print(list(t2.out_db['x']))
    print(list(t2.out_db['x'])[1])
    
    print(type(list(t2.out_db.get_variable('x'))))
    print(type(list(t2.out_db.get_variable('x'))[1]))
    print(list(t2.out_db.get_variable('x'))[1])

    


    #for rec in t2.out_db["x"]:
    #    print("x(" + rec.key(0) + "): level=" + str(rec.level) + " marginal=" + str(rec.marginal))
    
