#! /usr/bin/env python
# coding: utf8
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

df = pd.DataFrame(pd.read_excel('AI.xlsx', engine='openpyxl'))
df = df.drop(columns=['資料來源'])
df = df.drop(columns=['ID'])
df = df.rename(columns={'正確答案':'output'})

df['instruction'] =  '請根據以下輸入回答選擇題，並以數字回答:\n'
col = df.pop('instruction')
df.insert(0, col.name, col)

df['input'] = df['文章'].astype('string') + '問題:' + df['問題'].astype('string') + '1: ' + df['選項1'].astype('string') + '2: ' + df['選項2'].astype('string') + '3: ' + df['選項3'].astype('string') + '4: ' + df['選項4'].astype('string') + '\n'
df = df.drop(columns=['文章', '問題', '選項1', '選項2', '選項3', '選項4'])
col1 = df.pop('input')
df.insert(1, col1.name, col1)

df['instruction'] = df['instruction'].astype('string')
df['input'] = df['input'].astype('string')
df['output'] = df['output'].astype('string')

train, validation = train_test_split(df, test_size=0.2)


with open('AI_train.json', 'w', encoding='utf-8') as f:
    train.to_json(f, force_ascii=False, orient='records', indent=4)

with open('AI_validation.json', 'w', encoding='utf-8') as f1:
    validation.to_json(f1, force_ascii=False, orient='records', indent=4)
print("-----Training Data Conversion finish!-----")




df1 = pd.DataFrame(pd.read_excel('AI1000.xlsx', engine='openpyxl'))
df1 = df1.replace(np.nan, '', regex=True)
df1 = df1.rename(columns={'題號':'id'})
df1['instruction'] =  '請根據以下輸入回答選擇題，並以數字回答:\n'
col_df1 = df1.pop('instruction')
df1.insert(1, col_df1.name, col_df1)

df1['input'] = df1['文章'].astype('string') + '問題:' + df1['問題'].astype('string') + '1: ' + df1['選項1'].astype('string') + '2: ' + df1['選項2'].astype('string') + '3: ' + df1['選項3'].astype('string') + '4: ' + df1['選項4'].astype('string') + '\n'
df1 = df1.drop(columns=['文章', '問題', '選項1', '選項2', '選項3', '選項4'])
col1_df1 = df1.pop('input')
df1.insert(2, col1_df1.name, col1_df1)

df1['id'] = df1['id'].astype('string')
df1['instruction'] = df1['instruction'].astype('string')
df1['input'] = df1['input'].astype('string')

with open('AI1000.json', 'w', encoding='utf-8') as file:
    df1.to_json(file, force_ascii=False, orient='records', indent=4)
print("-----Testing Data Conversion finish!-----")