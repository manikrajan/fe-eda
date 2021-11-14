"""
countyAnalysis class used for county level analysis of food environment dataset

"""
import pandas as pd
import numpy as np
import random

# Define a class for county level analysis
class countyAnalysis:
  # Decription of class and fields

    def __init__(self, df_county, target_var = None, var_list = None):
      '''
      Class constructor
      df_county: county level dataframe (pre-formatted and cleaned)
      target_var: optional, specify variable of interest for future analysis
      var_list: optional, specific list of variables you're interested in exploring (i.e. their relation to target)
      '''
      self.df_county = df_county.copy() # Original dataframe, copy so that changes within class doesn't change original
      self.target_var = target_var
      self.var_list = var_list
    
    def select_state(self, state):
      # Filter dataframe to counties from a specfific state
      self.df_county = self.df_county[self.df_county['State']==state]
    
    def calculate_na_summary(self):
      # Calculate percent missing
      self.pct_missing = self.df_county.isnull().sum() * 100 / len(self.df_county)
      # Find variable with largest % missing
      print('Missing values summary: ')
      print('The 10 variables with the highest percent missing are: ') 
      print(self.pct_missing.nlargest(10))
    
    def remove_missing_threshold_cols(self, threshold):
      print(f"Removing columns with greater than {(threshold)*100}% missing")
      # Remove variables with more than "theshold"% missing
      # Threshold in drop na is number of observations so multiply theshold % by number of rows
      self.df_county.dropna(thresh=self.df_county.shape[0]*(1-threshold), axis=1, inplace=True)
    
    def remove_missing_threshold_rows(self, threshold):
      print(f"Removing rows (counties) with greater than {(threshold)*100}% missing")
      # Remove rows (counties) with more than "theshold"% missing
      # Threshold in drop na is number of observations so multiply theshold % by number of columns
      self.df_county.dropna(thresh=self.df_county.shape[1]*(1-threshold), axis=0, inplace=True)
    
    def calculation_correlations_with_variable(self, num_pos_corr = 10, num_neg_corr = 10, display_all = False):
      '''
      num_pos_corr: number of top postive correlations to display. Default 10
      num_neg_corr: number of top negative correlations to display. Default 10   
      display_all: (default false), but if true will display all correlations (not just top pos/neg)
      '''
      # todo: skip non-numeric columns
      # todo: option to remove high correlations
      
      # If haven't defined variable of interest, prompt user to select
      if self.target_var is None:
        self.select_target_var()
      if self.var_list is not None: # If provided a list of variables only calculte correlations for those
        self.corrs_with_var = self.df_county[self.var_list].apply(lambda x: x.corr(self.df_county[self.target_var]))
      else: # Otherwise use all other variables (but only numeric columns)
        numeric_cols = self.df_county.select_dtypes(include=np.number).columns.tolist() # Select only numeric columns to calculate correlations with target
        self.corrs_with_var = self.df_county[numeric_cols].drop([self.target_var],axis=1).apply(lambda x: x.corr(self.df_county[self.target_var]))
      if not display_all:
        # Display top correlations
        print(f'Top {num_pos_corr} largest (positives) correlations with {self.target_var}: ')
        print(self.corrs_with_var.nlargest(num_pos_corr))
        print(f'Top {num_neg_corr} smallest (negative) correlations {self.target_var}: ')
        print(self.corrs_with_var.nsmallest(num_neg_corr))
      else:
        print(f"Top correlations with {self.target_var}:")
        print(self.corrs_with_var.sort_values())
    
    
    def find_zero_variance_state_cols(self, drop = False):
      # Calculate standard deviation for each variable within each state
      # To identify columns that are really at a state level 
      # (i.e. all counties within the state have the same value)
      state_stdev = self.df_county.groupby(['State']).std()
    
      self.state_zero_var_cols = []
      for col in state_stdev.columns:
        if state_stdev[col].sum() == 0:
          self.state_zero_var_cols.append(col)
    
      # If desired, drop columns that are really state level
      if drop == True:
        self.df_county.drop(self.state_zero_var_cols, axis=1, inplace=True)
    
    
    def find_most_recent_data(self, drop = False):
      '''
      Some of the columns in this dataset measure the same thing but for different years.
      For example: 'LACCESS_POP10' and 'LACCESS_POP15'.
      For some analysis we may be interested in both of these columns while for others 
      we may only want to consider the most recent year.
      This function helps to find the columns that contain data for multiple years
      and gives the option of dropping any that are not the most recent.
      '''
      column_stub_dict = {}
    
      # Create dictionary of column name stubs (column name minus last two elements)
      # With list of the last two elements (i.e. years) that match each name stub
      for i, col in enumerate(self.df_county.columns):
        if f'{col[:-2]}' in column_stub_dict: # If we've already searched for columns that match this beginning
          continue # Skip this column
        column_stub_dict[f'{col[:-2]}'] = [col[-2:]] # Create dictionary row for this beginning
        for j, x in enumerate(self.df_county.columns[i+1:]): # Search subsequent columns for match
          if col[:-2] == x[:-2]: # If the elements are the same (other than the last two (years))
            column_stub_dict[f'{col[:-2]}'].append(x[-2:]) # Add the years to the dictionary
    
      # Use column name stub dictionary to find latest (and oldest) datapoint for each
      self.list_recent_cols = []
      self.list_non_recent_cols = []
      for stub in column_stub_dict:
        if len(column_stub_dict[stub])>1: # if there were more than one column (year) for this stub
          int_year_lst = [int(year) for year in column_stub_dict[stub]] # Create list of ints so we can check for max
          for year in column_stub_dict[stub]: # Loop through each year
            if int(year) == max(int_year_lst): # If it is the max add to list_recent_cols
              self.list_recent_cols.append(f'{stub}{year}')
            else: # Otherwise add to list of non-recent columns
              self.list_non_recent_cols.append(f'{stub}{year}')
    
      # Keep only the most recent data points (if desired)
      if drop == True:
        self.df_county.drop(self.list_non_recent_cols, axis=1, inplace=True)
    
    
    def select_variables_to_analyze(self, n):
      '''
      n: number of variables to select
      '''
      print(f"Randomly selecting {n} variables for analysis...")
      all_vars = [var for var in self.df_county.columns if var not in ["FIPS",    "State",    "County"]]
      self.var_list = random.sample(all_vars, n)
      print(f"Selected variables: {self.var_list}")
    
    def select_target_var(self):
        print("Please select a variable of interest: ")
        self.target_var = input()
        if self.target_var not in self.df_county.columns:
          print("This variable is not in this dataset.")
          print("Will be using default (LACCESS_POP15) until a valid variable is chosen.")
          self.target_var = "LACCESS_POP15"
    
    def append_region(self, data_path):
        # Read in region data
        df_region = pd.read_csv(data_path + 'State and Region.csv')
        # Join region data to df_county
        self.df_county = pd.merge(self.df_county, df_region, how='inner', on = 'State')
    

    def average_by_category(self, by_col, new_var_list = None):
        '''
        Calculate average value of variables by another column
        '''
        if new_var_list is not None: # If provided a variable list for this function use it
            self.average_by = self.df_county.groupby(by_col, as_index=False)[new_var_list].mean()
        elif self.var_list is not None: # Otherwise use var_list for the class
          self.average_by = self.df_county.groupby(by_col, as_index=False)[self.var_list].mean()
        else: # Otherwise calculate for all variables
          self.average_by = self.df_county.groupby(by_col, as_index=False).mean()

        return self.average_by

    def labeled_categorical_cols(self):
        # Create column that labels 0/1 in METRO13 variable
        self.df_county['Metro'] = np.where(self.df_county['METRO13']==0, "Non-metro", "Metro")
        # Create column that labels 0/1 in PERPOV10 variable
        self.df_county['Persistent_Poverty'] = np.where(self.df_county['PERPOV10'] == 1, "Persistent-Poverty", "Other")


'''
Other ideas:
- return county with largest/smallest value for a specified variable of interest
- more plotting/visualizing
- exploring/visualizing across years (2012/2017) - like side by side graphs grace had

Other to do:
- Build in check for whether or not variables are in columns (for target_var and var_list)....maybe do some fuzzy matching to match user input to variable column
'''