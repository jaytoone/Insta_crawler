import json
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)

with open('Insta_Data/2020-12-16.json', 'r') as f:
    dict_ = json.load(f)

# print(dict_)
result_df = pd.DataFrame.from_dict(dict_, 'index')
# print(result_df)
# copy = 'https://scontent-gmp1-1.cdninstagram.com/v/t51.2885-15/e35/s1080x1080/130813151_3564190793696209_5919216480571498654_n.jpg?_nc_ht=scontent-gmp1-1.cdninstagram.com&_nc_cat=101&_nc_ohc=mXAlAkHRUEkAX8arot2&tp=1&oh=ebbe15ae5316b76735163325cd227ce6&oe=600424D9'
print(result_df['picture'][20])
