#!/usr/bin/bash
echo 'Gathering data':
for i in {'ASA','ASA'}; 
do
    echo Journal: $i
    #python3 webscrapping.py $i -v -l
done

echo 'Generating graphs':
for i in {'JQT','TCH','QEN'}; 
do
    echo Journal: $i
    #TODO: cli for dataviz generation
done
