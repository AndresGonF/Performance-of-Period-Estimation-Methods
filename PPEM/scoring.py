import pandas as pd
import numpy as np

def fold_scores_summary(fold_scores, score_names):
    """ 
    Summarizes the scores from a folded curve inspection in 
    a DataFrame format
    
    Parameters
    ---------
    fold_scores: pandas DataFrame
        DataFrame containing the scores of the period estimation
        of a class using multiple methods 

    score_names: string python list 
        List of the criteria names used for scoring
    """    
    score_df = pd.DataFrame(index=range(len(score_names)+2),
                            columns=fold_scores.columns)
    scores = []
    for i in fold_scores.columns:
        scores.append(fold_scores[i].value_counts())
    scores = pd.concat(scores, axis=1).sort_index()
    score_df.fillna(scores,inplace=True)
    score_names += ["Null", "Non-Nulls"]
    score_df.rename(lambda i: score_names[int(i)],inplace=True)
    score_df.fillna(0,inplace=True)
    score_df.loc["Non-Nulls"] = 100 - score_df.loc["Null"]
    
    score_df, nulls_df = score_df.iloc[:-2], score_df.iloc[-2:]
    
    score_df /= nulls_df.loc["Non-Nulls"]
    return score_df, nulls_df/100


def summary_source(classes_fold_score_list, classes_periods, classes):
    """ 
    Summarizes the scores of multiple classes from the folded curves 
    inspection in a DataFrame format considering only the data from the 
    catalogs
    
    Parameters
    ---------
    classes_fold_score_list: pandas DataFrame python list
        List of DataFrames containing the scores of the period estimation
        of multiple classes

    classes_periods: pandas DataFrame python list 
        List of DataFrames containing the catalog's periods

    classes: string python list
        List of the names of the classes to be considered
    """        
    scores = []
    for idx in range(len(classes_periods)):
        temp = pd.concat([classes_fold_score_list[idx], classes_periods[idx].source], axis=1)
        temp = temp.groupby(['source', 'catalog']).size().unstack(fill_value=0).T
        scores.append(temp)
    score_df = pd.concat(scores, keys=classes)
    score_df.index.set_levels(["Wrong", "Right", "Multiply"], 
                              level=1,
                              inplace=True)
    score_df = (score_df.T.fillna(0))
    dividend = score_df.iloc[:, score_df.columns.get_level_values(1)=="Right"].T.droplevel(-1).T
    divisor = score_df.T.groupby(level=0).sum().T.loc[:,["RRL","Ceph","LPV","DSCT","EB"]]
    return dividend.divide(divisor).round(2).mean(axis=1)    



def summary_scores(fold_scores_list):
    """ 
    Summarizes the scores from multiple folded curves inspection in 
    a DataFrame format for a single class.
    
    Parameters
    ---------
    fold_scores_list: pandas DataFrame python list
        List of DataFrames containing the scores of the period estimation
        of a single class with different number of samples being used
    """        
    d = {}
    nulls = {}
    for idx, score in enumerate(fold_scores_list):
        d.update({f"{idx+1}0 samples:": score[0].T})
        nulls.update({f"{idx+1}0 samples:": score[1].T})
        
    summary_scores = pd.concat(d.values(), axis=1, keys=d.keys()).T
    summary_nulls = pd.concat(nulls.values(), axis=1, keys=nulls.keys()).T
    return summary_scores, summary_nulls