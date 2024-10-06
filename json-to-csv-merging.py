import json, csv, os
import pandas as pd

root_dir = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

out_df = pd.DataFrame(columns=['region', 'regionid', 'province', 'provinceid', 'citymun', 'citymunid', 'brgy', 'brgyid', 'ppn', 'pctid', 'pos', 'cand', 'candid', 'pctvotes', 'pcttotal'])

with open(root_dir + "/data/regions/44/root.json", "r") as file:
    reg_df = pd.DataFrame(json.load(file)['srs']).transpose()

with open(root_dir + "/data/regions/" + reg_df.iloc[0]['url'] + ".json", "r") as file:
    prov_df = pd.DataFrame(json.load(file)['srs']).transpose()

for index, value in prov_df.iterrows():
    with open(root_dir + "/data/regions/" + value['url'] + ".json", "r") as file:
        citymun_df = pd.DataFrame(json.load(file)['srs']).transpose()
        print(citymun_df)