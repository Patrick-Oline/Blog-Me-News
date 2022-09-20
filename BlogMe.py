#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 10:54:25 2022

@author: pat
"""

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#reading excel or xlxs files
data = pd.read_excel('articles.xlsx')

data.describe()
data.info()

#counting the number of articles per source
data.groupby(['source_id'])['article_id'].count()

#number of reactions
data.groupby(['source_id'])['engagement_reaction_count'].sum()

#dropping column
data = data.drop('engagement_comment_plugin_count' , axis = 1 )


# #creating a keyword flag

# keyword = 'crash'

# #for loop to isolate each title
# length = len(data)
# keyword_flag = []
# for x in range(0,length):
#     heading = data['title'][x]
#     if keyword in heading:
#         flag = 1
#     else:
#         flag = 0
#     keyword_flag.append(flag)
    

#creating a function for word search
def keywordflag(keyword):
    length = len(data)
    keyword_flag = []
    for x in range(0,length):
        try:
            heading = data['title'][x]
            if keyword in heading:
                flag = 1
            else:
                flag = 0
        except:
            flag = 0
        keyword_flag.append(flag)
    return keyword_flag

keywordflag = keywordflag('murder')

#creating a new column in data dataframe
data['keyword_flag'] = pd.Series(keywordflag)


#initialize SentimentIntensityAnalyzer
sent_int = SentimentIntensityAnalyzer()

text = data['title'][16]
sent = sent_int.polarity_scores(text)

neg = sent['neg']
pos = sent['pos']
neu = sent['neu']

#adding a for loop to extract sentiment per title
title_neg_sent = []
title_pos_sent = []
title_neu_sent = []

length = len(data)

for x in range(0,length):
    try:    
        text = data['title'][x]
        sent_int = SentimentIntensityAnalyzer()
        sent = sent_int.polarity_scores(text)
        neg = sent['neg'] 
        pos = sent['pos']
        neu = sent['neu']
    except:
        neg = 0
        pos = 0
        neu = 0
    title_neg_sent.append(neg)
    title_pos_sent.append(pos)
    title_neu_sent.append(neu)
#making a series
title_neg_sent = pd.Series(title_neg_sent)
title_pos_sent = pd.Series(title_pos_sent)
title_neu_sent = pd.Series(title_neu_sent)

data['title_neg_sent'] = title_neg_sent
data['title_pos_sent'] = title_pos_sent
data['title_neu_sent'] = title_neu_sent

#writing data as xlsx file
data.to_excel('blogme_clean.xlsx', sheet_name = "blogmedata", index = False)
    










