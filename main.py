import urllib.request
import json
import csv
import os
import time

dir_path = os.path.dirname(os.path.realpath(__file__))
baseurl = "https://2022electionresults.comelec.gov.ph/"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

#   president candidates
url = baseurl + "data/contests/5587.json"
req = urllib.request.Request(url, None, headers)

with urllib.request.urlopen(req) as file:
    out_dir = os.path.join(dir_path, "data", "contests").replace("\\", "/")
    os.makedirs(os.path.dirname(out_dir + "/" + "pres.json"), exist_ok=True)
    with open(out_dir + "/" + "pres.json", "w") as outfile:
        outfile.write(file.read().decode('utf-8'))
        outfile.close()

#   senator candidates
url = baseurl + "data/contests/5589.json"
req = urllib.request.Request(url, None, headers)

with urllib.request.urlopen(req) as file:
    out_dir = os.path.join(dir_path, "data", "contests").replace("\\", "/")
    os.makedirs(os.path.dirname(out_dir + "/" + "sen.json"), exist_ok=True)
    with open(out_dir + "/" + "sen.json", "w") as outfile:
        outfile.write(file.read().decode('utf-8'))
        outfile.close()

#   partylist candidates
url = baseurl + "data/contests/11172.json"
req = urllib.request.Request(url, None, headers)

with urllib.request.urlopen(req) as file:
    out_dir = os.path.join(dir_path, "data", "contests").replace("\\", "/")
    os.makedirs(os.path.dirname(out_dir + "/" + "partylist.json"), exist_ok=True)
    with open(out_dir + "/" + "partylist.json", "w") as outfile:
        outfile.write(file.read().decode('utf-8'))
        outfile.close()

#   results
url = baseurl + "data/regions/44/44021.json"
req = urllib.request.Request(url, None, headers)

with urllib.request.urlopen(req) as file:
#   regions json
    region = json.load(file)
    out_dir = os.path.join(dir_path, "data", "regions").replace("\\", "/")
    os.makedirs(os.path.dirname(out_dir + "/" + "44/root" + ".json"), exist_ok=True)
    with open(out_dir + "/" + "44/root" + ".json", "w") as outfile:
        json.dump(region, outfile)
        outfile.close()

    for r_key in region['srs']:
        req = urllib.request.Request(
            baseurl + "data/regions/" + region['srs'][r_key]['url'] + ".json", 
            None, headers
            )
        
        with urllib.request.urlopen(req) as file:
#           provinces json
            province = json.load(file)
            out_dir = os.path.join(dir_path, "data", "regions").replace("\\", "/")
            os.makedirs(os.path.dirname(out_dir + "/" + region['srs'][r_key]['url'] + ".json"), exist_ok=True)
            with open(out_dir + "/" + region['srs'][r_key]['url'] + ".json", "w") as outfile:
                json.dump(province, outfile)
                outfile.close()
            
            for p_key in province['srs']:
                req = urllib.request.Request(
                    baseurl + "data/regions/" + province['srs'][p_key]['url'] + ".json",
                    None, headers
                )

                with urllib.request.urlopen(req) as file:
#                   cities and municipalities json
                    citymun = json.load(file)
                    print("Province: " + citymun['rn'])
                    out_dir = os.path.join(dir_path, "data", "regions").replace("\\", "/")
                    os.makedirs(os.path.dirname(out_dir + "/" + province['srs'][p_key]['url'] + ".json"), exist_ok=True)
                    with open(out_dir + "/" + province['srs'][p_key]['url'] + ".json", "w") as outfile:
                        json.dump(citymun, outfile)
                        outfile.close()

                    for cm_key in citymun['srs']:
                        req = urllib.request.Request(
                            baseurl + "data/regions/" + citymun['srs'][cm_key]['url'] + ".json",
                            None, headers
                        )

                        with urllib.request.urlopen(req) as file:
                            brgy = json.load(file)
                            print("City/Mun: " + brgy['rn'])
                            out_dir = os.path.join(dir_path, "data", "regions").replace("\\", "/")
                            os.makedirs(os.path.dirname(out_dir + "/" + citymun['srs'][cm_key]['url'] + ".json"), exist_ok=True)
                            with open(out_dir + "/" + citymun['srs'][cm_key]['url'] + ".json", "w") as outfile:
                                json.dump(brgy, outfile)
                                outfile.close()

                            for b_key in brgy['srs']:
                                req = urllib.request.Request(
                                    baseurl + "data/regions/" + brgy['srs'][b_key]['url'] + ".json",
                                    None, headers
                                )

                                with urllib.request.urlopen(req) as file:
#                                   precincts json
                                    precinct = json.load(file)
                                    out_dir = os.path.join(dir_path, "data", "regions").replace("\\", "/") + "/" + brgy['srs'][b_key]['url'] + ".json"
                                    os.makedirs(os.path.dirname(out_dir), exist_ok=True)
                                    with open(out_dir, "w") as outfile:
                                        json.dump(precinct, outfile)
                                        outfile.close()

                                    for pct in precinct['pps']:
                                        out_dir = os.path.join(dir_path, "data", "results").replace("\\", "/") + "/" + pct['vbs'][0]['url'] + ".json"
                                        os.makedirs(os.path.dirname(out_dir), exist_ok=True)

                                        if os.path.isfile(out_dir):
                                            continue

                                        req = urllib.request.Request(
                                            baseurl + "data/results/" + pct['vbs'][0]['url'] + ".json",
                                            None, headers
                                        )

                                        try:
                                            with urllib.request.urlopen(req) as file:
                                                with open(out_dir, "w") as outfile:
                                                    outfile.write(file.read().decode('utf-8'))
                                                    outfile.close()
                                        except:
                                            print("Error: " + req.full_url)
                print("Timeout...")
                time.sleep(30)
                                            
