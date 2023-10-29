import pandas as pd
from io import StringIO

data = """Name, Age, Country, Salary
Alice, 30, USA, 50000
Bob, 25, Canada, 55000
Charlie, 35, UK, 60000
David, 40, Australia, 70000
"""

# Save this CSV data to a file and read it into a DataFrame
df = pd.read_csv(StringIO(data))

print("Original DataFrame:")
print(df)

# Filter the DataFrame to show only people older than 30
filtered_df = df[df['Age'] > 30]
print("\nPeople older than 30:")
print(filtered_df)

# Sort the DataFrame based on Age
sorted_df = df.sort_values(by='Age')
print("\nDataFrame sorted by Age:")
print(sorted_df)

# Get the average age
average_age = df['Age'].mean()
print("\nAverage Age:", average_age)

# Get the average salary by country
average_salary_by_country = df.groupby('Country')['Salary'].mean()
print("\nAverage Salary by Country:")
print(average_salary_by_country)

# Add a new column indicating if the salary is above 55000
df['High Salary'] = df['Salary'] > 55000
print("\nDataFrame with new 'High Salary' column:")
print(df)

# Drop the 'High Salary' column
df_dropped = df.drop(columns=['High Salary'])
print("\nDataFrame with 'High Salary' column dropped:")
print(df_dropped)

# Apply a function to convert salary to euros (assuming 1 USD = 0.9 EUR)
df['Salary in EUR'] = df['Salary'].apply(lambda x: x * 0.9)
print("\nDataFrame with Salary in EUR:")
print(df)

# Rename the 'Salary in EUR' column to 'Salary (EUR)'
df_renamed = df.rename(columns={'Salary in EUR': 'Salary (EUR)'})
print("\nDataFrame with renamed column:")
print(df_renamed)

# For demonstration, let's add a row with missing values
df.loc[4] = ['Eva', None, None, None]

# Drop rows with any missing values
df_dropped_na = df.dropna()
print("\nDataFrame with rows with missing values dropped:")
print(df_dropped_na)

# Fill missing values with a specific value
df_filled_na = df.fillna('Unknown')
print("\nDataFrame with missing values filled:")
print(df_filled_na)