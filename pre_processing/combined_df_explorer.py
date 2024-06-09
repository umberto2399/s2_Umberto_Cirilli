import pandas as pd
import numpy as np

# Load the cleaned data
df = pd.read_csv('final_cleaned_breakfast_products_with_macro_category.csv')

# Step 1: Handle Missing Values
# Drop rows where 'product_name_es' is missing
df = df.dropna(subset=['product_name_es'])

# Fill missing values for other columns
df['brands'].fillna('Unknown', inplace=True)
df['categories'].fillna('Unknown', inplace=True)
df['quantity'].fillna('Unknown', inplace=True)
df['serving_size'].fillna('Unknown', inplace=True)
df['energy-kcal_value'].fillna(0, inplace=True)
df['sugars_value'].fillna(0, inplace=True)
df['fat_value'].fillna(0, inplace=True)
df['saturated-fat_value'].fillna(0, inplace=True)
df['proteins_value'].fillna(0, inplace=True)
df['salt_value'].fillna(0, inplace=True)
df['fiber_value'].fillna(0, inplace=True)
df['ingredients_text_es'].fillna('Unknown', inplace=True)

# Step 2: Create Ad Hoc Columns for Health Score Calculation
df['adj_sugars_value'] = df['sugars_value'].replace(0, np.nan)
df['adj_fat_value'] = df['fat_value'].replace(0, np.nan)
df['adj_saturated_fat_value'] = df['saturated-fat_value'].replace(0, np.nan)
df['adj_proteins_value'] = df['proteins_value'].replace(0, np.nan)
df['adj_salt_value'] = df['salt_value'].replace(0, np.nan)
df['adj_fiber_value'] = df['fiber_value'].replace(0, np.nan)

# Normalize the nutritional values to a common scale (e.g., per 100 grams)
df['normalized_calories'] = df['energy-kcal_value'] / df['energy-kcal_value'].max()
df['normalized_sugars'] = df['adj_sugars_value'] / df['adj_sugars_value'].max()
df['normalized_fat'] = df['adj_fat_value'] / df['adj_fat_value'].max()
df['normalized_saturated_fat'] = df['adj_saturated_fat_value'] / df['adj_saturated_fat_value'].max()
df['normalized_proteins'] = df['adj_proteins_value'] / df['adj_proteins_value'].max()
df['normalized_salt'] = df['adj_salt_value'] / df['adj_salt_value'].max()
df['normalized_fiber'] = df['adj_fiber_value'] / df['adj_fiber_value'].max()

# Calculate health score with a complex formula
# This is a sample formula: you can adjust the weights based on nutritional guidelines or expert recommendations
df['health_score'] = (df['normalized_proteins'] + df['normalized_fiber']) / (df['normalized_sugars'] + df['normalized_fat'] + df['normalized_saturated_fat'] + df['normalized_salt'] + 1)

# Drop temporary normalization and adjustment columns
df.drop(['normalized_calories', 'normalized_sugars', 'normalized_fat', 'normalized_saturated_fat', 
         'normalized_proteins', 'normalized_salt', 'normalized_fiber',
         'adj_sugars_value', 'adj_fat_value', 'adj_saturated_fat_value', 
         'adj_proteins_value', 'adj_salt_value', 'adj_fiber_value','product_name_en'], axis=1, inplace=True)

df.head()

# store all the infos of a row in a dictionary to check if everything is correct
row = df.iloc[0]
row_dict = row.to_dict()
print(row_dict)
# Save the cleaned dataframe to a new CSV file with standard line terminators
df.to_csv('final_preprocessed_breakfast_products_with_health_score.csv', index=False)

print("Data preprocessing completed. Cleaned data saved to 'final_preprocessed_breakfast_products_with_health_score.csv'.")

