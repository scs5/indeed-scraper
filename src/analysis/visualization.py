import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def visualize_skill_counts(skills_count_fn, output_fn, min_count=10):
    # Load skill counts (filter out low count skills)
    skill_counts = pd.read_csv(skills_count_fn)
    skill_counts = skill_counts[skill_counts['Count'] >= min_count]
    
    # Create a bar plot using Seaborn
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x="Count", y="Skill", data=skill_counts, palette="viridis")
    ax.set(xlabel="Count", ylabel="Skill")
    plt.subplots_adjust(left=0.3)
    ax.xaxis.label.set_fontsize(18)
    ax.yaxis.label.set_fontsize(18)
    plt.title("What Are the Most Needed Skills?", fontsize=18, y=1.04)
    
    # Save and display plot
    plt.savefig(output_fn)
    plt.show()


def visualize_hard_vs_soft(skills_count_fn, output_fn):
    # Load skill type counts
    skill_counts = pd.read_csv(skills_count_fn)
    
    # Group skills by category (Hard or Soft) and sum their counts
    category_counts = skill_counts.groupby('Type')['Count'].sum()
    
    # Create the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', colors=['lightblue', 'lightcoral'])
    plt.title('Hard vs. Soft Skills', fontsize=18)
    
    # Save and display chart
    plt.savefig(output_fn)
    plt.show()


def visualize_category_pie(skill_category_fn, output_fn):
    # Load skill category counts
    skill_categories = pd.read_csv(skill_category_fn)
    
    # Group skills by category and sum their counts
    category_counts = skill_categories.groupby('Category')['Count'].sum()
    
    # Filter categories with a percentage of 1% or more
    category_counts = category_counts[category_counts / category_counts.sum() >= 0.01]

    # Remove the "Other" category
    if "Other" in category_counts.index:
        category_counts = category_counts.drop("Other")

    # Create the pie chart
    colors = plt.cm.Paired(range(len(category_counts)))
    plt.figure(figsize=(12, 8))
    plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140, colors=colors)
    plt.title('Skill Categories', fontsize=18)
    
    # Save and display chart
    plt.savefig(output_fn)
    plt.show()


def visualize_known_skills(data_fn, output_fn):
    # Read data
    data = pd.read_csv(data_fn)
    #data = data.drop(index=0)

    # Define a custom color palette for 'Known' values
    color_palette = {'Yes': '#70a34e', 'Kinda': '#d4b04a', 'No': '#c42e1c'}

    # Create a bar plot using Seaborn with custom color mapping
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 12))
    ax = sns.barplot(x="Count", y="Skill", hue="Known", data=data, palette=color_palette, dodge=False)
    ax.set(xlabel="Count", ylabel="Skill")
    plt.subplots_adjust(left=0.3)
    ax.xaxis.label.set_fontsize(18)
    ax.yaxis.label.set_fontsize(18)
    plt.title('What Skills Do I Have?', fontsize=18, y=1.04)
    
    # Increase the fontsize of y-axis tick labels
    ax.tick_params(axis='y', labelsize=12)
    
    # Customize legend fontsize and title fontsize
    ax.legend(title="Do I Know It?", fontsize=14, title_fontsize=16)
    
    # Save and display chart
    plt.savefig(output_fn)
    plt.show()