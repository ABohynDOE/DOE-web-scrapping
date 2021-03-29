#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Scrape the table of contents of all the issues in a journal (from Taylor and Francis online) 
to find relevant article's informations and save it as a csv and pickle.
Author: Alexandre Bohyn
Email: alexandre[dot]bohyn[at]kuleuven[dot]be
Created on Mar 23 2021
"""
# %% Packages
import urllib.request, sys, time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import re


if __name__ == "__main__":
    # Retrieve CLI args and options
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
    journal = sys.argv[1].upper()  # [0] is filename
    # Set verbose
    if "-v" in opts:
        verbose = 1
    else:
        verbose = 0
    # Set logging:
    if "-l" in opts:
        logging = 1
    else:
        logging = 0
    # Currently accepted journals are JQT, TCH, ASA, JAS, QEN
    if journal not in ["JQT", "TCH", "ASA", "JAS", "QEN"]:
        raise ValueError("Unknown journal")
    # %% Journal-specific variables
    if journal.upper() == "JAS":
        url_journal_prefix = "c"
    elif journal.upper() == "QEN":
        url_journal_prefix = "l"
    else:
        url_journal_prefix = "u"
    # %% Scrape journal
    # Combinations of volumes and issues
    max_vol_dict = {"jqt": 53, "tch": 63, "asa": 116, "jas": 48, "qen": 33}
    max_vol = max_vol_dict[journal.lower()]
    # TODO: change the number of issues per volume in ASA (issue don't reset at new volume) and JAS (issue max changes)
    vol_issue = [
        (j, i)
        for j in range(max_vol, 0, -1)
        for i in range(4, 0, -1)
        if not (j == max_vol and i > 1)
    ]
    # Create global data file (and delete previous ones)
    filename = "articles_data/articles" + journal.upper() + ".csv"
    if os.path.exists(filename):
        os.remove(filename)
    f = open(filename, "w", encoding="utf-8")
    headers = "title;type;authors;doi;cite_number;volume;issue;date\n"
    f.write(headers)
    # Create a log file
    log = open("logfile.txt", "w", encoding="utf-8")
    # Loop over all the volumes and issues
    url_base = "https://www.tandfonline.com/toc"
    journal_signature = url_journal_prefix + journal.lower() + "20"
    url_end = "?nav=tocList&"
    upperframe = []
    for vol_iss in vol_issue:
        volume = vol_iss[0]
        date_year = volume + (2021 - max_vol)
        issue = vol_iss[1]
        verbstring = f"{journal.upper()} - Processing volume {volume}: issue {issue}"
        if verbose:
            print(verbstring)
        if logging:
            log.write(verbstring)
        # Generate the URL
        url = "/".join([url_base, journal_signature, str(volume), str(issue) + url_end])
        # Get page content
        try:
            page = requests.get(url)
            if page.status_code == 200:
                if verbose:
                    print("Page content acquired")
                if logging:
                    log.write("\tPage content acquired\n")
            elif page.status_code == 404:
                if verbose:
                    print("Error 404: page not found")
                if logging:
                    print("\tError 404: page not found\n")
            else:
                if verbose:
                    print(f"Unsucessful page status: {page.status_code}")
                if logging:
                    log.write(f"\tUnsucessful page status: {page.status_code}\n")
        except Exception as e:
            error_type, error_obj, error_info = sys.exc_info()
            if verbose:
                print("ERROR FOR LINK:", url)
                print(error_type, "Line:", error_info.tb_lineno)
            if logging:
                log.write("\nERROR FOR LINK: " + url)
                log.write(
                    " ".join(["\n", error_type, "Line:", error_info.tb_lineno, "\n"])
                )
            continue
        # HTML parsing
        # Get all articles entries
        soup = BeautifulSoup(page.text, "html.parser")
        toc_entry = soup.find_all(
            "div",
            attrs={"class": "tocArticleEntry include-metrics-panel toc-article-tools"},
        )

        # Write each article info in the file
        frame = []
        for entry in toc_entry:
            # Title (without quotes or commas)
            title = entry.find("span", attrs={"class": "hlFld-Title"}).text.strip()
            title = re.sub("[“”;]", "", title)
            title = re.sub(",", ":", title)
            type = entry.find("div", attrs={"class": "article-type"})
            if type is None:
                type = title
            else:
                type = type.text.strip().lower()
            # Do not care for editorial board messages
            if type.lower() == "editorial" or "doi/" in type:
                continue
            # Get number of citations
            cross_ref = entry.find("div", attrs={"class": "metrics-panel"})
            if cross_ref is None:
                cite_number = "NA"
            else:
                m = re.search(r"Views(\d+?)Cross", cross_ref.text)
                cite_number = m.group(1)
            # Authors (as dash-separated string)
            authors_text = entry.find(
                "span", attrs={"class": "articleEntryAuthorsLinks"}
            )
            if authors_text is None:
                authors = "NA"
            else:
                authors_text = authors_text.text.strip()
                authors_list = re.split("&|,", authors_text)
                authors = "-".join(authors_list)

            # DOI
            doi = entry.find("a", attrs={"class": "ref nowrap"})
            if doi is None:
                doi = "NA"
            else:
                doi = doi["href"]
            # Log all values in a list
            article_data_list = [
                title,
                type,
                authors,
                doi,
                cite_number,
                str(volume),
                str(issue),
                str(date_year),
            ]
            # Write to csv file and dataframe
            f.write(";".join(article_data_list) + "\n")
            frame.append(tuple(article_data_list))
        # Update the dataframe
        upperframe.extend(frame)

    # Close global csv file
    f.close()
    # Create the global dataframe
    df = pd.DataFrame(
        upperframe,
        columns=[
            "Title",
            "Type",
            "Authors",
            "DOI",
            "Citations",
            "Volume",
            "Issue",
            "Year",
        ],
    )
    # Save it as a pickle
    df_name = "articles_data/articles" + journal.upper() + ".pkl"
    df.to_pickle(df_name)
