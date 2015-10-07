""" Functions used for sensitivity analysis of septoria model
"""
from disease_sensi_morris import *
from alinea.alep.disease_outputs import AdelSeptoRecorder
from sensi_septo_tools import variety_code
from alinea.alep.simulation_tools.brown_rust_decomposed import annual_loop_rust
import numpy as np
import pandas as pd

def get_stored_rec(variety, year, i_sample, i_boot):
    return './brown_rust/'+variety.lower()+'_'+ str(year)+ \
            '_'+str(int(i_sample))+'_boot'+str(int(i_boot))+'.csv'
            
def run_brown_rust(sample):
    i_sample = sample.pop('i_sample')
    print '------------------------------'
    print 'i_sample %d' %i_sample
    print '------------------------------'
    i_boot = sample.pop('i_boot')
    year = sample.pop('year')
    variety = sample.pop('variety')
    sowing_date = '10-15'
    if year == 2012:
        sowing_date = '10-21'
    elif year == 2013:
        sowing_date = '10-29'
    output_file = get_stored_rec(variety, year, i_sample, i_boot)
    annual_loop_rust(year = year, variety = variety, sowing_date=sowing_date,
                    nplants = 5, output_file = output_file, **kwds)

def get_rust_morris_path(year = 2012, variety = 'Tremie12', nboots = 5):
    return './brown_rust/rust_morris_output_'+variety.lower()+'_'+str(year)+'.csv'
                    
def save_sensitivity_outputs(year = 2012, variety = 'Tremie12',
                             parameter_range_file = 'rust_param_range.txt',
                             input_file = './brown_rust/rust_morris_input_full.txt',
                             nboots = 5):
    parameter_names = pd.read_csv(parameter_range_file, header=None, sep = ' ')[0].values.tolist()
    list_param_names = ['i_sample', 'i_boot', 'year', 'variety'] + parameter_names
    for boot in range(nboots):
        input_boot = input_file[:-9]+'_boot'+str(boot)+input_file[-9:]
        df_in = pd.read_csv(input_boot, sep=' ',
                            index_col=0, names=list_param_names)
        vc = variety_code()
        df_in = df_in[(df_in['year']==year) & (df_in['variety']==vc[variety])]
        i_samples = df_in.index
        df_out = pd.DataFrame(columns = ['num_leaf_top'] + list(df_in.columns) + ['normalized_audpc'])
        for i_sample in i_samples:
            stored_rec = get_stored_rec(variety, year, i_sample, boot)
            df_reco = pd.read_csv(stored_rec)
            for lf in np.unique(df_reco['num_leaf_top']):
                df_reco_lf = df_reco[(df_reco['num_leaf_top']==lf)]
                output = {}
                output['num_leaf_top'] = lf
                for col in df_in.columns:
                    output[col] = df_in.loc[i_sample, col]
                output['normalized_audpc'] = df_reco_lf.normalized_audpc.mean()
                df_out = df_out.append(output, ignore_index = True)
        output_file = get_rust_morris_path(year=year, variety=variety, boot=boot)
        df_out.to_csv(output_file)
    
def plot_rust_morris_by_leaf(year = 2012, variety = 'Tremie12',
                             parameter_range_file = './brown_rust/rust_param_range.txt',
                             input_file = './brown_rust/rust_morris_input_full.txt'):
    output_file = get_rust_morris_path(year=year, variety=variety)
    df_out = pd.read_csv(output_file)
    plot_morris_by_leaf(df_out, variable=variable,
                        parameter_range_file=parameter_range_file,
                        input_file=input_file)
                        
def plot_septo_morris_by_leaf_by_boot(year = 2012, variety = 'Tremie12',
                             variable = 'audpc',
                             parameter_range_file = './brown_rust/rust_param_range.txt',
                             input_file = './brown_rust/rust_morris_input_full.txt',
                             nboots = 5, ylims=None):
    output_file = get_rust_morris_path(year=year, variety=variety)
    df_out = pd.read_csv(output_file)
    plot_morris_by_leaf_by_boot(df_out, variable=variable,
                        parameter_range_file=parameter_range_file,
                        input_file=input_file, nboots=nboots, ylims=ylims)

def plot_septo_morris_3_leaves(year = 2012, variety = 'Tremie12', 
                               leaves = [10, 5, 1], variable = 'audpc',
                               parameter_range_file = './brown_rust/rust_param_range.txt',
                               input_file = './brown_rust/rust_morris_input_full.txt',
                               nboots=5, ylims=None):
    output_file = get_rust_morris_path(year=year, variety=variety)
    df_out = pd.read_csv(output_file)
    plot_morris_3_leaves(df_out, leaves=leaves, variable=variable,
                        parameter_range_file=parameter_range_file,
                        input_file=input_file, nboots=nboots, ylims=ylims)
                        
def septo_scatter_plot_by_leaf(year = 2012, variety = 'Tremie12',
                                variable = 'normalized_audpc',
                                parameter = 'Smax'):
    output_file = get_rust_morris_path(year=year, variety=variety)
    df_out = pd.read_csv(output_file)
    scatter_plot_by_leaf(df_out, variable=variable, parameter=parameter)
    
def septo_boxplot_by_leaf(year = 2012, variety = 'Tremie12',
                            variable = 'audpc',
                            parameter = 'Smax', ylims=None):
    output_file = get_rust_morris_path(year=year, variety=variety)
    df_out = pd.read_csv(output_file)
    boxplot_by_leaf(df_out, variable=variable, 
                    parameter=parameter, ylims=ylims)
    
def septo_boxplot_3_leaves(year = 2012, leaves = [10, 5, 1],
                            variety = 'Tremie12',
                            variable = 'audpc',
                            parameter = 'Smax', ylims=None):
    output_file = get_rust_morris_path(year=year, variety=variety)
    df_out = pd.read_csv(output_file)
    boxplot_3_leaves(df_out, leaves=leaves, variable=variable,
                    parameter=parameter, ylims=ylims)