# Import
from runFAST_v8 import runFAST_v8
from runTurbSim import runTurbSim


def callturbsim(mean_wind_speed, turbulence_intensity):

    ts = runTurbSim()
    ts.ts_exe = "/home/sebasanper/Downloads/turbsim/turbsim/TurbSim"

    # abs path
    ts.ts_dir = "/home/sebasanper/PycharmProjects/owf_MDAO/aero_loads_models/"
    ts.ts_file = "TurbSim.inp"

    # relative path
    #    ts.ts_dir = "TurbSimTest"
    #    ts.ts_file = "turbsim_template.inp"

    ts.run_dir = "/home/sebasanper/PycharmProjects/owf_MDAO/aero_loads_models/turbsim_test_run"
    ts.set_dict({"URef": mean_wind_speed, "AnalysisTime": 600, "UsableTime": 100, "IECturbc": turbulence_intensity})
    ts.execute()

    with open('/home/sebasanper/PycharmProjects/owf_MDAO/aero_loads_models/turbsim_test_run/TurbSim.sum', 'r') as files:
        filedata = files.read()

    # Replace the target string
    filedata = filedata.replace('87.700', '87.600')

    # Write the file out again
    with open('/home/sebasanper/PycharmProjects/owf_MDAO/aero_loads_models/turbsim_test_run/TurbSim.sum', 'w') as files:
        files.write(filedata)


def callfast():
    print 'Executing FAST using pure Python wrapper'
    print ''

    # Initialize FAST instance
    fstInst = runFAST_v8()

    # Define various members of the FAST instance. Can use relative locations.
    fstInst.fst_exe = "/home/sebasanper/PycharmProjects/owf_MDAO/aero_loads_models/bin/FAST_glin64"
    fstInst.fst_dir = "input_FAST"
    fstInst.fst_file = "Test19.fst"
    fstInst.run_dir = "FAST_run"
    fstInst.fst_file_type = 2  # specifies v8.15
    fstInst.fst_exe_type = 2  # specifies v8.15

    # Define inputs (could be FAST, ElastoDyn, or AeroDyn inputs)
    fstInst.fstDict['TMax'] = 100  # changed from 60
    # fstInst.fstDict['BlPitch(1)'] = 0
    # fstInst.fstDict['BlPitch(2)'] = 0
    # fstInst.fstDict['BlPitch(3)'] = 0
    # fstInst.fstDict['RotSpeed'] = 10.0  # change initial rotational speed

    # Define outputs (currently just FST outputs, others have to be changed in template input files)
    # fstInst.setOutputs(['Azimuth', 'RootMyb1'])

    # Execute FAST
    fstInst.execute()

    # Give some output to command line
    time = list(fstInst.getOutputValue("Time"))
    wave = list(fstInst.getOutputValue("Wave1Elev"))
    loads1 = list(fstInst.getOutputValue("HydroFxi"))
    loads2 = list(fstInst.getOutputValue("M1N1MKxe"))
    loads3 = list(fstInst.getOutputValue("HydroMxi"))
    loads4 = list(fstInst.getOutputValue("HydroMyi"))

    return time, wave, loads1, loads2, loads3, loads4

if __name__ == '__main__':

    # for ws in range(16, 20):
    #     for turb in range(1, 16):
    #         name = 'root_moment_w' + str(ws) + '_ti' + str(turb) + '.dat'
    #         callturbsim(ws, turb)
    #         a, b, c, d, e = callfast()
    #         with open(name, "w") as out:
    #             for i in range(len(a)):
    #                 out.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(a[i], b[i], c[i], d[i], e[i]))
    callturbsim(8.5, 8.0)

    a, b, c, d, e, f = callfast()
    for i in range(len(a)):
        print a[i], b[i], c[i], d[i], e[i], f[i]

    # from joblib import Parallel, delayed
    #
    # def analysis(ws, turb):
    #     name = 'root_moment_w' + str(ws) + '_ti' + str(turb) + '.dat'
    #     callturbsim(ws, turb)
    #     a, b, c, d, e = callfast()
    #     with open(name, "w") as out:
    #         for i in range(len(a)):
    #             out.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(a[i], b[i], c[i], d[i], e[i]))
    #
    # for ws in range(16, 20):
    #     Parallel(n_jobs=-1)(delayed(analysis)(ws, turb) for turb in range(1, 16))
