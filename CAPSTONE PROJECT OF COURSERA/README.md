# SpaceX Falcon 9 Landing Prediction

An end-to-end data science capstone project that investigates Falcon 9 first-stage landing success and compares machine-learning models for predicting whether a launch will land successfully.

## Project overview

This project covers:

- Data collection from the SpaceX REST API
- Web scraping of Falcon 9 launch records from Wikipedia
- Data cleaning, feature engineering, and binary landing-outcome labels
- SQL-based exploratory analysis with SQLite
- Exploratory data visualization with Matplotlib and Seaborn
- Interactive launch-site mapping with Folium
- An interactive Plotly Dash dashboard
- Classification with Logistic Regression, SVM, Decision Tree, and KNN
- Model selection with 10-fold `GridSearchCV`
- A generated PDF presentation/report

## Repository contents

| File | Description |
| --- | --- |
| [`SpaceX_Capstone_Complete.ipynb`](SpaceX_Capstone_Complete.ipynb) | Complete notebook, from data collection through model evaluation |
| [`spacex_dash_app.py`](spacex_dash_app.py) | Plotly Dash application for launch-site and payload analysis |
| [`build_report.py`](build_report.py) | Script that builds the PDF report |
| [`Data_Science_Capstone_Project_Report.pdf`](Data_Science_Capstone_Project_Report.pdf) | Generated project report |

## Main findings

- Landing success improves as flight experience and booster maturity increase.
- Launch site, orbit, payload mass, and booster version are useful predictors.
- Geostationary Transfer Orbit (GTO) has a lower success rate than several other orbits.
- The Decision Tree achieved the strongest cross-validation result among the tested models.
- The tested models reached approximately 83.33% accuracy on the held-out test set.
- KSC LC-39A shows a high landing-success rate in the analyzed data.

## Technologies

- Python
- Jupyter Notebook
- Pandas and NumPy
- Requests and BeautifulSoup
- SQLite and PrettyTable
- Matplotlib and Seaborn
- Folium
- Plotly and Dash
- Scikit-learn
- ReportLab

## Setup

Create and activate a virtual environment, then install the libraries used by the notebook and dashboard:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install jupyter pandas numpy requests beautifulsoup4 matplotlib seaborn scikit-learn folium plotly dash prettytable reportlab
```

## Run the notebook

Start Jupyter from the repository directory:

```powershell
jupyter notebook
```

Open `SpaceX_Capstone_Complete.ipynb` and run the cells in order. The notebook retrieves the capstone datasets from the referenced IBM Skills Network and SpaceX/Wikipedia sources, performs the analysis, and displays the visualizations and model results.

## Run the Dash dashboard

The dashboard reads a file named `spacex_launch_dash.csv` from the repository directory. Place that dataset beside `spacex_dash_app.py` before starting the app.

```powershell
python spacex_dash_app.py
```

Then open <http://127.0.0.1:8050/> in a browser. The dashboard provides:

- A launch-site dropdown
- A success pie chart
- A payload-range slider
- A payload-versus-outcome scatter chart

## Build the PDF report

The report builder can include optional screenshots from a `screenshots` folder. If a screenshot is not provided, the script inserts a labelled placeholder.

Before building, update the `GITHUB` and author placeholders in `build_report.py` if you want the generated PDF to contain your repository URL and name.

```powershell
python build_report.py
```

This regenerates `Data_Science_Capstone_Project_Report.pdf`.

## Data sources

- SpaceX REST API: <https://api.spacexdata.com/v4/launches/past>
- Wikipedia launch-history snapshot referenced by the notebook: <https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches>
- IBM Skills Network datasets used by the Coursera labs

Dataset availability and external URLs may change over time. Review the notebook cells for the exact URLs and transformations used in this project.

## Author

**Your Name**

Replace the placeholder above with your name and add your GitHub profile link when publishing the repository.
