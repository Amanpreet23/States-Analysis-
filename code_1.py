import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Loading data from csv file
df = pd.read_csv("STATES.csv", encoding='latin1')

# Drop null values and duplicates
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

# Cohort analysis
cohort_years = [1960, 1970, 1980]  # List of cohort years
cohort_analysis = []

# Perform cohort analysis
for year in cohort_years:
    cohort_data = df[df['Year'] == year]  # Subset data for the cohort year
    
    # Clean 'Population Density' column and convert to numeric
    cohort_data['Population Density'] = cohort_data['Population Density'].str.replace('[^\d.]', '', regex=True).astype(float)
    
    avg_density = cohort_data['Population Density'].mean()
    avg_literacy = cohort_data['Literacy Rate%'].mean()

    cohort_analysis.append({'Cohort Year': year,
                            'Avg Population Density': avg_density,
                            'Avg Literacy Rate': avg_literacy})

# Convert cohort analysis to a DataFrame
cohort_df = pd.DataFrame(cohort_analysis)

# Visualize cohort analysis
plt.figure(figsize=(10, 6))
plt.plot(cohort_df['Cohort Year'], cohort_df['Avg Population Density'], marker='o', label='Population Density')
plt.plot(cohort_df['Cohort Year'], cohort_df['Avg Literacy Rate'], marker='o', label='Literacy Rate')
plt.xlabel('Cohort Year')
plt.ylabel('Average')
plt.title('Cohort Analysis: Population Density and Literacy Rate')
plt.legend()
plt.grid()
plt.show()

fig1 = px.bar(df, x='State', y='Sex Ratio', title='Population by State')
fig2 = px.scatter(df, x='Population Density', y='Literacy Rate%', title='Population Density vs. Literacy Rate')
fig3 = px.histogram(df, x='Urban Pop.', nbins=20, title='Urban Population Distribution')
fig4 = px.box(df, x='Year', y='Sex Ratio', title='Sex Ratio by Year')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("States Analysis"),
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3),
    dcc.Graph(figure=fig4)
])

if __name__ == '__main__':
    app.run_server(debug=True)
