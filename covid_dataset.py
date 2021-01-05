import numpy as np
import pandas as pd

# Creates COVID-19 County Level Dataset

# Basic Stats Relating to the Virus *download "stat_data.csv", attached, and insert the path of the file*

# "stat_data.csv" comes from the census website and has been cut down to only a few important attributes; download the full file here: https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/cc-est2019-alldata.csv

def create_race_data():
    
    stat_data = pd.read_csv('/Users/kabirmoghe/Desktop/COVID Stuff for Article and github/stat_data.csv', index_col=0).rename(columns = {'Population Density': 'Approximate Population Density'})
    
    pop_url = 'https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_county_population_usafacts.csv'

    pop = pd.read_csv(pop_url)
    pop['countyFIPS'] = pop['countyFIPS'].apply(lambda value: '0' + str(value) if len(str(value)) == 4 else str(value))
    pop = pop[pop['County Name'] != 'Statewide Unallocated'].reset_index(drop = True)[['County Name', 'State','population']].rename(columns = {'population':'Population'})
    pop['County Name'] = pop['County Name']  + ', ' + pop['State']
    
    race_data = pd.merge(pop, stat_data)
    
    race_cols = ['African American', 'Hispanic', 'Asian American', 'White American', 'Native American and Alaska Native', 'Native Hawaiian and Other Pacific Islander']

    for col in race_cols:
        race_data['% ' + str(col)] = round(race_data[col + ' Population'] / race_data['Population'] * 100,2)
        race_data = race_data.drop(col + ' Population', axis = 1)    
    
    race_data = race_data.drop(['Population','State'], axis = 1)
    
    return race_data

# Income / Unemployment Data

def create_inc_unemp_data():
    
    income_data = pd.read_excel('https://www.ers.usda.gov/webdocs/DataFiles/48747/Unemployment.xls?v=2512', skiprows = 7)[['area_name','Unemployment_rate_2019', 'Median_Household_Income_2018']].reset_index(drop = True).rename(columns = {'area_name': 'County Name', 'Unemployment_rate_2019': '% Unemployed', 'Median_Household_Income_2018':'Median Household Income'})
    
    income_data['% Unemployed'] = income_data['% Unemployed'].round(2)
    
    ### Broken down below
    
    # income_data = pd.read_excel('https://www.ers.usda.gov/webdocs/DataFiles/48747/Unemployment.xls?v=2512', skiprows = 7)
    
    #income_data = income_data[['area_name','Unemployment_rate_2019', 'Median_Household_Income_2018']] # Includes the unemployment rate in 2019 and the median household income as of 2018 (per county)

    #income_data = income_data.reset_index(drop = True)

    #income_data = income_data.rename(columns = {'area_name': 'County Name', 'Unemployment_rate_2019': '% Unemployed', 'Median_Household_Income_2018':'Median Household Income'})
    
    return income_data

# Education Data

def create_edu_data():
    sts = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
           "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
           "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
           "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
           "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
           "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
           "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
           "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
    
    edu_link = 'https://www.ers.usda.gov/webdocs/DataFiles/48747/Education.xls?v=6188.1'
    
    edu_data = pd.read_excel(edu_link).drop([0,1,2,4])
    
    edu_data.columns = edu_data.loc[3].values
    
    edu_data = edu_data.drop(3).reset_index(drop = True)

    for value in edu_data['Area name']:
        if value in sts:
            edu_data.drop(edu_data[edu_data['Area name'] == value].index[0], inplace = True)
        
    edu_data['Area name'] = edu_data['Area name'] + ', ' + edu_data['State']

    edu_data = edu_data.rename(columns = {'Area name': 'County Name'})

    edu_data = edu_data[['County Name', "Some college or associate's degree, 2014-18"]]
    
    # Creates more understandable education metric
    
    pop_url = 'https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_county_population_usafacts.csv'

    pop = pd.read_csv(pop_url)
    pop['countyFIPS'] = pop['countyFIPS'].apply(lambda value: '0' + str(value) if len(str(value)) == 4 else str(value))
    pop = pop[pop['County Name'] != 'Statewide Unallocated'].reset_index(drop = True)[['County Name', 'State','population']].rename(columns = {'population':'Population'})
    pop['County Name'] = pop['County Name']  + ', ' + pop['State']
    
    edu_data = pd.merge(pop, edu_data, on = 'County Name')
    
    edu_data["Approx. % People with College or Associate's Degree per Year"] = [round(float(val), 2) for val in ((edu_data["Some college or associate's degree, 2014-18"] / 4) / edu_data['Population'] *100)]

    edu_data = edu_data.drop(["Some college or associate's degree, 2014-18", 'State', 'Population'], axis = 1)
    
    return edu_data

# Creates a dataframe of statewide data about mask reqs

#link = https://masks4all.co/what-states-require-masks/ ; you must click the "Get the data" button and save it as 'data-AD5p1.csv', * and then change the path of the file in the line below accordingly *

def create_mask_data():
    states = {
        'District of Columbia': 'DC',
        'Puerto Rico': 'PR',
        'Alabama': 'AL',
        'Montana': 'MT',
        'Alaska': 'AK',
        'Nebraska': 'NE',
        'Arizona': 'AZ',
        'Nevada': 'NV',
        'Arkansas': 'AR',
        'New Hampshire': 'NH',
        'California': 'CA',
        'New Jersey': 'NJ',
        'Colorado': 'CO',
        'New Mexico': 'NM',
        'Connecticut': 'CT',
        'New York': 'NY',
        'Delaware': 'DE',
        'North Carolina': 'NC',
        'Florida': 'FL',
        'North Dakota': 'ND',
        'Georgia': 'GA',
        'Ohio': 'OH',
        'Hawaii': 'HI',
        'Oklahoma': 'OK',
        'Idaho': 'ID',
        'Oregon': 'OR',
        'Illinois': 'IL',
        'Pennsylvania': 'PA',
        'Indiana': 'IN',
        'Rhode Island': 'RI',
        'Iowa': 'IA',
        'South Carolina': 'SC',
        'Kansas': 'KS',
        'South Dakota': 'SD',
        'Kentucky': 'KY',
        'Tennessee': 'TN',
        'Louisiana': 'LA',
        'Texas': 'TX',
        'Maine': 'ME',
        'Utah': 'UT',
        'Maryland': 'MD',
        'Vermont': 'VT',
        'Massachusetts': 'MA',
        'Virginia': 'VA',
        'Michigan': 'MI',
        'Washington': 'WA',
        'Minnesota': 'MN',
        'West Virginia': 'WV',
        'Mississippi': 'MS',
        'Wisconsin': 'WI',
        'Missouri': 'MO',
        'Wyoming': 'WY',
    }
    
    mask_data = pd.read_csv('/Users/kabirmoghe/Desktop/Datasets/data-AD5p1.csv')

    mask_data['State.'] = mask_data['State.'].apply(lambda value: value[1:].split(']')[0])
    
    mask_data = mask_data.rename(columns = {'State.':'State'})
    
    mask_data['State'] = mask_data['State'].map(states)
    
    def mask_cleaner(val):
        if val == 'Entire State' or val == 'Entire Territory':
            return 'Yes'
        elif val == 'No':
            return val
        else:
            return 'Some Parts'
    
    mask_data['Statewide Mask Requirement'] = mask_data['Masks Required?'].apply(mask_cleaner)
    mask_data.drop(['Masks Required?','Requirement Date','Type of Requirement'], axis = 1, inplace = True) 
    
    return mask_data

# Data from usafacts.org (https://usafacts.org/visualizations/coronavirus-covid-19-spread-map/)
# URLs for cases, deaths, and population data from the above website

def create_covid_pop_data():
    cases_url = 'https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_confirmed_usafacts.csv'
    deaths_url = 'https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_deaths_usafacts.csv'
    pop_url = 'https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_county_population_usafacts.csv'

    # Creates the cumulative cases dataframe
    cases = pd.read_csv(cases_url)
    cases['countyFIPS'] = cases['countyFIPS'].apply(lambda value: '0' + str(value) if len(str(value)) == 4 else str(value))
    cases = cases[cases['County Name'] != 'Statewide Unallocated'].reset_index(drop = True)
    cases['County Name'] = cases['County Name']  + ', ' + cases['State']
    cases.drop(['12/28/20','12/29/20','12/30/20','12/31/20','1/1/21','1/2/21'], axis = 1, inplace = True)

    # Creates the cumulative deaths dataframe
    deaths = pd.read_csv(deaths_url)
    deaths['countyFIPS'] = deaths['countyFIPS'].apply(lambda value: '0' + str(value) if len(str(value)) == 4 else str(value))
    deaths = deaths[deaths['County Name'] != 'Statewide Unallocated'].reset_index(drop = True)
    deaths['County Name'] = deaths['County Name']  + ', ' + deaths['State']
    deaths.drop(['12/28/20','12/29/20', '12/30/20', '12/31/20', '1/1/21', '1/2/21'], axis = 1, inplace = True)

    # Converts '\n' value for McDowell County, NC to the same as November and converts random string values to integers in Deaths dataset

    deaths.iloc[1948, -1] = 38

    def str_int(val):
        if type(val) == str:
            return int(val)
        else:
            return val

    deaths.iloc[:, -1] = deaths.iloc[:, -1].apply(str_int)

    # Creates the population dataframe
    
    pop = pd.read_csv(pop_url)
    pop['countyFIPS'] = pop['countyFIPS'].apply(lambda value: '0' + str(value) if len(str(value)) == 4 else str(value))
    pop = pop[pop['County Name'] != 'Statewide Unallocated'].reset_index(drop = True)['population']
    pop = pd.DataFrame(pop).rename(columns = {'population':'Population'})

    # Creates 'dates' as a list of all of the days past

    c_dates = cases.iloc[:,4:].columns.values

    d_dates = deaths.iloc[:,4:].columns.values

    # Defines the function to compile the daily data into monthly data

    def m_compiler(df, c_or_d):
        c_df = df.copy(deep = True)
        
        c_mos = {1:'January Cases', 2:'February Cases', 3:'March Cases', 4:'April Cases', 5:'May Cases', 6:'June Cases', 7:'July Cases', 8:'August Cases', 9:'September Cases', 10:'October Cases', 11:'November Cases', 12:'December Cases'}
        
        d_mos = {1:'January Deaths', 2:'February Deaths', 3:'March Deaths', 4:'April Deaths', 5:'May Deaths', 6:'June Deaths', 7:'July Deaths', 8:'August Deaths', 9:'September Deaths', 10:'October Deaths', 11:'November Deaths', 12:'December Deaths'}
        
        c_mo_ls = list(range(int(c_dates[-1].split('/')[0])))
        
        d_mo_ls = list(range(int(d_dates[-1].split('/')[0])))
        
        if c_or_d == 'c':
            for i in range(int(c_dates[-1].split('/')[0])):
                for date in c_dates:
                    while int(date.split('/')[0]) < i + 2:
                        c_mo_ls.pop(i)
                        c_mo_ls.insert(i,date)
                        break
        
            monthly_df = c_df[c_mo_ls]
        
            c_df.drop(c_df.iloc[:,4:], axis = 1, inplace = True)
        
        elif c_or_d == 'd':
            for i in range(int(d_dates[-1].split('/')[0])):
                for date in d_dates:
                    while int(date.split('/')[0]) < i + 2:
                        d_mo_ls.pop(i)
                        d_mo_ls.insert(i,date)
                        break
        
            monthly_df = c_df[d_mo_ls]
        
            c_df.drop(c_df.iloc[:,4:], axis = 1, inplace = True)
                
        def num_to_mo(cols):
            sing_nums = cols.map(lambda col: int(col.split('/')[0]))
            return sing_nums
        
        monthly_df.columns = num_to_mo(monthly_df.columns)
        
        if c_or_d == 'c':
            monthly_df.columns = monthly_df.columns.map(c_mos)
        
        if c_or_d == 'd':
            monthly_df.columns = monthly_df.columns.map(d_mos)
       
        c_df = pd.concat([c_df, monthly_df], axis = 1)
            
        split1 = c_df.iloc[:,:4]
        split2 = c_df.iloc[:,4:]
                
        for i in range(1,len(split2.columns)):
            split2.iloc[:,-i] = split2.iloc[:,-i] - split2.iloc[:,-i-1]

        c_df = pd.concat([split1, split2], axis = 1)
        
        return c_df
    
    # Cumulative data 
    
    c_mo_us = m_compiler(cases, 'c')
    d_mo_us = m_compiler(deaths, 'd').drop(['countyFIPS', 'County Name', 'State', 'stateFIPS'], axis = 1)

    covid_data = c_mo_us.iloc[:, :4]
    covid_data = pd.concat([covid_data, pop], axis = 1)
    c_mo_us.drop(c_mo_us.iloc[:,:4], axis = 1, inplace = True)
    cd = covid_data.copy(deep = True)

    for i in range(len(c_mo_us.columns)):
        cd = pd.concat([cd, c_mo_us.iloc[:,i:i+1], d_mo_us.iloc[:, i:i+1]], axis = 1)
    
    c_cols = []
    d_cols = []

    for col in cd.columns: 
        col_cont = col.split()
        if len(col_cont) == 2:
            if col_cont[1] == 'Cases':
                c_cols.append(col)
            elif col_cont[1] == 'Deaths': 
                d_cols.append(col)
        
    c_rates = pd.DataFrame()
    d_rates = pd.DataFrame()

    for c_mo in c_cols:
        c_rates[c_mo.split()[0] + ' Infection Rate (per 100,000)'] = round(cd[c_mo]/cd['Population'] * 100000, 2)
    
    for d_mo in d_cols:
        d_rates[d_mo.split()[0] + ' Mortality Rate (per 100,000)'] = round(cd[d_mo]/cd['Population'] * 100000, 2)
    
    for i in range(len(c_mo_us.columns)):
        covid_data = pd.concat([covid_data, c_mo_us.iloc[:,i:i+1], d_mo_us.iloc[:, i:i+1], c_rates.iloc[:, i:i+1], d_rates.iloc[:, i:i+1]], axis = 1)    

    def projector(df, df2, c_or_d):
        mo_days = {1 : 31,
                   2 : (28,29),
                   3 : 31,
                   4 : 30,
                   5 : 31,
                   6: 30,
                   7 : 31,
                   8 : 31,
                   9 : 30,
                   10 : 31,
                   11 : 30,
                   12 : 31
                  }
    
        latest_date = df.columns[-1].split('/')
    
        latest_day = int(latest_date[1])
    
        latest_month = int(latest_date[0])
    
        latest_year = int(latest_date[2])
    
        if latest_month != 2:
            tot_days = [mo_days[val] for val in [latest_month]][0]
        else:
            if latest_year % 4 == 0:
                tot_days = 29
            else:
                tot_days = 28
    
        perc_done = latest_day/tot_days
    
        no_mo = {1:'January',
                 2:'February',
                 3:'March',
                 4:'April',
                 5:'May',
                 6:'June',
                 7:'July',
                 8:'August',
                 9:'September',
                 10:'October',
                 11:'November',
                 12:'December'
                }
        la_mo = [no_mo[val] for val in [latest_month]][0]
    
        if c_or_d == 'c':
            latest_col = df2['{mo} Cases'.format(mo = la_mo)]
            predicted_cases = (latest_col / perc_done).apply(lambda value: int(value))
            predicted_i_r = round(predicted_cases/df2['Population'] * 100000, 2)
            predictions = pd.concat([predicted_cases,predicted_i_r], axis = 1)
            predictions.columns = ['Predicted {mo} Cases'.format(mo = la_mo), 'Predicted {mo} Infection Rate (per 100,000)'.format(mo = la_mo)]
    
            return predictions
        else:
            latest_col = df2['{mo} Deaths'.format(mo = la_mo)]
            predicted_deaths = (latest_col / perc_done).apply(lambda value: int(value))
            predicted_m_r = round(predicted_deaths/df2['Population'] * 100000, 2)
            predictions = pd.concat([predicted_deaths,predicted_m_r], axis = 1)
            predictions.columns = ['Predicted {mo} Deaths'.format(mo = la_mo), 'Predicted {mo} Mortality Rate (per 100,000)'.format(mo = la_mo)]
    
            return predictions
    
    pred_inf = projector(cases, covid_data, 'c')
    pred_dth = projector(deaths, covid_data, 'd')

    covid_data = pd.concat([covid_data, pred_inf, pred_dth], axis = 1)

    covid_data['Cumulative Infection Rate (per 100,000)'] = round(c_rates.mean(axis = 1), 2)
    covid_data['Cumulative Mortality Rate (per 100,000)'] = round(d_rates.mean(axis = 1), 2)
    
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    for month in months:
        covid_data = covid_data.drop([month + ' Cases', month + ' Deaths'], axis = 1)
    
    return covid_data

def combiner():
    
    race_data = create_race_data()
    inc_unemp_data = create_inc_unemp_data()
    edu_data = create_edu_data()
    mask_data = create_mask_data()
    covid_data = create_covid_pop_data()
    
    county_data = pd.merge(covid_data, inc_unemp_data, on = 'County Name')
    county_data = pd.merge(county_data, race_data, on = 'County Name')
    county_data = pd.merge(county_data, edu_data, on = 'County Name')
    county_data = pd.merge(county_data, mask_data, on = 'State')
    
    return county_data

def main_function():

    data = combiner()    
    return data