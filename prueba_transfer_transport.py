'''
@file
In this tutorial example we show how GAMS Transfer and the OO API can work together. 
Essentially, the Transfer Container takes on the role of GAMSDatabase. This example
combines elements from transport4.py and transport7.py.
'''

from gams import GamsWorkspace, GamsModifier, UpdateAction, VarType
import gams.transfer as gt
import numpy as np
import sys
import os


def get_model_text():
    return '''
Sets
     i   "canning plants"
     j   "markets"

Parameters
     a(i)   "capacity of plant i in cases"
     b(j)   "demand at market j in cases"
     d(i,j) "distance in thousands of miles"
Scalar f  "freight in dollars per case per thousand miles";

$if not set gdxincname $abort "no include file name for data file provided"
$gdxin %gdxincname%
$load i j a b d f
$gdxin

Parameter c(i,j) "transport cost in thousands of dollars per case";
c(i,j) = f * d(i,j) / 1000;

Variables
     x(i,j)  "shipment quantities in cases"
     z       "total transportation costs in thousands of dollars";

Positive Variable x;

Equations
     cost        "define objective function"
     supply(i)   "observe supply limit at plant i"
     demand(j)   "satisfy demand at market j";

Scalar 
     bmult       "demand multiplier" /1/;
     
cost ..        z  =e=  sum((i,j), c(i,j)*x(i,j));

supply(i) ..   sum(j, x(i,j))  =l=  a(i);

demand(j) ..   sum(i, x(i,j))  =g=  bmult*b(j);

Model transport /all/;

Solve transport using lp minimizing z;'''

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ws = GamsWorkspace(system_directory = sys.argv[1])
    else:
        ws = GamsWorkspace(working_directory='.')

    #create the container    
    m = gt.Container()

    #create data from adding thoughout the container functions
    i = m.addSet('i', records=[ "Seattle", "San-Diego" ])
    j = m.addSet('j', records=[ "New-York", "Chicago", "Topeka" ])
    m.addParameter('a', [i], records=np.array([350, 600]))
    m.addParameter('b', [j], records=np.array([325, 300, 275]))
    m.addParameter('d', [i,j], records=np.array([[2.5, 1.7, 1.8],
                                                 [2.5, 1.8, 1.4]]))
    m.addParameter('f', records=90)

    tm = ws.add_job_from_string(get_model_text())  #get model from string above
    opt = ws.add_options()  #create a worspace options
    opt.defines["gdxincname"] = "gtin.gdx"  #gdxincname 
    opt.all_model_types = "xpress"
    opt.gdx = "gtout.gdx"

    m.write(os.path.join(ws.working_directory, opt.defines["gdxincname"])) #create a gdx file with name  "gtin.gdx"
    cp = ws.add_checkpoint() #checkpoint for included a gdx file above
    tm.run(gams_options=opt, checkpoint=cp, create_out_db=False) #run the model and solve it
    tmOut = gt.Container(os.path.join(ws.working_directory, opt.gdx)) #create a container "gtout.gdx"
    
    # create a GAMSModelInstance and solve it multiple times with different scalar bmult
    mi = cp.add_modelinstance() #create a instance of checkpoint 
    bmult = mi.sync_db.add_parameter("bmult", 0, "demand multiplier") #add parameter from instance of checkpoint
    opt = ws.add_options() #create option of workspaces
    opt.all_model_types = "cplex" #option solver

    # instantiate the GAMSModelInstance and pass a model definition and GAMSModifier to declare bmult mutable
    mi.instantiate("transport use lp min z", GamsModifier(bmult), opt) #instantiate the checkpoint instance using a modifier and the new options

    bmult.add_record().value = 1.0
    bmultlist = [ 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3 ]

    m = gt.Container()
    gt_bmult = m.addParameter('bmult', records=1.0);
    for b in bmultlist:
        gt_bmult.setRecords(b)
        m.write(mi.sync_db)
        mi.solve()
        mOut = gt.Container(mi.sync_db)
        print("Scenario bmult=" + str(b) + ":")
        print("  Modelstatus: " + str(mi.model_status))
        print("  Solvestatus: " + str(mi.solver_status))
        print("  Obj: " + str(mOut.data['z'].records['level'].iloc[0]))

    # create a GAMSModelInstance and solve it with single links in the network blocked
    mi = cp.add_modelinstance()
    x = mi.sync_db.add_variable("x", 2, VarType.Positive)
    xup = mi.sync_db.add_parameter("xup", 2, "upper bound on x")
    
    # instantiate the GAMSModelInstance and pass a model definition and GAMSModifier to declare upper bound of X mutable
    mi.instantiate("transport use lp min z", GamsModifier(x, UpdateAction.Upper, xup))
    mi.solve()
    
    m = gt.Container()
    gt_xup = m.addParameter('xup', ['i','j']);
    for i in tmOut.data['i'].records['i_0']:
        for j in tmOut.data['j'].records['j_0']:
            gt_xup.setRecords([(i,j,-0.0)]) # -0.0 turns the 0 into an EPS
            m.write(mi.sync_db)
            mi.solve()
            mOut = gt.Container(mi.sync_db)
            print("Scenario link blocked: " + i + " - " + j)
            print("  Modelstatus: " + str(mi.model_status))
            print("  Solvestatus: " + str(mi.solver_status))
            print("  Obj: " + str(mOut.data['z'].records['level'].iloc[0]))
