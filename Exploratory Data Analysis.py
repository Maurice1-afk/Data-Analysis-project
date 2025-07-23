import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px  # Optional for interactive visualizations

# Load the dataset
df = pd.read_csv('owid-covid-data.csv')

# Initial exploration
print("Dataset shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst 5 rows:")
display(df.head())
print("\nMissing values summary:")
display(df.isnull().sum().sort_values(ascending=False).head(20))

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Select countries of interest (customize as needed)
countries = ['United States', 'India', 'Brazil', 'United Kingdom', 'Kenya', 'South Africa']
df_filtered = df[df['location'].isin(countries)].copy()

# Handle missing values for key columns
key_columns = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths', 
               'total_vaccinations', 'people_vaccinated', 'population']
               
for col in key_columns:
    df_filtered[col] = df_filtered[col].fillna(0)  # Or use interpolation if appropriate
    
# Calculate derived metrics
df_filtered['death_rate'] = df_filtered['total_deaths'] / df_filtered['total_cases']
df_filtered['vaccination_rate'] = df_filtered['people_vaccinated'] / df_filtered['population']

# Set visualization style
sns.set_style('whitegrid')
plt.figure(figsize=(12, 6))

# Plot total cases over time
plt.figure(figsize=(14, 7))
for country in countries:
    country_data = df_filtered[df_filtered['location'] == country]
    plt.plot(country_data['date'], country_data['total_cases'], label=country)

plt.title('Total COVID-19 Cases Over Time')
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.legend()
plt.show()

# Plot new cases (7-day average)
plt.figure(figsize=(14, 7))
for country in countries:
    country_data = df_filtered[df_filtered['location'] == country]
    plt.plot(country_data['date'], country_data['new_cases'].rolling(7).mean(), label=country)

plt.title('Daily New COVID-19 Cases (7-day Average)')
plt.xlabel('Date')
plt.ylabel('New Cases')
plt.legend()
plt.show()

# Death rate comparison
latest_data = df_filtered.sort_values('date').groupby('location').last()
plt.figure(figsize=(10, 6))
sns.barplot(x=latest_data.index, y=latest_data['death_rate'])
plt.title('Case Fatality Rate by Country')
plt.xticks(rotation=45)
plt.ylabel('Death Rate (Deaths/Cases)')
plt.show()

# Vaccination progress
plt.figure(figsize=(14, 7))
for country in countries:
    country_data = df_filtered[df_filtered['location'] == country]
    plt.plot(country_data['date'], country_data['people_vaccinated'], label=country)

plt.title('Total Vaccinations Over Time')
plt.xlabel('Date')
plt.ylabel('People Vaccinated')
plt.legend()
plt.show()

# Vaccination rate comparison
plt.figure(figsize=(10, 6))
sns.barplot(x=latest_data.index, y=latest_data['vaccination_rate'])
plt.title('Vaccination Rate by Country (% of Population)')
plt.xticks(rotation=45)
plt.ylabel('Vaccination Rate')
plt.show()

# Get latest data for all countries
latest_global = df.sort_values('date').groupby('location').last().reset_index()

# Create choropleth map of total cases
fig = px.choropleth(latest_global, 
                    locations="iso_code",
                    color="total_cases_per_million",
                    hover_name="location",
                    color_continuous_scale=px.colors.sequential.Plasma,
                    title="Total COVID-19 Cases per Million People")
fig.show()
