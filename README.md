# How is the UKs energy provision changing over time?
Data Science in Economics (BEE2041_A_2_202526) Empirical Project.

## Table of contents:
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

An [easy to view version](https://miriam-meeks.github.io/Data-Science-Empirical-Project/site/blog-uk-energy.html) is checked in and available via GitHub pages.

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

```bash
.
├── README.md
├── Makefile
├── csv-raw/
│   ├── electricity-generated.csv          # Raw data sheets in CSV format
│   ├── monthly-energy-generation.csv
│   ├── net-imports.csv
│   ├── share-electricity-generated.csv
│   └── uk-fuel-consption.csv
├── csv-reshaped/
│   ├── electricity-generated-long.csv     # Reshaped, manipulated CSV ready for visualising
│   ├── net-imports-long.csv
│   └── share-electricity-generated-long.csv
├── python/
│   ├── electricity-generated.py           # Main bulk of data wrangling and visualising
│   ├── trade-balance.py
│   ├── fuel-usage.py
│   ├── web-scrape.py                      # Includes topic 5 web scrape
│   └── blog.py                            # Script for creating HTML blog
└── site/
    ├── index.html                         # Index page that blog is accessible from
    └── blog-uk-energy.html                # Locally hosted blog on UK energy
    └── Visualisations/                    #Saved outputs (gifs and html visuals)
```
All raw data (in csv format) lives in `csv-raw/`. All python scripts, including the one that creates a blog is in `python/` and all output is exported to `Visualisations`. It is important to understand that for the blog to have the most up-to-date visualisations, **all other python scripts must be run before running blog.py** -as made clear in the makefile. To access the blog open the site folder and follow the link in the index.html or go directly to the blog-uk-energy-html page by following the hyperlink in the folder.


## Requirements
System

Python version 3 (tested on Python 3.14.3, Linux)

`make` (optional but recommended)

Must be able to host locally html blog.

Python Packages

Install all dependedcies via pip:

```bash
pip install pandas==3.0.2 matplotlib==3.10.8 plotly==6.6.0 numpy==2.4.4 selenium==4.43.0
```

Or install without pinned versions (results may differ slightly):

```bash
pip install pandas matplotlib plotly numpy selenium
```

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

```bash
make
```
This will automatically:

Run the Python scripts and re-create the blog (if outputs are out of date).

Option B: Manual steps

If `make` is not available, run the following steps in order:

**1. Run the Python scripts:**

```bash
Python 3  electricity-generated.py
    trade-balance.py
    fuel-usage.py
    web-scrape.py
```

This will update the webscrape and outputs in the `Visualisations` folder.

**2. Subsequently run the Python script**

```bash
blog.py 
```

**3. Open the blog**

Open the site folder and follow the link in the index folder to get to the HTML blog (locally hosted) or just open site/blog-uk-energy.html

```bash
site/
    index.html
    blog-uk-energy.html
```

I have also checked in the generated site which you can view below in GitHub pages:

https://miriam-meeks.github.io/Data-Science-Empirical-Project/site/blog-uk-energy.html

## Outputs
Figures (results/figures/)

|File | Description|
|-----|------------|
|`annual-renewable-generation.gif`| Animated line graph showing renewable energy (solar and wind) generation in GWhs between 1997 and 2024 |
|`monthly-mpps-renewable-generation.gif`| Animated monthly renewable (solar and wind) TWh generation for Major Power Producers (MPPs) showing seasonal trends |
|`monthly-wind-generation.html`|Interactive, hover and zoom graph to show monthly wind generation TWh in the UK since 2007|
|`combined_energy_pie_charts.html`|Aggregated hover pie charts to show average energy generation mix between time periods over the past two decades|
|`trade-balance-animation.gif`|Trade balance animation of energy imports/exports for the UK between 2017 and 2024|
|`fuel-consumption-line.html`|Hover line graph for UK Road Transport Fuel Consumption between 1970 and 2024|
|`scraped-generation-mix.html`|Scraped current/ up-to-date hover pie chart with data on energy generation mix|

## Methods
Web scraped relevant data off the website https://grid.iamkate.com/ and using the package selinium in the process. With this data I then created an interactive pie chart to show the current days energy generation mix. 

This is scrapable data (off a free GitHub: given to the public domain) and is correctly referenced on the blog and in the references section of this ReadME.

To create my blog post I used a python script, which generates the blog post and saves it locally in a file, that is accessible through the site folder.
One of the reasons I did this was so that when this repository is used and the make file is run the whole blog post will be recreated, with the up-to-date web scraped data and visualisations adjusted, while being available locally it is not available for anyone online to find.

Note: The web-scrape script should be run before running the blog script for the scraped pie chart visualisation to correctly update.

## References and Resources
**Data:**

- Digest of UK Energy Statistics (DUKES) – Electricity (Chapter 5):

https://www.gov.uk/government/statistics/electricity-chapter-5-digest-of-united-kingdom-energy-statistics-dukes

- Energy Consumption in the UK (ECUK) 2025:

https://www.gov.uk/government/statistics/energy-consumption-in-the-uk-2025

- Energy Trends – Electricity (Section 5):

https://www.gov.uk/government/statistics/electricity-section-5-energy-trends

**In Text:**

Compare Your Footprint. (n.d.). *Wind vs solar: Which green energy is winning?* 

https://www.compareyourfootprint.com/wind-vs-solar-green-energy-winning/

Reuters. (2026, March 31). *Record wind output helps shield UK from worst Iran war fallout.* 

https://www.reuters.com/business/energy/record-wind-output-helps-shield-uk-worst-iran-war-fallout-2026-03-31/

Business Energy Deals. (n.d.). *Wind farms in the UK.* 

https://www.businessenergydeals.co.uk/blog/wind-farms-in-the-uk/

Renewables Now. (n.d.). *Great Britain sets new wind generation record.* 

https://renewablesnow.com/news/great-britain-sets-new-wind-generation-record-1292116/

MacTech. (n.d.). *Why Britain’s nuclear future runs through France.* 

https://mactech.co.uk/why-britains-nuclear-future-runs-through-france/

National Audit Office. (n.d.). *Sizewell C.* https://www.nao.org.uk/work-in-progress/sizewell-c/

Electric Insights. (n.d.). *Electric Insights report.* https://reports.electricinsights.co.uk/?p=1740

Energy UK. (n.d.). *The power of partnership: UK-EU energy cooperation for a clean, secure future.* 

https://www.energy-uk.org.uk/insights/the-power-of-partnership-uk-eu-energy-cooperation-for-a-clean-secure-future/

UK Government. (2024). *National Travel Survey 2024: Household car availability and trends in car trips.* 

https://www.gov.uk/government/statistics/national-travel-survey-2024/nts-2024-household-car-availability-and-trends-in-car-trips

BBC News. (n.d.). *News article.* https://www.bbc.co.uk/news/articles/cvgk3qgkz41o

Scrape: 

https://grid.iamkate.com/ by Kate Morley. Contains BMRS data © Elexon Limited (2026) and data from the National Energy System Operator and Carbon Intensity API.
