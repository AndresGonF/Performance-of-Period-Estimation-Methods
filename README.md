PPEM
===

Description
-----------

PPEM is a project for a guided work from Universidad de Chile. The main focus of this work is to analyze the performance of the period estimation methods currently available at the P4J package (https://github.com/phuijse/P4J). These methods are used by ALeRCE, specifically with variable stars and periods. There are multiple methods for the estimation of these periods, among which MHAOV is the one that's used most because of it's good performance. However, there are other methods implemented on this library and although there's evidence to prefer the MHAOV method, an exhaustive analysis has'nt been carried out taking into account the folded curves with the estimated periods. Then, for this work it'll be studied the performance of each one of the methods for different classess (RRL, Ceph, LPV ,DSCT, EB/EW) and using different number of detections for the estimations, in addition to also analyzing the current labels that are available.


Contents
--------

1. Introduction
2. Work methodology\
    2.1. Database\
    2.2. Object selection\
    2.3. Period estimation\
    2.4. Folde curve scoring
3. Analysis and results\
    3.1. Catálogo\
    3.2. Hit-rate\
    3.3. Computing time
4. Difficulties
5. Conclusions and future work

Instalation
-----------

Dependencies::

    P4J
    Numpy
    GCC
    Cython (optional)
    Pandas
    Matplotlib


Install by cloning this github and do:

    python setup.py install --user

Report
-------

Please review

    https://github.com/AndresGonF/Performance-of-Period-Estimation-Methods/blob/main/reports/Informe_Trabajo_Dirigido.pdf
    
    
Process
-------

Please review

    https://github.com/AndresGonF/Performance-of-Period-Estimation-Methods/blob/main/notebooks/Trabajo%20dirigido%20-%20Desempe%C3%B1o%20m%C3%A9todos.ipynb


Authors
-------

-  Andrés González
-  Pablo A. Estévez (tutor)
-  Ignacio Reyes (tutor)

References
----------
1. M. Catelan, H. Smith ``Pulsating Stars''. Weinheim Germany: Wiley-VCH, 2015.
2. P. Huijse et al ``Robust Period Estimation Using Mutual Information for Multiband Light Curves in the Synoptic Survey Era'' in ApJS, 2018, 236 12.
3. N. Mondrik et al ``A MULTIBAND GENERALIZATION OF THE MULTIHARMONIC ANALYSIS OF VARIANCE PERIOD ESTIMATION ALGORITHM AND THE EFFECT OF INTER-BAND OBSERVING CADENCE ON PERIOD RECOVERY RATE'' in ApJL, 2015, 811 L34.
4. P. Huijse, P. Protopapas, P. Estévez, P. Zegers, J. Príncipes, ``P4J'', 2016.
