import pandas as pd
import numpy as np

class NanoBetaCharlie(object):
    '''Pass a NanoBetaCharlie input pandas df (with no header)
        returns a NanoBetaCharlie output csv file'''

    def __init__(self, df):
        self.raw = df


    def clean(self):
        new_df = self.create_multiindex_header(self.raw) #change top three rows to a multi-index header
        new_df_indexed = new_df.set_index([
                                     ('Creator Export Name','Creator Export Name','Creator Export Name'), 
                                     ('Cleaned Name','Cleaned Name','Cleaned Name')
        ])

        new_df_stacked = new_df_indexed.stack([0,1]) #Move report dates and platform to row multi-index
        new_df_ordered = new_df_stacked.swaplevel(0,2).sortlevel([0,1], ascending=[0,1]) # change multi-index order and resort 

        ndf = self.drop_nonessential_index(new_df_ordered) #drop an unessential column, easiest to drop here, could have dropped earlier
        ndf = ndf.swaplevel(0,1).reset_index() #change multi-index levels again and move all indicies to columns
        ndf_cleaned_cols = self.clean_column_names(ndf) 
        cleaned_both_reports = ndf_cleaned_cols.set_index('Creator Name')
        
        #default imputs have two reports of data, we are only interested in latest
        this_report_date = max(cleaned_both_reports['Date']) 
        cleaned_report = cleaned_both_reports[cleaned_both_reports['Date'] == this_report_date]

        return cleaned_report


    def create_multiindex_header(self, df):
        '''takes a df with 3 top rows as headers and converts it to a df with a 3 level multi-index'''
        h1 = df.iloc[0,:] #grab first level
        h2 = df.iloc[1,:] #'' second level
        h3 = df.iloc[2,:]#'' third level

        df_values = df.iloc[3:,:].values #pull original df values excluding headers
        mi = [np.array(h1),np.array(h2),np.array(h3)] #create array for multi-index
        new_df = pd.DataFrame(df_values, columns=mi) #create new df with multi-index and original values

        return new_df


    def drop_nonessential_index(self, new_df_ordered):
        '''drop one of the columns that is unessential for this client'''
        ndf = new_df_ordered 
        ndf.index = new_df_ordered.index.droplevel(2) #drops an index level

        return ndf


    def clean_column_names(self, ndf):
        '''Changes default names given to columns when they were moved out of the index'''
        new_column_names = list(ndf.columns) #get old column names

        #change each column name that needs to be changed
        new_column_names[0] = 'Creator Name'
        new_column_names[1] = 'Date'
        new_column_names[2] = 'Platform'

        #overwrite old column names
        ndf.columns = new_column_names

        return ndf

