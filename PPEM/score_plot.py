import matplotlib.pylab as plt

def hitrate_plot(sample_list, fold_score_sb, fold_score_mb, score, method_list, MHAOV=False, figsize=(20,10)):
    plt.rcParams['axes.grid'] = True
    font = {'size'   : 15,
           'weight':'bold'}
    plt.rc('font', **font)    
    
    fig, ax = plt.subplots(nrows=1,
                           ncols=3,
                           figsize=figsize,
                          sharex=True,
                          sharey=True)
    style = ["-o","-^","-x","-8","-*","-+","-p"]
    for idxx, method in enumerate(method_list):
        for idx, band in enumerate(["g","r"]):
            ax[idx].plot(sample_list,
                       [fold_score.iloc[score][f"{method}_{band}"] for fold_score in fold_score_sb],
                       style[idxx])
            ax[idx].legend(method_list)
            ax[idx].set_xlabel("N° samples", **font)
            ax[idx].set_ylabel("Hit rate", **font)
            ax[idx].set_title(f"{band.upper()} - band", **font)
            ax[idx].set_ylim([0,1])
        
        if MHAOV:
            ax[2].plot(sample_list,
                       [fold_score.iloc[score][f"MHAOV_g"] for fold_score in fold_score_mb],
                       "-o")
            ax[2].legend(["MHAOV"])
            ax[2].set_xlabel("N° samples", **font)
            ax[2].set_title(f"All - band", **font)
            ax[2].set_ylim([0,1])
        else:
            ax[2].plot(sample_list,
                       [fold_score.iloc[score][f"{method}_g"] for fold_score in fold_score_mb],
                       "-o")
            ax[2].legend(method_list)
            ax[2].set_xlabel("N° samples", **font)
            ax[2].set_title(f"All - band", **font)
            ax[2].set_ylim([0,1])
    ax[1].set_ylabel("")
    plt.show()    



def time_plot(sample_list, periods_sb, periods_mb, method_list, MHAOV=False, figsize=(20,10)):
    plt.rcParams['axes.grid'] = True
    font = {'size'   : 15,
           'weight':'bold'}
    plt.rc('font', **font)    
    
    fig, ax = plt.subplots(nrows=1,
                           ncols=3,
                           figsize=figsize,
                          sharex=True,
                          sharey=True)
    style = ["-o","-^","-x","-8","-*","-+","-p"]
    
    for idxx, method in enumerate(method_list):
        for idx, band in enumerate(["g","r"]):
            ax[idx].plot(sample_list,
                       [periods[f"{method}_time_{band}"].mean() for periods in periods_sb],
                       style[idxx])
            ax[idx].legend(method_list)
            ax[idx].set_xlabel("N° samples", **font)
            ax[idx].set_ylabel("Time [s]", **font)
            ax[idx].set_title(f"{band.upper()} - band", **font)
            ax[idx].set_yscale("log")
                
        if MHAOV:
            ax[2].plot(sample_list,
                       [periods[f"MHAOV_time"].mean() for periods in periods_mb],
                       "-o")
            ax[2].legend(["MHAOV"])
            ax[2].set_xlabel("N° Samples", **font)
            ax[2].set_title(f"All - band", **font)
            ax[2].set_yscale("log")
        else:
            ax[2].plot(sample_list,
                       [periods[f"{method}_time"].mean() for periods in periods_mb],
                       "-o")
            ax[2].legend(method_list)
            ax[2].set_xlabel("N° Samples", **font)
            ax[2].set_title(f"All - band", **font)
            ax[2].set_yscale("log")
    ax[1].set_ylabel("")
    plt.show()           