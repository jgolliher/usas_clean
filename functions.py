'''
This python file creates two functions to take a USA Swimming NCAA Top Times Report
CSV file, clean it, and export it as a formatted CSV file.

The first function `toSeconds` converts string formatted swim times into seconds.

Example:
-------
    toSeconds('1:41.39')
        101.39
        
The second functon `CleanUSAS` cleans the formatting issues within USA Swimming's
export file. It takes two arguments- the dataframe of the "dirty" export file and
a description that will be included in the CSV export file.

Example:
-------
    CleanUSAS(DATA,Description='SEC_Rankings')
'''

#### Libraries ####

import pandas as pd
import numpy as np

def toSeconds(timestring):
    '''
    toSeconds(timestring)
        Convert swimming time to seconds
    
    Parameters
    ----------
    timestring : str
        Swimming time in string format
    
    Examples
    ---------
        toSeconds('1:41.39')
    '''
    if len(timestring) > 5:
        i = timestring.split(':')
        y = (float(i[0]) * 60) + float(i[1])
    elif len(timestring) <= 5:
        y = float(timestring)
    else:
        print('ERROR')
    return y


def CleanUSAS(DATA,Description='MeetName'):
    '''
    CleanUSAS(DATA,Description='MeetName')
        Clean USAS NCAA CSV file
        
        Parameters
        ----------
        DATA : Pandas DataFrame
            DataFrame that has already been read-in
        Description : str
            Description of file; used to name export CSV
        
        Examples
        --------
            CleanUSAS(DATA=df, Description='2021_22_SEC')
    '''
    #Rename columns
    DATA.columns = ['MeetName','Time','Date','FullDesc','TCode','TeamShortName',
                'AthFullName','Gender','DOB','EventID','SwimTimeAsTime',
                'AltAdjustFlag','ConvertedTimeFlag','EligPeriodCode',
                'StandardName','EventRank','FullDescIntl','FINAPoints',
                'MeetCity','CountryCode','Ineligable_Secondary_Team']
    
    #Remove `=` and `"` from all columns
    DATA = DATA.replace('=','',regex=True)
    DATA = DATA.replace('"','',regex=True)
    
    #Split `Name` into `First` and `Last`
    DATA[['Last','First']] = DATA.AthFullName.apply(lambda x: pd.Series(str(x).split(',')))
    
    #Replace long stroke names with short stroke names
    DATA['FullDesc'] = DATA['FullDesc'].str.replace('Butterfly','Fly')
    DATA['FullDesc'] = DATA['FullDesc'].str.replace('Backstroke','Back')
    DATA['FullDesc'] = DATA['FullDesc'].str.replace('Breaststroke','Breast')
    DATA['FullDesc'] = DATA['FullDesc'].str.replace('Freestyle','Free')
    DATA['FullDesc'] = DATA['FullDesc'].str.replace('Individual Medley','IM')
    
    #Split out race information
    DATA[['Distance','Stroke','Course','Gender']] = DATA.FullDesc.apply(lambda x: pd.Series(str(x).split(' ')))
    
    #Convert `DOB` and `Date` to DateTime format
    DATA['DOB'] = pd.to_datetime(DATA['DOB'])
    DATA['Date'] = pd.to_datetime(DATA['Date'])
    
    #DOB for ID purposes
    DATA['ID_DOB'] = DATA['DOB'].astype('string').str.replace('-','')
    
    #Convert time to seconds
    DATA['TimeSS'] = DATA['Time'].apply(toSeconds)
    DATA['TimeSS'] = np.round(DATA['TimeSS'],decimals=2)
    
    #Create ID column
    DATA['ID'] = DATA[['Last','ID_DOB','Distance','Stroke','Course']].agg(''.join,axis=1)
    
    #Create final data frame
    FORMATTED = DATA[['ID','First','Last','Gender','DOB','TCode','Distance','Stroke','Course','Time','TimeSS','EventRank','Date','MeetName']]
    FORMATTED.to_csv(f'FORMATTED_{Description}.csv') 
    return FORMATTED




