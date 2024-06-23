import pandas as pd

# Define the file paths
input_file_path = r'C:\Users\noapa\OneDrive - Technion\PhD\Research\Exploration project\TrialRun_data\input_data.csv'
output_file_path = r'C:\Users\noapa\OneDrive - Technion\PhD\Research\Exploration project\TrialRun_data\processed_data.csv'

# Load the CSV file
df = pd.read_csv(input_file_path)

df_ordered = df.sort_values(by=['Prolific_id'])

# Save the processed data to a new CSV file
df_ordered.to_csv(output_file_path, index=False)