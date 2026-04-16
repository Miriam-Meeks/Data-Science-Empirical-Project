# How is the UKs energy provision changing over time?
Data Science in Economics (BEE2041_A_2_202526) Empirical Project.

Table of contents:
1.	[Overview](#overview)
2.	[Data](#data)
3.	[Repository Structure](#repository-structure)
4.	[Requirements](#requirements)
5.	[Running Instructions:](#running-instructions)
6.	[Outputs](#outputs)
7.	[Methods](#methods)
8.	[References and Resources:](#references-and-resources)

## Overview
This project aims to understand more about energy, generation and provision within the UK and how it is changing overtime.
I have used multiple datasets and techniques to adequately visualise changes of interest.
I have also used a Web scrape to find and import current information for this project from the site of inspiration https://grid.iamkate.com/ 

## Data
Datasets used came from Digest of UK Energy Statistics (DUKES) and Accredited official statistics - both reliable UK Government sources
The published materials came as Excel worksheets, which I converted to csv formats and can be found in this repository.
Note that although the original imported Excel spreadsheets of the dataset are in the repository (folder: Raw Data Sources) I have used the converted csv’s in my code instead, the Excel spreadsheets are purely there for optional independent further investigation with the other worksheets.

I read them directly using pandas and the key variables shown in the project are listed below: 

Dataset: Electricity_Generation_DUKES_5.6.xlsx  [electricity-generated.csv], [share-electricity-generated.csv]
| Variable                      | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| Total renewable generation    | Includes offshore and onshore wind generation, shoreline wave and tidal generation, solar generation and thermal renewable (bioenergy) generation. |
| Total wind                    | Wind (fuel) used in generation GWh. The fuel used is assumed the same as the electricity generated. |
| Total Solar                   | Solar (fuel) used in generation GWh. The fuel used is assumed the same as the electricity generated. |


Dataset: ET_5.4_MAR_26.xlsx [monthly-energy-generation.csv]
| Variable                    | Description                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| Total Electricity (MPPs)    | Electricity production from the Main Power Producers (MPPs), across fuels in TWh. |
| Total Wind                  | Major Power Producers (onshore and offshore) wind provision TWh.           |
| Total Solar                 | Major Power Producers solar provision TWh.                                 |


Dataset: ECUK_2025_Consumption_tables.xlsx [uk-fuel-consumption.csv]
| Variable            | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| Fuel consumption    | UK, all road transport energy consumption annually (million tonnes).       |


Dataset: Net_Imports_DUKES_5.13.xlsx [net-imports.csv]
| Variable | Description |
|----------|-------------|
| Import   | (Foreign country to UK trade direction). What the UK takes from the specified country. |
| Export   | (UK to Foreign country trade direction). What the UK gives to the specified country. |

## Repository Structure





## Requirements
System
Python version 3 (tested on Python 3.14.3, Linux)
`make` (optional but recommended)
Must be able to host locally html blog.

Python Packages
Install the dependedcies via pip:

```bash
pip install pandas==3.0.2 matplotlib==3.10.8 plotly==6.6.0 numpy==2.4.4 selenium==4.43.0 ```

Or install without pinned versions (results may differ slightly):

```bash
pip install pandas matplotlib plotly numpy selenium```

The exact versions to produce the original results are listed below:
| Package      | Version|
|--------------|--------|
| `pandas`     | 3.0.2  |
| `matplotlib` | 3.10.8 |
| `plotly`     | 6.6.0  |
| `numpy`      | 2.4.4  |
| `selenium`   | 4.43.0 |

## Running Instructions
Option A: Using make (recommended)
If make is available, simply run from the top level of the repository:
`make`

## Outputs
Figures ()
## Methods
Do I need to include this for a webscrape (maybe write a line).

To create my blog post I used a python script, which generates the blog post and saves it locally in a file, that is accessible……………………………..VIA WHAT?
One of the reasons I did this was so that when this repository is used and the make file is run the whole blog post will be recreated, with the up-to-date web scraped data and visualisations adjusted.

## References and Resources
Datasets, I am Kate, referenced text.
