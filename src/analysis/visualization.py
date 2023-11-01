import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def visualize_skill_counts(skills_count_fn, output_fn, min_count=10):
    # Load skill counts (filter out low count skills)
    skill_counts = pd.read_csv(skills_count_fn)
    skill_counts = skill_counts[skill_counts['Count'] >= min_count]
    
    # Create a bar plot using Seaborn
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))  # Adjust the figure size as needed
    ax = sns.barplot(x="Count", y="Skill", data=skill_counts, palette="viridis")
    
    # Customize x and y axis titles
    ax.set(xlabel="Count", ylabel="Skill")
    
    # Adjust the plot's margins to ensure skill labels are fully visible
    plt.subplots_adjust(left=0.3)
    
    # Customize axis title font size and weight
    ax.xaxis.label.set_fontsize(18)
    ax.yaxis.label.set_fontsize(18)
    
    # Display and save the plot
    plt.savefig(output_fn)
    plt.show()


def visualize_hard_vs_soft(skills_count_fn, output_fn):
    # Load skill counts
    skill_counts = pd.read_csv(skills_count_fn)
    
    # Group skills by category (Hard or Soft) and sum their counts
    category_counts = skill_counts.groupby('Category')['Count'].sum()
    
    # Create a pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', colors=['lightblue', 'lightcoral'])
    plt.title('Hard vs. Soft Skills')
    
    # Save the pie chart
    plt.savefig(output_fn)
    plt.show()