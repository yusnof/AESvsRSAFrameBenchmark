import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file
csv_file = 'results.csv'  # Replace with your CSV file path
data = pd.read_csv(csv_file)

# Filter for successful decryptions
data = data[data['Decryption Correct'].astype(str).str.lower() == 'true']

# Convert times to milliseconds and compute combined time
data['Encryption Time (ms)'] = data['Encryption Time (s)'] * 1000
data['Decryption Time (ms)'] = data['Decryption Time (s)'] * 1000
data['Combined Time (ms)'] = data['Encryption Time (ms)'] + data['Decryption Time (ms)']

# Group by Algorithm and fileSize, averaging over iterations
grouped_data = data.groupby(['Algorithm', 'fileSize (kBytes)'])['Combined Time (ms)'].mean().reset_index()

# Pivot data for plotting
pivot_data = grouped_data.pivot(index='fileSize (kBytes)', columns='Algorithm', values='Combined Time (ms)').fillna(0)
file_sizes = pivot_data.index.astype(str).tolist()  # Convert to strings for labels
algorithms = pivot_data.columns.tolist()
combined_times = pivot_data.values

# Create bar chart
plt.figure(figsize=(10, 6))
bar_width = 0.35
index = np.arange(len(file_sizes))

# Plot bars for each algorithm
for i, algo in enumerate(algorithms):
    plt.bar(index + i * bar_width, 
            combined_times[:, i], 
            bar_width, 
            label=f'{algo} Combined Time', 
            color=['#4ECDC4', '#FF6B6B'][i % 2], 
            edgecolor=['#388E3C', '#D32F2F'][i % 2])

# Add value labels on top of bars
for i, algo in enumerate(algorithms):
    for j, time in enumerate(combined_times[:, i]):
        plt.text(index[j] + i * bar_width, time, f'{time:.2f}', 
                 ha='center', va='bottom', fontsize=8)

# Customize plot
plt.xlabel('File Size (kBytes)')
plt.ylabel('Combined Time (milliseconds)')
plt.title('AES vs RSA Combined Encryption + Decryption Time')
plt.xticks(index + bar_width / 2, file_sizes)
plt.yscale('log')  # Log scale for large time differences
plt.grid(True, which="both", ls="--")
plt.legend()
plt.tight_layout()

# Save and show plot
plt.savefig('benchmark_plot.png')
plt.show()