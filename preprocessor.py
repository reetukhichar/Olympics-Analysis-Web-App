import pandas as pd

def preprocess(df,noc_country):
    df = df.merge(noc_country, on='NOC', how='left')
    df.drop_duplicates(inplace=True)
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    return df