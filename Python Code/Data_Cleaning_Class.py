"""
DataCleaning class used for cleaning raw data from the Food Environment Atlas.
"""

# Import libraries
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup


class DataCleaning:

    def __init__(self, df):
        '''
		Initialize instance of data cleaning class
		:param df: dataframe to perform data cleaning on
		'''
        self.df = df.copy()  # Original dataframe

    # copy so that changes within class doesn't change original

    def full_data_cleaning(self):
        '''
			Method to perform all necessary cleaning tasks. Each distinct task/step
			is defined as its own method and called sequentially.
			'''
        self.clean_state_column()
        self.prep_fips_lookup_table()
        self.clean_county_column()
        self.reformat_data()
        self.split_state_county_data()

    def clean_state_column(self):
        # Fill any nan with empty string
        self.df['State'] = self.df['State'].fillna('')
        # Remove extra whitespace on some state names
        self.df['State'] = self.df['State'].str.strip()

    def prep_fips_lookup_table(self):
        # Webscrape fips table
        self.webscrape_fips_lookup()
        # Add missing fips codes to the table
        self.add_missing_fips()

    def webscrape_fips_lookup(self):
        '''
		Function to webscrape fips lookup table
		'''
        # Define header
        headers = {
            'user-agent': 'UVA Project (pkx2ec@virginia.edu) (Language=Python 3.8.2; Platform=Macintosh; Intel Mac OS X 11_5_2)'}
        # Specify URL
        URL = 'https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/home/?cid=nrcs143_013697'
        # Access HTML content
        r = requests.get(URL, headers=headers)
        # Parse HTML content
        soup = BeautifulSoup(r.content, 'html5lib')
        # Find data of interest
        table = soup.find('div', attrs={'class': 'centerColImg'})
        # Create empty dataframe to save FIPS info
        self.fips_table = pd.DataFrame(columns=['FIPS', 'County', 'State'])
        # Add each FIPS code to dataframe
        first_row = True
        for row in table.findAll('tr'):
            # First row doesn't have the info we want so skip it
            if first_row:
                first_row = False
            else:
                row_entries = row.findAll('td')
                row_text = [i.text for i in row_entries]
                self.fips_table.loc[len(self.fips_table)] = row_text
        # Change type of fips table to int so we join it with our data
        self.fips_table['FIPS'] = self.fips_table['FIPS'].astype(int)

    def add_missing_fips(self):
        # Update fips lookup table to add any fips in df, but not fips_table
        # List of fips codes in df and fips_table
        original_fips = self.df.FIPS.unique()
        new_fips = self.fips_table.FIPS.unique()
        # For any missing fips, add the info from the first record in df
        for i in original_fips:
            if i not in new_fips:
                self.fips_table.loc[len(self.fips_table.index)] = \
                    self.df.loc[self.df['FIPS'] == i, ['FIPS', 'County', 'State']].iloc[0]

    def clean_county_column(self):
        # Webscrape fips lookup table
        self.prep_fips_lookup_table()
        # Add any missing fips codes to the lookup table
        self.add_missing_fips()
        # Drop original state and county columns (otherwise we'll have 2 columns with the same name)
        self.df.drop(['State', 'County'], axis=1, inplace=True)
        # Join together fips lookup table
        # Left join so we don't lose any data from our original table
        self.df = self.df.merge(self.fips_table, on=['FIPS'], how='left')

    def reformat_data(self):
        # Re-format so variables are across the columns not adding rows in the "Variable Code" column
        self.pivot = pd.pivot_table(self.df, index=['FIPS', 'State', 'County'], columns='Variable_Code', values='Value')
        self.pivot.reset_index(inplace=True)

    def split_state_county_data(self):
        '''
		Some FIPS codes (1-56) are state level, all others are at the county level.
		In addition, some of the variables in the dataset are at the state level
		(corresponding to these 1-56 FIPS codes) and thus will be missing for
		all the remaining county level FIPS codes. Other variables are at a county
		level so those will be missing for the state level FIPS codes.

		This method splits the data into a state level and county level dataframe
		and removes variables with all missing values in the resulting dataframes.
		'''
        # Split data based on FIPS code
        self.df_state = self.pivot[self.pivot.FIPS <= 56]
        self.df_county = self.pivot[self.pivot.FIPS > 56]
        # Drop columns with all missing values
        self.df_state = self.df_state.dropna(axis=1, how='all')
        self.df_county = self.df_county.dropna(axis=1, how='all')
