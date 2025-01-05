import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('2024/Day17/summary.csv')

# Pivot the data to prepare for plotting
gap_data = data.pivot(index='iter_no', columns='match_size', values='gap_count')

# Plot the data
plt.figure(figsize=(12, 6))

for match_size in gap_data.columns:
    plt.plot(gap_data.index, gap_data[match_size], label=f'Match Size {match_size}')

# Add labels and title
plt.xlabel('Iteration Number')
plt.ylabel('Gap Size')
plt.title('Gap Size by Iteration Number for Different Match Sizes')
plt.legend(title='Match Size')
plt.grid(True)

# Show the plot
plt.show()




# Pivot the data to prepare for plotting
gap_data = data.pivot(index='iter_no', columns='match_size', values='match_count')

# Plot the data
plt.figure(figsize=(12, 6))

for match_size in gap_data.columns:
    plt.plot(gap_data.index, gap_data[match_size], label=f'Match Size {match_size}')

# Add labels and title
plt.xlabel('Iteration Number')
plt.ylabel('Match Size')
plt.title('Match Size by Iteration Number for Different Match Sizes')
plt.legend(title='Match Size')
plt.grid(True)

# Show the plot
plt.show()