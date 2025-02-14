# -*- coding: utf-8 -*-
"""Mercari_Price_Suggest.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PmemBw9XWZrguqUWG8plkz0ll_dw8zPW
"""

!pip install kaggle

from google.colab import files
files.upload()

import os
import shutil

os.makedirs("/root/.kaggle", exist_ok=True)
shutil.move("kaggle.json", "/root/.kaggle")
os.chmod("/root/.kaggle/kaggle.json", 600)

!kaggle competitions download -c mercari-price-suggestion-challenge

!unzip mercari-price-suggestion-challenge.zip -d ./mercari_data

!cd mercari_data
!ls

!apt-get install -y p7zip-full

!7z e ./mercari_data/train.tsv.7z -o./mercari_data/
!7z e ./mercari_data/test.tsv.7z -o./mercari_data/

!unzip ./mercari_data/sample_submission_stg2.csv.zip -d ./mercari_data/
!unzip ./mercari_data/test_stg2.tsv.zip -d ./mercari_data/

!ls -lh ./mercari_data

!pwd

!ls

# Commented out IPython magic to ensure Python compatibility.
# %cd ./mercari_data
!pwd  # Show the current working directory

!ls

import numpy as np
import pandas as pd

train_data = pd.read_csv('train.tsv', sep = '\t')

test_data = pd.read_csv('test.tsv', sep = '\t')



"""# EDA"""

train_data.head()

test_data.head()

train_data.info()

y = train_data['price']

y

y.describe()

import seaborn as sns
import matplotlib.pyplot as plt

sns.histplot(y)
plt.show()

"""## since data is left skewed, so we have to do log transformation to make it normal distribution form

# Data Cleaning and prepration
"""

y_log = np.log1p(y)

sns.histplot(y_log)
plt.show()

train_data['price'] = np.log1p(train_data['price'])
train_data.head()

"""##  since there are 3 category written in category_name section, so we can divide these into 3 coloumns.."""

def split_category(category_name: str) -> list[str]:
  try:
    return category_name.split('/')
  except:
    return ['NULL', 'NULL', 'NULL']

category_1 = []
category_2 = []
category_3 = []
"""
    just for debugging..
    a = split_category(train_data['category_name'][1])
    print(a[0])
"""
for i in range(train_data.shape[0]):
    temp = split_category(train_data['category_name'][i])
    category_1.append(temp[0])
    category_2.append(temp[1])
    category_3.append(temp[2])

train_data['category_1'] = category_1
train_data['category_2'] = category_2
train_data['category_3'] = category_3

"""## checking if there is null value in data and if there is then replacing with string value.."""

print('1st Category :', train_data['category_1'].value_counts())
print('2nd Category :', train_data['category_2'].nunique())
print('3rd Category :', train_data['category_3'].nunique())

train_data.isnull().sum()

train_data['category_name'] = train_data['category_name'].fillna('NULL')
train_data['brand_name'] = train_data['brand_name'].fillna('NULL')
train_data['item_description'] = train_data['item_description'].fillna('NULL')

train_data.isnull().sum()

"""## now doing same thing for test data"""

category_1_test = []
category_2_test = []
category_3_test = []

for i in range(test_data.shape[0]):
    temp = split_category(test_data['category_name'][i])
    category_1_test.append(temp[0])
    category_2_test.append(temp[1])
    category_3_test.append(temp[2])
test_data['category_1'] = category_1_test
test_data['category_2'] = category_2_test
test_data['category_3'] = category_3_test

print('1st Category :', test_data['category_1'].value_counts())
print('2nd Category :', test_data['category_2'].nunique())
print('3rd Category :', test_data['category_3'].nunique())

test_data.isnull().sum()

test_data['category_name'] = test_data['category_name'].fillna('NULL')
test_data['brand_name'] = test_data['brand_name'].fillna('NULL')

test_data.isnull().sum()

"""# Feature Encoding and vectorization

## combining training and testing dataset
"""

train_data_target = train_data['price']
train_data.drop('price', axis = 1, inplace = True)

mercari_df = pd.concat([train_data, test_data], axis = 0).reset_index(drop = True)
mercari_df.head()

"""## since train_id and test_id are useless ,so we can remove it."""

mercari_df = mercari_df.drop(['train_id', 'test_id'], axis = 1)

mercari_df

# for memory cleaning
import gc
gc.collect()

"""# importing neccesary libraries"""

from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import LabelBinarizer, OneHotEncoder
from sklearn.metrics import mean_squared_error
from sklearn import preprocessing

"""## feature vectorization"""

cntc_vec = CountVectorizer()

x_name = cntc_vec.fit_transform(mercari_df['name'])

tfidf_descp = TfidfVectorizer(max_features = 50000, ngram_range = (1, 3), stop_words = 'english')
x_descp = tfidf_descp.fit_transform(mercari_df['item_description'])

print('name vectorization shape:', x_name.shape)
print('descp vectorization shape:', x_descp.shape)

"""# feature encoding(using one hot encoder)"""

ohe = OneHotEncoder()

x_brand_name = ohe.fit_transform(mercari_df['brand_name'].values.reshape(-1, 1))
x_category_1 = ohe.fit_transform(mercari_df['category_1'].values.reshape(-1, 1))
x_category_2 = ohe.fit_transform(mercari_df['category_2'].values.reshape(-1, 1))
x_category_3 = ohe.fit_transform(mercari_df['category_3'].values.reshape(-1, 1))
x_item_condition_id = ohe.fit_transform(mercari_df['item_condition_id'].values.reshape(-1, 1))
x_shipping = ohe.fit_transform(mercari_df['shipping'].values.reshape(-1, 1))

print('brand_name shape:', x_brand_name.shape)
print('category_1 shape:', x_category_1.shape)
print('category_2 shape:', x_category_2.shape)
print('category_3 shape:', x_category_3.shape)
print('item_condition_id shape:', x_item_condition_id.shape)
print('shipping shape:', x_shipping.shape)

"""##  combining feature vectorized sparse matrix and one hot encoded sparse matrix"""

from lightgbm import LGBMRegressor
from scipy.sparse import hstack

combined_matrix_train = (x_name[:1482535], x_descp[:1482535], x_brand_name[:1482535], x_item_condition_id[:1482535],
                         x_shipping[:1482535], x_category_1[:1482535], x_category_2[:1482535], x_category_3[:1482535])
x_train = hstack(combined_matrix_train).tocsr()

combined_matrix_test = (x_name[1482535:], x_descp[1482535:], x_brand_name[1482535:], x_item_condition_id[1482535:],
                        x_shipping[1482535:], x_category_1[1482535:], x_category_2[1482535:], x_category_3[1482535:])
x_test = hstack(combined_matrix_test).tocsr()

y_train = train_data_target

"""## Ridge regression, since here we have to predict price,  using regression and features are multicollinear so ridge regression.."""

ridge = Ridge(solver = 'lsqr', fit_intercept = False)
ridge.fit(x_train, y_train)
preds = ridge.predict(x_test)
print(preds)
print()

"""## since we had done log trnasformation, so we are doing it exponnetial transformation so it becomes normal.."""

preds = np.expm1(preds)

final_submission = pd.DataFrame()
final_submission['test_id'] = test_data['test_id']
final_submission['price'] = preds
final_submission.head()

final_submission.to_csv('submission.csv', index = False, header = True)

final_submission.shape

