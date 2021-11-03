import P4J
import time
import pandas as pd
import numpy as np
import tqdm


def get_period(method, mjd, mag, error, fids=None):
    """ 
    Computes the period from the periodogram created with the
    input data using one of the methods from P4J
    
    Parameters
    ---------
    method: {'PDM1', 'LKSL', 'AOV', 'MHAOV', 'QMICS', 'QMIEU'} 
        Method used to perform the fit
        
        PDM: Phase Dispersion Minimization
        LKSL: Lafler Kinman statistic for string length
        AOV: Analysis of Variance Periodo
        MHAOV: Orthogonal multiharmonic AoV
        QMICS: Cauchy Schwarz Quadratic Mutual Information
        QMIEU: Euclidean Quadratic Mutual Information    

    mjd: float python list
        Modified julian date (time instants)

    mag: float python list
        Stellar magnitude 

    err: float python list
        Photometric error

    fids: int python list
        Band identifier
    """
    if fids != None:
        my_per = P4J.MultiBandPeriodogram(method=method)
        my_per.set_data(mjd, mag, error, fids)
    else:
        my_per = P4J.periodogram(method=method)
        my_per.set_data(mjd, mag, error)        
    
    start = time.time()
    my_per.frequency_grid_evaluation(fmin=1e-3, fmax=20.0, fresolution=1e-3, log_period_spacing=True)
    my_per.finetune_best_frequencies(fresolution=1e-4, n_local_optima=10)
    p_time = time.time() - start
    
    freq, per = my_per.get_periodogram()
    fbest, pbest = my_per.get_best_frequencies()
    return 1/fbest[0], p_time


def object_estimation(obj, method, n_samples=None, multiband=False):
    """ 
    Computes the period of an object using one of the methods from P4J
    
    Parameters
    ---------
    obj: pandas DataFrame
        DataFrame containing the detection data of a determined
        object

    method: {'PDM1', 'LKSL', 'AOV', 'MHAOV', 'QMICS', 'QMIEU'} 
        Method used to perform the fit
        
        PDM: Phase Dispersion Minimization
        LKSL: Lafler Kinman statistic for string length
        AOV: Analysis of Variance Periodo
        MHAOV: Orthogonal multiharmonic AoV
        QMICS: Cauchy Schwarz Quadratic Mutual Information
        QMIEU: Euclidean Quadratic Mutual Information    

    n_samples: positive integer
        Number of samples to be used for the period estimation

    multiband: boolean
        Condition to choose if the period estimation will consider
        the bands seperatly (single band) or all together (multi band)
    """    
    obj_g = obj[obj["fid"] == 1]
    obj_r = obj[obj["fid"] == 2]
    if n_samples != None:
        try:
            obj_g = obj_g.sample(n = n_samples, random_state = 42)
            obj_r = obj_r.sample(n = n_samples, random_state = 42)
            obj_band_list = [obj_g, obj_r]
        except:
            pass
    fbest = []
    comp_time = []
    if multiband:
        try:
            obj = pd.concat(obj_band_list)
            fbest_mb, comp_time_mb = get_period(
                method, 
                obj.mjd.values,
                obj.magpsf_corr.values,
                obj.sigmapsf_corr_ext.values,
                obj.fid.values)
        except:
            fbest, comp_time = np.nan, np.nan
        fbest.append(fbest_mb)
        comp_time.append(comp_time_mb)
    else:
        for obj_band in obj_band_list:
            try:
                fbest_band, comp_time_band = get_period(
                    method, 
                    obj_band.mjd.values,
                    obj_band.magpsf_corr.values,
                    obj_band.sigmapsf_corr_ext.values)
            except:
                fbest_band, comp_time_band = np.nan, np.nan 
            fbest.append(fbest_band)
            comp_time.append(comp_time_band)                
    return [obj_g.shape[0], obj_r.shape[0]] + comp_time + fbest

def multi_object_estimation(objs_df, method, n_samples=None, multiband=False):
    """ 
    Computes the period of multiple objects using one of the methods from P4J
    
    Parameters
    ---------
    objs_df: pandas DataFrame
        DataFrame containing the detection data of multiple
        objects

    method: {'PDM1', 'LKSL', 'AOV', 'MHAOV', 'QMICS', 'QMIEU'} 
        Method used to perform the fit
        
        PDM: Phase Dispersion Minimization
        LKSL: Lafler Kinman statistic for string length
        AOV: Analysis of Variance Periodo
        MHAOV: Orthogonal multiharmonic AoV
        QMICS: Cauchy Schwarz Quadratic Mutual Information
        QMIEU: Euclidean Quadratic Mutual Information    

    n_samples: positive integer
        Number of samples to be used for the period estimation

    multiband: boolean
        Condition to choose if the period estimation will consider
        the bands seperatly (single band) or all together (multi band)
    """    
    period_list = []
    objs_oid = objs_df.index.unique()
    with tqdm.tqdm(total=len(objs_oid)) as pbar:
        for oid in objs_oid:
            obj_estimations = []
            query = object_estimation(objs_df.loc[oid], method, n_samples, multiband)
            obj_estimations += query
            pbar.update(1)
            period_list.append([oid] +obj_estimations)
    if multiband:
        band_columns =  [f"{method}_time", f"{method}_T"]
    else:
        band_columns = [f"{method}_time_g", f"{method}_time_r",f"{method}_T_g",f"{method}_T_r"]
    return pd.DataFrame(period_list,
                        columns = ['oid', f'{method}_samples_g', f"{method}_samples_r"] + band_columns).set_index("oid")