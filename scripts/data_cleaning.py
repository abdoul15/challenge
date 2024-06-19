import pandas as pd


def normalize_title(title):
    return title.strip().lower().replace(" ", "").replace(":", "").replace("-", "")

def clean_data(input_file, output_file):
    df_bomojo = pd.read_csv(input_file, sep='\t')
    df_bomojo.fillna({'#1 Release': 'Unknown'}, inplace=True)
    df_bomojo.drop_duplicates(inplace=True)
    df_bomojo['normalized_title'] = df_bomojo['#1 Release'].apply(normalize_title)
    df_bomojo.to_csv(output_file, index=False)

if __name__ == "__main__":
    clean_data('data/raw/bomojobrandindices.csv', 'data/cleaned_bofficemojo.csv')