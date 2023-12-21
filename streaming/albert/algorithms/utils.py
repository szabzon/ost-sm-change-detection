import pandas as pd

def data_preprocessing(df):
    preprocessed = False
    # Since attack column is aggregation of attack_P1, attack_P2 and attack_P3, we are dropping those three columns and using only attack col as label
    col_to_drop = ['time','attack_P1', 'attack_P2', 'attack_P3']
    if all(column in df.columns for column in col_to_drop):
        df = df.drop(columns=col_to_drop)
        preprocessed = True
    
    return df, preprocessed


def split_df(df):
    label = df.pop('attack')
    return df, label