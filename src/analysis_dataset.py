import pandas as pd
import matplotlib.pyplot as plt

input_csv = "data/dataset.csv"

if __name__ == '__main__':
    df = pd.read_csv(input_csv)

    print(df.info())
    print(df.describe())

    # Plot boxplot with logarithmic scale on the X axis
    plt.figure(figsize=(10, 6))
    plt.boxplot(df['engagement'].dropna(), vert=False, patch_artist=True, 
                boxprops=dict(facecolor='lightblue', color='blue'),
                flierprops=dict(markerfacecolor='red', marker='o', markersize=5))

    plt.title('Boxplot of Engagement with Log Scale', fontsize=16)
    plt.xlabel('Engagement (log scale)', fontsize=14)

    plt.xscale('log')

    output_image_path = "data/boxplot_engagement.png"
    plt.savefig(output_image_path)
