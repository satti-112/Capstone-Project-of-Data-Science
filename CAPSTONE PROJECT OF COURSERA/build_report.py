"""Builds Data_Science_Capstone_Project_Report.pdf (landscape slides).
Put your screenshots in ./screenshots/ using the file names listed in SLOTS below (png/jpg);
any missing screenshot shows as a dashed placeholder box. Then run: python build_report.py"""
import os
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader, simpleSplit

GITHUB = "<PASTE YOUR GITHUB REPO URL HERE>"   # <-- edit
NB = GITHUB + "/blob/main/SpaceX_Capstone_Complete.ipynb"
W, H = landscape(A4)
NAVY, BLUE, GREY = colors.HexColor("#0b2447"), colors.HexColor("#19376d"), colors.HexColor("#555555")
c = canvas.Canvas("Data_Science_Capstone_Project_Report.pdf", pagesize=(W, H))
c.setTitle("Data Science Capstone Project Report – SpaceX Falcon 9 Landing Prediction")
page = [0]

def find_img(key):
    for ext in ("png", "jpg", "jpeg"):
        p = f"screenshots/{key}.{ext}"
        if os.path.exists(p): return p

def slide(title):
    if page[0]: c.showPage()
    page[0] += 1
    c.setFillColor(NAVY); c.rect(0, H - 60, W, 60, fill=1, stroke=0)
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 22); c.drawString(30, H - 40, title)
    c.setFillColor(GREY); c.setFont("Helvetica", 8); c.drawRightString(W - 30, 15, f"Data Science Capstone  |  {page[0]}")
    return H - 90

def text(y, lines, x=30, size=12, width=None, bullet=True, font="Helvetica"):
    width = width or (W - x - 30)
    c.setFillColor(colors.black); c.setFont(font, size)
    for ln in lines:
        wrapped = simpleSplit(("• " if bullet else "") + ln, font, size, width)
        for j, w in enumerate(wrapped):
            c.drawString(x + (0 if j == 0 or not bullet else 10), y, w); y -= size + 4
        y -= 3
    return y

def link(y, label="GitHub URL:", url=None):
    c.setFillColor(BLUE); c.setFont("Helvetica-Bold", 10); c.drawString(30, y, label)
    c.setFont("Helvetica", 10); c.drawString(100, y, url or NB)

def slot(key, label, x, y, w, h):
    p = find_img(key)
    if p:
        img = ImageReader(p); iw, ih = img.getSize(); s = min(w / iw, h / ih)
        c.drawImage(img, x + (w - iw * s) / 2, y + (h - ih * s) / 2, iw * s, ih * s)
    else:
        c.setStrokeColor(colors.HexColor("#999999")); c.setDash(4, 3); c.rect(x, y, w, h); c.setDash()
        c.setFillColor(GREY); c.setFont("Helvetica-Oblique", 10)
        c.drawCentredString(x + w / 2, y + h / 2 + 6, "Insert screenshot:"); c.drawCentredString(x + w / 2, y + h / 2 - 8, label)
        c.setFont("Helvetica", 8); c.drawCentredString(x + w / 2, y + h / 2 - 22, f"screenshots/{key}.png")

def flow(y, steps):
    n = len(steps); bw = (W - 60 - (n - 1) * 22) / n
    for i, s in enumerate(steps):
        x = 30 + i * (bw + 22)
        c.setFillColor(colors.HexColor("#e8eefc")); c.setStrokeColor(BLUE); c.roundRect(x, y - 60, bw, 60, 6, fill=1)
        c.setFillColor(colors.black); c.setFont("Helvetica", 9)
        for k, w in enumerate(simpleSplit(s, "Helvetica", 9, bw - 8)[:4]): c.drawCentredString(x + bw / 2, y - 16 - k * 11, w)
        if i < n - 1:
            c.setStrokeColor(BLUE); c.line(x + bw, y - 30, x + bw + 18, y - 30)
            c.setFillColor(BLUE); p = c.beginPath(); p.moveTo(x + bw + 18, y - 30); p.lineTo(x + bw + 12, y - 26); p.lineTo(x + bw + 12, y - 34); p.close(); c.drawPath(p, fill=1)
    return y - 80

# 1 Title
y = slide("Data Science Capstone Project Report")
y = text(y - 20, ["SpaceX Falcon 9 First Stage Landing Prediction"], size=22, bullet=False, font="Helvetica-Bold")
y = text(y - 10, ["End-to-end: data collection, wrangling, SQL & visual EDA, Folium, Plotly Dash, and machine learning classification"], size=13, bullet=False)
y = text(y - 30, ["Author: <YOUR NAME>", "Date: November 2026", f"GitHub: {GITHUB}"], size=13, bullet=False)

# 2 Executive Summary
y = slide("Executive Summary")
text(y, ["Problem: predict whether the Falcon 9 first stage lands successfully, because reuse is what lets SpaceX charge ~$62M versus $165M+ for competitors.",
 "Methods: SpaceX REST API + Wikipedia web scraping; data wrangling and Class labelling; SQL (SQLite) and Matplotlib/Seaborn EDA; Folium maps; Plotly Dash dashboard; Logistic Regression, SVM, Decision Tree and KNN tuned with 10-fold GridSearchCV.",
 "Key results: landing success rises with flight number and booster maturity (FT, Block 5); orbit, payload and launch site matter; KSC LC-39A has the most and the highest-rate successes.",
 "Models: all four reach 83.33% test accuracy (15/18); Decision Tree has the best cross-validation score. Errors are false positives (3), no false negatives."], size=13)

# 3 Introduction
y = slide("Introduction")
text(y, ["Project background: SpaceX reuses the Falcon 9 first stage, which drives its price advantage.",
 "Problem statement: given launch features (flight number, payload mass, orbit, launch site, booster hardware), predict landing success (Class = 1) or failure (Class = 0).",
 "Why it matters: a bidder competing with SpaceX can estimate launch cost if it can predict whether the booster will be reused.",
 "Questions answered: Which features drive success? Which sites, orbits, payload ranges and boosters perform best? Which classifier predicts best?"], size=13)

# 4 API
y = slide("Data Collection – SpaceX API")
y = flow(y - 10, ["GET api.spacexdata.com /v4/launches/past", "json_normalize to DataFrame", "Keep single-core, single-payload launches; date ≤ 2020-11-13", "Call rockets / launchpads / payloads / cores endpoints", "Drop Falcon 1; fill PayloadMass NaN with mean", "Export dataset_part_1.csv"])
y = text(y - 10, ["Key phrases: requests.get(), pd.json_normalize(), helper functions getBoosterVersion / getLaunchSite / getPayloadData / getCoreData."], size=12)
link(60, url=NB + "  (Part 1)")

# 5 Scraping
y = slide("Data Collection – Web Scraping")
y = flow(y - 10, ["requests.get() Wikipedia 'List of Falcon 9 and Falcon Heavy launches' (9 Jun 2021 snapshot)", "BeautifulSoup parse HTML", "Find wikitable tables; extract column headers", "Loop rows; parse flight no., date, booster, site, payload, orbit, outcome", "Build DataFrame", "Export spacex_web_scraped.csv"])
y = text(y - 10, ["Key phrases: BeautifulSoup, find_all('table'), extract_column_from_header(), launch_dict, to_csv()."], size=12)
link(60, url=NB + "  (Part 2)")

# 6 Wrangling
y = slide("Data Wrangling Methodology")
y = text(y, ["Profiled missing values (isnull) and data types.", "Counted launches per LaunchSite and per Orbit (value_counts).", "Counted landing Outcome categories; True Ocean / RTLS / ASDS = success.",
 "Created binary Class: 0 for bad outcomes (False Ocean/RTLS/ASDS, None ASDS, None None), 1 otherwise.", "Computed baseline success rate with df['Class'].mean(); exported dataset_part_2.csv."], size=13)
link(60, url=NB + "  (Part 3)")

# 7 EDA viz summary
y = slide("EDA with Data Visualization")
y = text(y, ["Charts used: catplot scatter (Flight Number / Payload vs Launch Site and Orbit), bar chart (success rate by orbit), line chart (yearly success trend).",
 "Purpose: scatter plots show how flight experience and payload relate to landing; the bar chart ranks orbits; the line chart shows improvement over time.",
 "Feature engineering: selected 12 predictors; one-hot encoded Orbit, LaunchSite, LandingPad, Serial → 80 numeric columns (dataset_part_3.csv)."], size=13)
link(60, url=NB + "  (Part 5)")

# 8 EDA viz results
y = slide("EDA with Visualization – Results")
slot("eda_flight_site", "Flight Number vs Launch Site", 30, 250, 250, 230); slot("eda_payload_site", "Payload vs Launch Site", 295, 250, 250, 230); slot("eda_orbit_bar", "Success rate by orbit", 560, 250, 250, 230)
slot("eda_year_line", "Yearly success trend", 30, 20, 250, 220)
text(235, ["Success improves as flight number grows at every site.", "ES-L1, GEO, HEO, SSO reach 100%; GTO is lower (~52%).", "Average success rises from 2013 to 2020, sharply after 2015."], x=295, size=11, width=520)

# 9 SQL summary
y = slide("EDA with SQL")
y = text(y, ["Loaded Spacex.csv into SQLite table SPACEXTABLE (rows with null Date removed) and ran 10 queries via ipython-sql (%sql).",
 "Topics: unique launch sites, CCA% filter, NASA (CRS) payload total, F9 v1.1 average payload, first ground-pad landing, drone-ship successes by payload, mission outcomes, max-payload boosters (subquery), 2015 drone-ship failures by month, ranked landing outcomes 2010-06-04 → 2017-03-20."], size=13)
link(60, url=NB + "  (Part 4)")

# 10 SQL results
y = slide("EDA with SQL – Results")
rows = [("Unique launch sites", "CCAFS LC-40, VAFB SLC-4E, KSC LC-39A, CCAFS SLC-40"), ("Total payload, NASA (CRS)", "45,596 kg"), ("Avg payload, F9 v1.1", "2,928 kg"),
 ("First ground-pad success", "2015-12-22"), ("Max payload (15,600 kg)", "Starlink boosters, F9 B5 variants"), ("Ranked outcomes", "No attempt, Success (drone ship), Failure (drone ship) lead the 2010-2017 window")]
for r in rows:
    y = text(y, [f"{r[0]}: {r[1]}"], size=12)
slot("sql_results", "Screenshot of SQL query outputs (Tasks 1-10)", 30, 20, W - 60, 200)

# 11 Folium summary
y = slide("Interactive Visual Analytics – Folium & Plotly Dash")
y = text(y, ["Folium map: launch-site circles and labels, MarkerCluster of success (green) / failure (red) launches, MousePosition + haversine distances with PolyLines to coast, railway, highway and city.",
 "Plotly Dash app: site dropdown, 0-10,000 kg payload RangeSlider, success pie chart and payload-vs-outcome scatter coloured by booster version category."], size=13)
link(y - 10, label="Folium:", url=NB + "  (Part 6)"); link(y - 28, label="Dash:", url=GITHUB + "/blob/main/spacex_dash_app.py")

# 12 Folium results
y = slide("Folium Map – Results")
slot("folium_sites", "All launch sites on map", 30, 260, 250, 220); slot("folium_markers", "Success/failure markers", 295, 260, 250, 220); slot("folium_distance", "Distance lines to proximities", 560, 260, 250, 220)
text(250, ["Sites are near the equator-side coast and on the coastline (safe ocean trajectories).", "Close to railways/highways for logistics; far from dense cities for safety."], size=12)

# 13/14 Dash
y = slide("Plotly Dash – Success Pie Charts")
slot("dash_pie_all", "Pie chart: all sites", 30, 150, 380, 330); slot("dash_pie_best", "Pie chart: highest-success site (KSC LC-39A)", 430, 150, 380, 330)
text(130, ["KSC LC-39A has the largest share of successful launches (41.7%) and the highest success rate (~76.9%)."], size=12)
y = slide("Plotly Dash – Payload vs Launch Outcome")
slot("dash_scatter_all", "Scatter: all sites, full payload range", 30, 150, 380, 330); slot("dash_scatter_range", "Scatter: selected payload range", 430, 150, 380, 330)
text(130, ["Mid-weight payloads (~2,000-5,000 kg) show most successes; FT and B5 boosters succeed most often. Confirm ranges on your dashboard."], size=12)

# 15 ML
y = slide("Predictive Analysis")
y = text(y, ["Standardised X (StandardScaler); 80/20 split (72 train / 18 test, random_state=2); 10-fold GridSearchCV."], size=12)
hdr = ["Model", "Best hyperparameters", "CV acc.", "Test acc."]
data = [("Logistic Regression", "C=0.01, l2, lbfgs", "84.64%", "83.33%"), ("SVM", "sigmoid, C=1, gamma=0.0316", "84.82%", "83.33%"), ("Decision Tree", "tuned depth/leaf/criterion", "~87.5-88.9%", "83.33%"), ("KNN", "n=10, p=1, auto", "84.82%", "83.33%")]
xs = [30, 190, 440, 540]; yy = y - 6
c.setFont("Helvetica-Bold", 11)
for x, h in zip(xs, hdr): c.drawString(x, yy, h)
c.setFont("Helvetica", 11)
for r in data:
    yy -= 16
    for x, v in zip(xs, r): c.drawString(x, yy, v)
slot("ml_confusion", "Confusion matrices (all 4 models)", 30, 20, 380, 210)
text(220, ["Best model: Decision Tree (highest CV score); all models tie on test accuracy.", "Confusion matrix: 12 TP, 3 TN, 3 FP, 0 FN.", "Main error: predicting a landing that does not happen."], x=430, size=11, width=380)
link(8, url=NB + "  (Part 8)")

# 16 Conclusion
y = slide("Conclusion & Insights")
text(y, ["Landing success grew with flight experience and hardware maturity (FT → Block 5).", "Orbit, payload mass and launch site are strong predictors; GTO is the riskiest orbit.",
 "Decision Tree is the best validated model; all four tie at 83.33% test accuracy, so the 18-sample test set is a limiting factor.",
 "Innovation ideas: add weather/sea-state and landing-pad data, use ensembles (Random Forest / Gradient Boosting), and use repeated cross-validation for a more reliable comparison.",
 "Business value: a predicted landing probability lets a bidder estimate SpaceX's cost advantage per launch."], size=13)
c.showPage(); c.save(); print("pages:", page[0])
