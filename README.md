# COVID_Data

A detailed, county-level dataset with data relating to the COVID-19 pandemic. Read more about the data and some analysis I performed here: https://medium.com/@kabirmoghe/county-based-covid-19-dataset-and-analytical-trends-ff1617030ba8. 

Above, you can access the code that creates and compiles the dataset, as well as the COVID-19 dataset as of 10/7/2020, and some of the county-level stats used to make the full dataset.

The dataset itself includes new cases each month, denoted by the names of the months (Janurary Cases, February Cases, etc.), new deaths each month (January Deaths, etc.), features about the county itself (population, population density, race demographics, median household income, unemployment, and a measure of education), and a form of government intervention (the presence of a mandatory mask requirement). The dataset also has FIP codes of counties and states, making it easy to create maps and charts. 

The data about county-level statistics (i.e. population density), ”stat_data.csv”, comes from the US Census website and has been cut down to only a few important attributes; download the full file here: https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/asrh/cc-est2019-alldata.csv.

The education data is from USDA and can be downloaded here: https://www.ers.usda.gov/webdocs/DataFiles/48747/Education.xls?v=6188.1.
