import random

import pandas as pd

if __name__ == '__main__':
    input_path = "D:\\Projects\\Capstone\\Code\\src\\Solvers\\constraint\\dispatching_inputs_old.txt"
    df = pd.read_csv(input_path)
    # Count unique in seed column
    print(df['seed'].nunique())
    # Add a new column with the line number
    df['slurm'] = df.index + 1

    # Rename "rules:+..." column to "rules"
    df.rename(columns={'rules:+...': 'rules'}, inplace=True)

    df["rules"] = [x.split(":") for x in df["rules"]]
    # Rules as a string, joined by a comma
    df["rules"] = [",".join(x) for x in df["rules"]]

    # 3 Dataframes from the original dataframe, one for single rule runs, one for two rule runs, and one for three rule runs
    # Need to add a column to each dataframe with the number of rules

    # N rules column
    df["n_rules"] = [len(x.split(",")) for x in df["rules"]]

    seeds = 30
    new_seeds = [random.randint(0, 1000000) for _ in range(seeds)]
    for i in range(1, 4):
        df_i = df[df["n_rules"] == i].copy()
        df_i['seed'] = df_i['seed'].astype('category')
        df_i['seed'] = df_i['seed'].cat.codes
        df_i['seed'] = df_i['seed'].astype('str')
        # use the current seed value as the index for the new_seeds seed
        df_i['seed'] = df_i['seed'].apply(lambda x: new_seeds[int(x)])
        df_i.to_csv(f"testing\\temp{i}.csv", index=False)

    # Load the three dataframes and combine into one dataframe
    df_1 = pd.read_csv("testing\\temp1.csv")
    df_2 = pd.read_csv("testing\\temp2.csv")
    df_3 = pd.read_csv("testing\\temp3.csv")
    combineddf = pd.concat([df_1, df_2, df_3])
    combineddf.to_csv("testing\\combined.csv", index=False)

    # Make a dict to map the slurm to the seed
    slurm_to_seed = dict(zip(combineddf['slurm'], combineddf['seed']))
    slurm_to_rules = dict(zip(combineddf['slurm'], combineddf['rules']))
    slurm_to_n_rules = dict(zip(combineddf['slurm'], combineddf['n_rules']))

    # Load the new CSV file
    path = "D:\\Projects\\Capstone\\Code\\jobs\\results\\results_sorted_dispatching_rules.csv"
    resultsdf = pd.read_csv(path)
    # remove seed column
    resultsdf.drop(columns=['seed'], inplace=True)

    # Add seed value to the resultsdf dataframe, use the slurm to match the seed value
    resultsdf['seed'] = resultsdf['slurm'].apply(lambda x: slurm_to_seed[x])
    resultsdf['rules'] = resultsdf['slurm'].apply(lambda x: slurm_to_rules[x])
    resultsdf['n_rules'] = resultsdf['slurm'].apply(lambda x: slurm_to_n_rules[x])

    resultsdf.to_csv("testing\\overriden.csv", index=False)

    combineddf.rename(columns={'rules': 'rules:+...'}, inplace=True)
    # Drop the n_rules column
    combineddf.drop(columns=['n_rules'], inplace=True)
    combineddf.drop(columns=['slurm'], inplace=True)
    print(combineddf.head())
    # Write back to inputs file
    combineddf.to_csv("testing\\dispatching_inputs.txt", index=False)