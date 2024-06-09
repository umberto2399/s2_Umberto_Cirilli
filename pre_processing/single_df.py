import pandas as pd

# Load the cereals data
df = pd.read_csv('cereals.csv')

# Store the columns into a list
columns = df.columns.tolist()

# Print the columns
print(columns)  