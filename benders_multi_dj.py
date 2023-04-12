
import pkg

if __name__ == "__main__":
    
    data_final = pkg.pd.read_csv('rutas.csv')
    array_input_dir = pkg.np.array(data_final['input_dir'])
    array_input_name = pkg.np.array(data_final['input_name'])
    array_output_dir = pkg.np.array(data_final['output_dir'])
    array_output_name = pkg.np.array(data_final['output_name'])
       
    for input_dir,input_name,output_dir,output_name in list(zip(array_input_dir,array_input_name,array_output_dir,array_output_name)):
        job_final=pkg.ClassGamsRun.GamsRunFromQuipu(input_dir,input_name,output_dir,output_name,'.','benders_multi_0_0.gms')
        job_final.execute_gams_gms()
        job_final.execute_csv_gams_output()
        gdx_name='gdx_'+output_name+'.gdx'
        pkg.shutil.copyfile('data_final.gdx',gdx_name)
    
    