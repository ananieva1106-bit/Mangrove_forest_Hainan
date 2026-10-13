# Geoscripting project : Mangrove forests in Hainan, China
# Authors : Elmo van den Beld, Aleksandra Ananieva, Lea Ehrensperger, Roxane Marguerat
# Period 1, october 2026
# This script is licensed under the MIT License
# Sources are reference throughout the script

# This script implements functions to plot indexes 

# Importing the packages
import matplotlib.pyplot as plt

def development_plot(years, index, title, caption, y_label):
    """
    Plots development of a index variable over given years. 
    : param years: years of interest, index: variable of interest (e.g. fragmentation ratio of mangrove forests), 
    title of the plot, caption of the plot explaining the variables, y_label: brief explanation of variable of interest
    sources : https://stackoverflow.com/questions/34010205/adding-caption-below-x-axis-for-a-scatter-plot-using-matplotlib
              https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figtext.html
    """
    # Creating the figure and subplot, as well as defining figure size
    fig, ax = plt.subplots(figsize=(8, 5))

    # Plotting the variables of interest
    ax.plot(years,index)
    # Defining aesthetics of the plot
    ax.set_title(title)
    ax.set_xlabel("Years")
    ax.set_ylabel(y_label)
    
    # Adding a caption to the plot and place it in the figure's bottom margin
    txt = caption
    fig.subplots_adjust(bottom=0.25)
    fig.text(0.5, 0.04, txt, wrap=True, ha="center", va="bottom", fontsize=11 )

    # Saving created plot into a png 
    fig.savefig("output/Fragm_ratio_table.png", dpi=300, bbox_inches="tight")
