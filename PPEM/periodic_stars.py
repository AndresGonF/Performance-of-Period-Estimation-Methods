import matplotlib.pylab as plt
import numpy as np
import tqdm
import pandas as pd
from PPEM.period_estimation import multi_object_estimation

class periodic_stars:

	def __init__(self, database, obj_class, n_objs, n_min):
	    """
	    Class for holding all the objects and tags from a database for 
	    a given type of periodic variable star. From these objects the
	    periods can be computed and then used to inspect the folde curve 
	    
	    Parameters
	    ---------
	    database: postgreSQL_database object
	    	Object to be used as a database to retrieve the objects
	    	detections
	        
	    obj_class: {'RRL', 'Ceph', 'LPV', 'DSCT', 'EB/EW'} 
	        Periodic variable star type to be considered
		
		n_objs: positive integer
			Number of objects to be used

		n_min: positive integer
			Minimum number of detection for each object

		objs_df: pandas DataFrame
			DataFrame containing all the objects with their
			corresponding detections

		tags: pandas DataFrame
			DataFrame containing the tags of all the objects;
			oid, catalog period, and source
	        
	    """		
		self.database = database
		self.obj_class = obj_class
		self.n_objs = n_objs
		self.n_min = n_min


	def get_objects(self, tags, noisy=False, max_sigma=1.0):
	    """
	    Gets the detections from the database of the objects 
	    within the input tags, considering the n_objs and n_min of 
	    the class. The data and the filtered tags are saved in new
	    attributes as 'objs_df' and 'tags', respectivly
	    
	    Parameters
	    ---------

		tags: pandas DataFrame
			DataFrame containing the tags of all the objects;
			oid, catalog period, and source

		noisy: boolean
			Condition to choose if the noisy detections will
			be included

		max_sigma: float
			Limit to be considered as the max amount of noise
			allowed for a detection to be included
	        
	    """		

		objs_oids = tags.index
		obj_samples = []
		with tqdm.tqdm(total=self.n_objs) as pbar:
			for oid in objs_oids:
				if len(obj_samples) >= self.n_objs:
					self.objs_df = pd.concat(obj_samples)
					self.tags = tags.loc[self.objs_df.index.unique()]
					return
				obj = self.database.query(oid)
				if not noisy:
					obj = obj[((obj['sigmapsf_corr_ext'] > 0.0) &
						(obj['sigmapsf_corr_ext'] < max_sigma))]          
				n_g = obj[obj.fid == 1].shape[0]
				n_r = obj[obj.fid == 2].shape[0]
				if (n_g < self.n_min) | (n_r < self.n_min):
					continue
				else:
					obj_samples.append(obj)
					pbar.update(1)


	def set_objects(self, objs_df, tags):	
	    """
	    Sets the detections data and tags manually. It can be
	    used to load previously computed data in csv format
	    
	    Parameters
	    ---------

		objs_df: pandas DataFrame
			DataFrame containing all the objects with their
			corresponding detections

		tags: pandas DataFrame
			DataFrame containing the tags of all the objects;
			oid, catalog period, and source
	        
	    """	

		self.objs_df = objs_df
		self.tags = tags.loc[self.objs_df.index.unique()]


	def compute_periods(self, methods, n_samples=None, multiband=False):
	    """
	    Method for computing the periods of the objects insided the
	    'objs_df' DataFrame using a list of methods available at P4J
	    
	    Parameters
	    ---------

	    methods: python list 
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
		estimated_periods = []
		for method in methods:
			print("-"*10 + " " + method + " " + "-"*10)
			method_estimated_periods = multi_object_estimation(self.objs_df, method, n_samples, multiband)
			estimated_periods.append(method_estimated_periods)
		return pd.concat([self.tags]+estimated_periods,axis=1)


	def folded_curve(self, obj_oid, band_periods):
	    """
	    Method for plotting the folded curve of an object according
	    to it's 'oid', using the input periods
	    
	    Parameters
	    ---------

	    obj_oid: string 
	    	oid of an object inside 'objs_df'

		band_periods: tuple
			Tuple of periods to select the g-band and r-band periods
			to be used for folding the curve

	    """				
		print(obj_oid)
		obj = self.objs_df.loc[obj_oid]
		catalog_period = self.tags.loc[obj_oid].period
		print(f'Catalog period = {catalog_period}')
		bands = ["green","red"]
		fig, ax = plt.subplots(1, 2, figsize=(20,5))
		for idx, band in enumerate(bands):
			period = band_periods[idx]
			print(f'{band[0]}-band period = {band_periods[idx]}')

			obj_band = obj[obj.fid == idx+1]

			phase = np.mod(obj_band.mjd, period)* (1/period)
			
			ax[idx].errorbar(
				phase, 
				obj_band.magpsf_corr.values, 
				obj_band.sigmapsf_corr_ext.values, 
				fmt='.', color=band)
			ax[idx].set_title(f'{obj_oid} {band[0]}-band folded curve')
			ax[idx].set_xlabel('Phase @ %0.5f [1/d], %0.5f [d]' %(1/period, period))
			ax[idx].set_ylabel('Magnitude')
			ax[idx].invert_yaxis()
			ax[idx].grid()

		plt.tight_layout()
		plt.show();          