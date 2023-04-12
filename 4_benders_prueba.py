from gams import GamsWorkspace
import os
import sys
from pprint import pprint

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

eq_r1(m)..       sum[i, A(m,i)*x(i)] =g= B(m);


model multibenders /all/

solve multibenders using LP minimizing Z;
  
    '''


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ws = GamsWorkspace(system_directory = sys.argv[1])
    else:
        ws = GamsWorkspace('.')
        
    '''  
    plants   = [ "Seattle", "San-Diego" ]
    markets  = [ "New-York", "Chicago", "Topeka" ]
    capacity = { "Seattle": 350.0, "San-Diego": 600.0 } 
    demand   = { "New-York": 325.0, "Chicago": 300.0, "Topeka": 275.0 }
    distance = { ("Seattle",   "New-York") : 2.5,
                 ("Seattle",   "Chicago")  : 1.7,
                 ("Seattle",   "Topeka")   : 1.8,
                 ("San-Diego", "New-York") : 2.5,
                 ("San-Diego", "Chicago")  : 1.8,
                 ("San-Diego", "Topeka")   : 1.4
               }
    '''
    i_p=['i1','i2','i3','i4','i5','i6','i7','i8','i9','i10','i11','i12','i13']
    m_p=['m1','m2','m3','m4','m5','m6','m7','m8','m9','m10','m11','m12','m13','m14','m15','m16','m17']
    
    C_p = {
    'i1':     184,
    'i2':     642,
    'i3':     312,
    'i4':     304,
    'i5':     472,
    'i6':     305,
    'i7':     531,
    'i8':     805,
    'i9':     516,
    'i10':      344,
    'i11':      740,
    'i12':      764,
    'i13':      386
    }
    
    B_p = {
    'm1':        2105,
    'm2':        2453,
    'm3':        4916,
    'm4':        2564,
    'm5':        1969,
    'm6':        1060,
    'm7':        3951,
    'm8':        1383,
    'm9':        2783,
    'm10':        2667,
    'm11':        3791,
    'm12':        1039,
    'm13':        4756,
    'm14':        2782,
    'm15':        2725,
    'm16':        3235,
    'm17':        3436
    }
        
    A_p = {
    ('m1','i1'):	28,
    ('m2','i1'):	18,
    ('m3','i1'):	-4,
    ('m4','i1'):	-1,
    ('m5','i1'):	-7,
    ('m6','i1'):	-2,
    ('m7','i1'):	0,
    ('m8','i1'):	0,
    ('m9','i1'):	0,
    ('m10','i1'):	0,
    ('m11','i1'):	0,
    ('m12','i1'):	0,
    ('m13','i1'):	0,
    ('m14','i1'):	0,
    ('m15','i1'):	0,
    ('m16','i1'):	0,
    ('m17','i1'):	0,
    ('m1','i2'):	38,
    ('m2','i2'):	82,
    ('m3','i2'):	-2,
    ('m4','i2'):	-2,
    ('m5','i2'):	-4,
    ('m6','i2'):	-3,
    ('m7','i2'):	0,
    ('m8','i2'):	0,
    ('m9','i2'):	0,
    ('m10','i2'):	0,
    ('m11','i2'):	0,
    ('m12','i2'):	0,
    ('m13','i2'):	0,
    ('m14','i2'):	0,
    ('m15','i2'):	0,
    ('m16','i2'):	0,
    ('m17','i2'):	0,
    ('m1','i3'):	12,
    ('m2','i3'):	15,
    ('m3','i3'):	-6,
    ('m4','i3'):	-5,
    ('m5','i3'):	-4,
    ('m6','i3'):	-1,
    ('m7','i3'):	0,
    ('m8','i3'):	0,
    ('m9','i3'):	0,
    ('m10','i3'):	0,
    ('m11','i3'):	0,
    ('m12','i3'):	0,
    ('m13','i3'):	0,
    ('m14','i3'):	0,
    ('m15','i3'):	0,
    ('m16','i3'):	0,
    ('m17','i3'):	0,
    ('m1','i4'):	0,
    ('m2','i4'):	0,
    ('m3','i4'):	61,
    ('m4','i4'):	30,
    ('m5','i4'):	50,
    ('m6','i4'):	92,
    ('m7','i4'):	-9,
    ('m8','i4'):	-8,
    ('m9','i4'):	-7,
    ('m10','i4'):	0,
    ('m11','i4'):	0,
    ('m12','i4'):	0,
    ('m13','i4'):	0,
    ('m14','i4'):	0,
    ('m15','i4'):	0,
    ('m16','i4'):	0,
    ('m17','i4'):	0,
    ('m1','i5'):	0,
    ('m2','i5'):	0,
    ('m3','i5'):	74,
    ('m4','i5'):	40,
    ('m5','i5'):	95,
    ('m6','i5'):	70,
    ('m7','i5'):	-7,
    ('m8','i5'):	-9,
    ('m9','i5'):	-7,
    ('m10','i5'):	0,
    ('m11','i5'):	0,
    ('m12','i5'):	0,
    ('m13','i5'):	0,
    ('m14','i5'):	0,
    ('m15','i5'):	0,
    ('m16','i5'):	0,
    ('m17','i5'):	0,
    ('m1','i6'):	0,
    ('m2','i6'):	0,
    ('m3','i6'):	0,
    ('m4','i6'):	0,
    ('m5','i6'):	0,
    ('m6','i6'):	0,
    ('m7','i6'):	88,
    ('m8','i6'):	81,
    ('m9','i6'):	55,
    ('m10','i6'):	-8,
    ('m11','i6'):	-4,
    ('m12','i6'):	-9,
    ('m13','i6'):	0,
    ('m14','i6'):	0,
    ('m15','i6'):	0,
    ('m16','i6'):	0,
    ('m17','i6'):	0,
    ('m1','i7'):	0,
    ('m2','i7'):	0,
    ('m3','i7'):	0,
    ('m4','i7'):	0,
    ('m5','i7'):	0,
    ('m6','i7'):	0,
    ('m7','i7'):	48,
    ('m8','i7'):	19,
    ('m9','i7'):	26,
    ('m10','i7'):	-7,
    ('m11','i7'):	-4,
    ('m12','i7'):	-6,
    ('m13','i7'):	0,
    ('m14','i7'):	0,
    ('m15','i7'):	0,
    ('m16','i7'):	0,
    ('m17','i7'):	0,
    ('m1','i8'):	0,
    ('m2','i8'):	0,
    ('m3','i8'):	0,
    ('m4','i8'):	0,
    ('m5','i8'):	0,
    ('m6','i8'):	0,
    ('m7','i8'):	26,
    ('m8','i8'):	95,
    ('m9','i8'):	51,
    ('m10','i8'):	-6,
    ('m11','i8'):	-7,
    ('m12','i8'):	-6,
    ('m13','i8'):	0,
    ('m14','i8'):	0,
    ('m15','i8'):	0,
    ('m16','i8'):	0,
    ('m17','i8'):	0,
    ('m1','i9'):	0,
    ('m2','i9'):	0,
    ('m3','i9'):	0,
    ('m4','i9'):	0,
    ('m5','i9'):	0,
    ('m6','i9'):	0,
    ('m7','i9'):	21,
    ('m8','i9'):	70,
    ('m9','i9'):	24,
    ('m10','i9'):	-1,
    ('m11','i9'):	-3,
    ('m12','i9'):	-8,
    ('m13','i9'):	0,
    ('m14','i9'):	0,
    ('m15','i9'):	0,
    ('m16','i9'):	0,
    ('m17','i9'):	0,
    ('m1','i10'):	0,
    ('m2','i10'):	0,
    ('m3','i10'):	0,
    ('m4','i10'):	0,
    ('m5','i10'):	0,
    ('m6','i10'):	0,
    ('m7','i10'):	0,
    ('m8','i10'):	0,
    ('m9','i10'):	0,
    ('m10','i10'):	24,
    ('m11','i10'):	32,
    ('m12','i10'):	70,
    ('m13','i10'):	-3,
    ('m14','i10'):	-8,
    ('m15','i10'):	-5,
    ('m16','i10'):	-6,
    ('m17','i10'):	-3,
    ('m1','i11'):	0,
    ('m2','i11'):	0,
    ('m3','i11'):	0,
    ('m4','i11'):	0,
    ('m5','i11'):	0,
    ('m6','i11'):	0,
    ('m7','i11'):	0,
    ('m8','i11'):	0,
    ('m9','i11'):	0,
    ('m10','i11'):	0,
    ('m11','i11'):	0,
    ('m12','i11'):	0,
    ('m13','i11'):	69,
    ('m14','i11'):	64,
    ('m15','i11'):	60,
    ('m16','i11'):	85,
    ('m17','i11'):	68,
    ('m1','i12'):	0,
    ('m2','i12'):	0,
    ('m3','i12'):	0,
    ('m4','i12'):	0,
    ('m5','i12'):	0,
    ('m6','i12'):	0,
    ('m7','i12'):	0,
    ('m8','i12'):	0,
    ('m9','i12'):	0,
    ('m10','i12'):	0,
    ('m11','i12'):	0,
    ('m12','i12'):	0,
    ('m13','i12'):	62,
    ('m14','i12'):	48,
    ('m15','i12'):	28,
    ('m16','i12'):	57,
    ('m17','i12'):	32,
    ('m1','i13'):	0,
    ('m2','i13'):	0,
    ('m3','i13'):	0,
    ('m4','i13'):	0,
    ('m5','i13'):	0,
    ('m6','i13'):	0,
    ('m7','i13'):	0,
    ('m8','i13'):	0,
    ('m9','i13'):	0,
    ('m10','i13'):	0,
    ('m11','i13'):	0,
    ('m12','i13'):	0,
    ('m13','i13'):	99,
    ('m14','i13'):	26,
    ('m15','i13'):	16,
    ('m16','i13'):	99,
    ('m17','i13'):	91
    }
    
    
    
    db = ws.add_database()

    i = db.add_set("i", 1, "variable master")
    for p in i_p:
        i.add_record(p)
    
    m = db.add_set("m", 1, "restricciones")
    for p in m_p:
        m.add_record(p)
        
    C = db.add_parameter_dc("C", [i], "capacity of plant i in cases")
    for p in i_p:
        C.add_record(p).value = C[p]

    B = db.add_parameter_dc("B", [m], "demand at market j in cases")
    for p in m_p:
        B.add_record(p).value = B[p]
    
    A = db.add_parameter_dc("A", [i,m], "distance in thousands of miles")
    for p, q in iter(A_p.items()):
        A.add_record(q).value = p
    '''
    f = db.add_parameter("f", 0, "freight in dollars per case per thousand miles")
    f.add_record().value = 90
    '''
    t4 = ws.add_job_from_string(get_model_text())
    opt = ws.add_options()
    
    opt.defines["gdxincname"] = db.name
    opt.all_model_types = "cplex"

    t4.run(opt, databases = db)
    for rec in t4.out_db["x"]:
        print("x(" + rec.key(0) + "," + rec.key(1) + "): level=" + str(rec.level) + " marginal=" + str(rec.marginal))
    
