# Educated in Helsinki

**A study on Helsinki's service availability and its impact on the demographics of different residential areas**

## [Google Colab](https://colab.research.google.com/drive/1WUox39VmuAN5vDv_pO2UcNvELQzXJMF3?usp=sharing)

## Project Description

This project analyzes how the availability of various services in Helsinki’s neighborhoods correlates with the demographics, focusing on attracting and retaining highly educated and high-income residents. It combines datasets on education, income, population, and service distribution to provide insights for urban development and strategic planning.

## Getting Started

1. **Prepare data files:**  

   Place the following files in your working directory or update file paths accordingly:  
   - `asuntokuntien_koulutus.xlsx` — Education data by household in Helsinki
   - `asuntokuntien_tulot.xlsx`— Income data by household
   - `väkiluku_aluettain.xlsx`— Population data by area
   - `Helsinki_alueittain_2019.xlsx`— Service availability data by area
   - `finland-postal-codes.geojson`— GeoJSON file with Helsinki postal code boundaries

3. **Install dependencies:**  
   ```bash
   pip install pandas matplotlib plotly folium numpy

4. **Run the code:**

   The script loads and processes data, then creates visualizations including scatter plots, bar charts, and interactive maps to analyze Helsinki’s demographics, services, and employment.

5. **Adjust paths if needed:**

   Modify the file paths at the beginning of the code to match your environment.

## Analysis Overview

* Extract education and income data from Excel headers and calculate total educated population and average/median salaries by region.
* Calculate the percentage of educated residents relative to population in each area.
* Visualize median income vs. number and percentage of educated residents using interactive scatter plots with Plotly.
* Calculate services per person in postal code areas.
* Create choropleth maps using Folium to visualize service availability per capita by postal code.
* Analyze selected districts with bar charts for various service types such as daycare capacity, playgrounds, recreational facilities, stores, pharmacies, and alcohol stores per capita.
* Visualize employment sector distribution across selected districts with stacked bar charts.

## Author: AnastasiiaX
