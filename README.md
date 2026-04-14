# Data-Science-Empirical-Project
Data Science in Economics (BEE2041_A_2_202526) Empirical Project.

Table of contents: MAKE HYPERLINKS
1.	url
2.	url
3.	url
4.	Requirements
5.	Running Instructions
6.	Outputs
7.	Methods?
8.	References and Resources

[Overview:](url)
This project aims to understand more about energy, generation and provision within the UK and how it is changing overtime.
I have used multiple datasets and techniques to adequately visualise interesting things.
I have also used a Web scrape to find and import interesting and current information for this project.

[Data:](url)
The published materials came as Excel worksheets, which I converted to csv and can be found in this repository. 
Note that although the original imported Excel spreadsheets of the dataset are in the repository (folder: Raw Data Sources) I have used the converted csv’s in my code instead, the Excel spreadsheets are purely there for optional independent further investigation with the other worksheets.
I read them directly using pandas and the key variables shown in the project are listed below: [share-electricity-generated.csv]
Dataset: Electricity_Generation_DUKES_5.6.xlsx  [electricity-generated.csv]
Variable	Description
Total renewable generation	Includes offshore and onshore wind generation, shoreline wave and tidal generation, solar generation and thermal renewable (bioenergy) generation.
Total wind	Wind (fuel) used in generation GWh
The fuel used is assumed the same as the electricity generated.
Total Solar	Solar (fuel) used in generation GWh
The fuel used is assumed the same as the electricity generated.
Dataset: monthly-energy-generation.csv
Variable	Description
Total Electricity (MPPs)	Electricity production from the Main Power Producers [MPPs], across fuels in TWh.
Total Wind	Major Power Producers (onshore and offshore) wind provision TWh
Total Solar	Major Power Producers solar provision TWh.
Dataset: ECUK_2025_Consumption_tables.xlsx [uk-fuel-consumption.csv]
Variable	Description
Fuel consumption	UK, all road transport energy consumption annually (million tonnes).
Dataset: Net_Imports_DUKES_5.13.xlsx [net-imports.csv]
Variable	Description
Import	(Foreign country to UK trade direction). What the UK takes from the specified country.
Export	(UK to Foreign country trade direction). What the UK gives to the specified country.

[Repository structure:](url)
Requirements:
System
Python version 3 (tested on Python 3.14.3, Linux)
Make (optional but recommended)
Web scrape option?

Python Packages



The exact versions to produce the original results are listed below:
Package	Version
pandas	3.0.2
matplotlib	3.10.8
plotly	6.6.0
numpy	2.4.4
selenium	4.43.0

Running Instructions:
Outputs:
Figures ()
Methods – Do I need to include this for a webscrape (maybe write a line).

To create my blog post I used a python script, which generates the blog post and saves it locally in a file, that is accessible……………………………..VIA WHAT?
One of the reasons I did this was so that when this repository is used and the make file is run the whole blog post will be recreated, with the up-to-date web scraped data and visualisations adjusted.

References and Resources:
Datasets, I am Kate, referenced text.
