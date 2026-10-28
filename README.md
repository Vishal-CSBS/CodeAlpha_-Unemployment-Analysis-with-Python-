# Unemployment Analysis in India Using Python

## Project Overview
This project explores unemployment trends across Indian regions using Python, Pandas, Matplotlib, and Seaborn. It includes data cleaning, exploratory data analysis, regional comparisons, rural-versus-urban analysis, and a comparison of unemployment observations across selected periods in 2020.

## Objectives
- Clean and prepare unemployment datasets.
- Analyze unemployment rates over time.
- Compare average unemployment rates across regions.
- Examine differences between rural and urban observations.
- Compare recorded unemployment rates across three periods in 2020.
- Present findings through charts and a CSV summary.

## Technologies Used
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Visual Studio Code

## Project Structure
```text
Unemployment_analysis/
├── Data/
├── outputs/
│   ├── charts/
│   ├── cleaned_data/
│   └── reports/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Key Findings
- Dataset 1 average unemployment rate: 11.79%.
- Dataset 2 average unemployment rate: 12.24%.
- Haryana had the highest regional average in Dataset 2 at 27.48%.
- Meghalaya had the lowest regional average in Dataset 2 at 3.87%.
- In Dataset 2, the highest monthly average was 23.24% in May 2020, while the lowest was 8.03% in October 2020.
- The rural average was 10.32%, compared with 13.17% for urban observations in Dataset 1.
- The average across recorded regional observations was 16.74% for March–June 2020, compared with 9.23% for January–February and 9.22% for July–October.

*Note: These figures are descriptive averages from the supplied datasets. They should not be interpreted as official national unemployment estimates or as proof of causation.*

## How to Run
1. Install Python.
2. Open the project folder in VS Code.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Ensure both original CSV datasets are in the `Data/` folder.
5. Run:

   ```bash
   python main.py
   ```

6. Review the generated charts in `outputs/charts/`, cleaned datasets in `outputs/cleaned_data/`, and the period comparison report in `outputs/reports/`.

## Outputs
- Monthly unemployment trend chart
- Regional unemployment comparison
- COVID-period trend chart
- Rural-versus-urban comparison
- COVID-period comparison chart
- Cleaned CSV datasets
- COVID-period summary CSV

## Limitations
The analysis depends on the supplied datasets, their time coverage, and the regional observations available. Averages across records may not represent population-weighted national unemployment rates. The analysis is descriptive and does not establish causation.
## Interactive Dashboard

This project includes a Streamlit dashboard for exploring unemployment observations across Indian regions.

### Dashboard Features
- Key unemployment statistics
- Monthly unemployment trends
- Regional comparisons
- Rural-versus-urban analysis
- COVID-period comparisons
- Region and date filters
- CSV download for filtered data

### Run the Dashboard

Install the dependencies:

```bash
pip install -r requirements.txt
```

Generate the cleaned datasets:

```bash
python main.py
```

Launch the dashboard:

```bash
python -m streamlit run dashboard.py
```

Open the local URL displayed in the terminal, usually `http://localhost:8501`.


## Author

**Vishal N A**

- GitHub: (https://github.com/Vishal-CSBS)
- Project: Unemployment Analysis with Python