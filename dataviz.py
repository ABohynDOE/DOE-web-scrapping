#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Visualize the data produced in webscrapping.csv
Author: Alexandre Bohyn
Email: alexandre[dot]bohyn[at]kuleuven[dot]be
Created on Mar 23 2021
"""
# Packages
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_style("white")

# TODO: implement CLI

# Upload the data
journal = "TCH"
data = pd.read_csv("articles_data/articles" + journal.upper() + ".csv", delimiter=";")
# Select articles only
# TODO: turn into python function
articles = data[data.type == "article"]
# Drop NA years
articles = articles.dropna(subset=["date"])
# Convert years to categorical
articles["year"] = articles["date"].map(int)

# Article count per year
art_count = (
    articles.groupby("year")["title"].apply(lambda x: x.count()).to_frame(name="count")
)
art_count["year"] = art_count.index.map(lambda x: x - 10)

# Perc. of "design" occurence in title
articles["contains_des"] = articles["title"].map(lambda s: "design" in s.lower())
des_perc = (
    articles.groupby("year")["contains_des"]
    .apply(lambda x: 100 * x.sum() / x.count())
    .to_frame(name="percentage")
)
des_perc["year"] = des_perc.index

# Plot number of articles per year
# TODO: make it a line plot
plt.figure()
ax1 = sns.countplot(x="year", data=articles)
ax1.set(xlabel="Year", ylabel="", title=f"Number of articles published in {journal}")
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90, fontsize="x-small")
None
plt.savefig(f"plots/{journal}_number_articles.png", dpi=300)

# Plot of percentage of articles containing the word "Design"
# TODO: make it a line plot
# TODO: group several journals on it
plt.figure()
ax2 = sns.barplot(x="year", y="percentage", data=des_perc)
ax2.set(
    xlabel="Year",
    ylabel="Percentage (%)",
    title=f"{journal} articles containing 'design' in the title",
)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90, fontsize="x-small")
None
# ax2.get_figure().savefig(f"plots/{journal}_percentage_design.png", dpi=300)
plt.savefig(f"plots/{journal}_percentage_design.png", dpi=300)

# TODO: convert to a dashboard (using dash and plotly) for interactive set choices