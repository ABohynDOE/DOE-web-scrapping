#!/usr/bin/python3
#-*- coding: utf-8 -*-
"""
Retrieve google scholar metrics
Author: Alexandre Bohyn
Email: alexandre[dot]bohyn[at]kuleuven[dot]be
Created on Mar 23 2021
"""
# Packages
import pandas as pd
from scholarly import scholarly
from scholarly._navigator import MaxTriesExceededException

# Get articles titles
df = pd.read_csv('articlesJQT.csv',delimiter=';')
titles = list(df[df['type']=='article']['title'])

# For each title, get GS metrics
num_cite_lst = []
filename = 'metrics.csv'
f = open(filename,"w",encoding="utf-8")
for i,t in enumerate(titles[:50]):
    print(f'Processing article {i} on {len(titles)}')
    try:
        search_query = scholarly.search_single_pub(t)
    except MaxTriesExceededException as e:
        print(f'ERROR: article {i}: {e}')
        continue
    num_cite = search_query['num_citations']
    num_cite_lst.append(num_cite)
    f.write(str(num_cite)+";"+t)
f.close()

