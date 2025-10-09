# 🌏 Earthquake Data Analysis in Japan  
## A Project to Understand Seismic Behavior Using Real Data and Data Science  

---

> 📦 **Project Info**
> - 🐍 Python Version: 3.11+
> - 💾 Database: MySQL (via SQLAlchemy & PyMySQL)
> - 📊 Focus: Earthquake Data Analysis (Japan)
> - 🧠 Core Tools: Pandas, NumPy, Matplotlib, Requests, BeautifulSoup, Selenium
> - 🧰 Environment: Virtualenv (venv)
> - 🕓 Time Range: Last 30 days of earthquakes in Japan
> - 🔍 Data Sources: USGS, GEOFON, EMSC

---

## 🧩 Project Overview  

This project was designed with the goal of **scientifically analyzing recent earthquakes in Japan**.  
Japan is one of the most earthquake-prone countries in the world, with dozens of tremors occurring each month.  
In this project, we aimed to combine multiple global data sources to build a more accurate and data-driven picture of earthquake activity across Japan.  

The project covers every stage — from **collecting raw data** to **final analysis and visualization**.  
The ultimate objective is to answer key questions such as:

- Which regions of Japan are most vulnerable to earthquakes?  
- What patterns exist in earthquake magnitudes across different areas?  
- Is there a correlation between earthquake depth and magnitude?  
- And finally, how has seismic activity changed over the past month?  

---

## 🔬 Workflow and Methodology  

### 1. Data Collection from Global Sources  

Earthquake data was gathered from three main and reliable sources:  

- **USGS:** United States Geological Survey  
- **GEOFON:** German Research Centre for Geosciences  
- **EMSC:** European-Mediterranean Seismological Centre  

To collect this data, a combination of techniques was used:  

- 📡 **USGS API:** Automatically fetched recent earthquake data within a 30-day range  
- 🕸️ **Web Scraping (GEOFON & EMSC):** Extracted tabular data from seismological websites  
- 💾 Finally, all data was saved in `.csv` format for further processing  

---

### 2. Data Cleaning and Preprocessing  

Raw data often contains noise, missing values, and inconsistencies.  
Using **Pandas** and **NumPy**, the following steps were performed:  

- Removed duplicate or missing records  
- Standardized date and time formats  
- Converted text-based numeric values into actual numbers  
- Created new columns such as:  
  - **Month:** To categorize earthquakes by month  
  - **Category:** To classify magnitudes as *Weak*, *Moderate*, or *Strong*  
  - **Region:** Extracted region names from place descriptions (e.g., Tokyo, Honshu, Offshore East Japan)  

---

### 3. Statistical and Mathematical Analysis  

This section focused on uncovering patterns and insights through statistical analysis.  
The following analyses were performed:  

- Calculated average and maximum magnitudes per region  
- Compared depth and magnitude to identify the most dangerous earthquakes  
- Found regions with the highest frequency of earthquakes  
- Observed trends over time (by month, week, or day)  

With **NumPy**, we performed mathematical operations such as calculating means, standard deviations, and the geographical distance between earthquake centers and Tokyo — helping identify risk intensity levels.  

---

### 4. Storing Data in an SQL Database  

To make querying and large-scale analysis faster, the cleaned data was stored in a relational database.  
A table was created with columns like `time`, `latitude`, `longitude`, `depth`, `magnitude`, `region`, and `source`.  
Using **SQLAlchemy** and **PyMySQL**, the processed DataFrame was inserted into the database.  

Here are some example SQL queries used:  

```sql
SELECT region, COUNT(*) FROM earthquakes GROUP BY region;
SELECT region, AVG(magnitude) FROM earthquakes GROUP BY region;
```

### 5. Visualization and Data Presentation  

To make the analysis more intuitive, several types of charts and visualizations were created:  

- 📊 **Bar Charts:** Displayed the number of earthquakes in each region  
- 📈 **Line Charts:** Showed the change in earthquake magnitudes over time  
- ⚪ **Scatter Plots:** Illustrated the relationship between depth and magnitude  
- 🔥 **Heatmaps:** Visualized the spatial distribution of earthquakes across Japan  

These visualizations helped transform raw statistical data into clear and meaningful insights that are easy to understand.

---

### 6. Final Conclusions  

From the analysis, several key findings emerged:  

- Most earthquakes in Japan are concentrated in the **eastern region** near the Pacific Ocean.  
- **Shallow earthquakes** tend to have higher magnitudes and are generally more destructive.  
- The three data sources (USGS, GEOFON, and EMSC) have minor coverage differences, but their overall patterns are consistent.  
- The majority of recent earthquakes occurred around **Honshu** and the **Near East Coast of Japan**.  

---

## 🎯 Project Impact and Applications  

This project can be beneficial for:  

- **Geoscience researchers** — as a reference for seismic data analysis  
- **Data science and computer engineering students** — as a real-world data analysis project  
- **Disaster management and safety organizations** — to study and predict high-risk regions  

The project demonstrates how **open-source tools and real-world data** can be used to analyze a complex natural phenomenon —  
without the need for expensive software or specialized systems.  

---

## ❤️ Summary  

This project is more than just a coding exercise —  
it’s a **journey from raw data to scientific insight.**  

We learned how to collect, clean, analyze, and visualize real data to reach meaningful conclusions.  
Ultimately, the project shows that with programming knowledge and creativity,  
we can turn data into a tool for understanding the world better 🌍





