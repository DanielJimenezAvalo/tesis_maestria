import os
import sys
import shutil
import time
from gams import GamsWorkspace

class GamsRunFromQuipu():

    def __init__(self,
                 input_dir,
                 input_name,
                 output_dir,
                 output_name,
                 gams_workspace,
                 gamsfile_gms):

        self.input_dir=input_dir
        self.input_name=input_name
        self.output_dir=output_dir
        self.output_name=output_name
        self.gams_workspace=gams_workspace
        self.gamsfile_gms=gamsfile_gms
    
    def execute_gams_gms(self):

        inicio = time.time()
        print(f'ejecucion archivo {self.input_name}')

        copy_input_dir=self.gams_workspace
        copy_input_name='input.DAT'
        copy_input_f = copy_input_dir + '/' + copy_input_name

        input_f = self.input_dir + '/' + self.input_name
        
        shutil.copyfile(input_f,copy_input_f)

        if len(sys.argv) > 1:
            ws = GamsWorkspace(system_directory = sys.argv[1])
        else:
            ws = GamsWorkspace(self.gams_workspace)

        t1 = ws.add_job_from_file(self.gamsfile_gms)
        t1.run()
        fin = time.time()
        
        os.remove(copy_input_f)
        
        return print(f'ejecucion finalizada {self.output_name} en {fin-inicio} segundos \n')
        
    def execute_csv_gams_output(self):

        gams_output_dir=self.gams_workspace
        gams_output_name='salida.put'
        gams_output_f = gams_output_dir + '/' + gams_output_name

        output_f = self.output_dir + '/' + self.output_name

        shutil.copyfile(gams_output_f,output_f)

        os.remove(gams_output_f)
        

        