import seaborn as sns
import pandas as pd

# Load the full diamonds dataset (53,940 rows)
diamonds = sns.load_dataset("diamonds")

# Save the full dataset to a CSV file
diamonds.to_csv("diamonds_full.csv", index=False)
