import urllib.request
import json
import csv

baseurl = "https://2022electionresults.comelec.gov.ph/"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

#   president candidates
url = baseurl + "data/contests/5587.json"
req = urllib.request.Request(url, None, headers)

with urllib.request.urlopen(req) as file:
    pres = json.load(file)

#   senator candidates
url = baseurl + "data/contests/5589.json"
req = urllib.request.Request(url, None, headers)

with urllib.request.urlopen(req) as file:
    senator = json.load(file)

#   partylist candidates
url = baseurl + "data/contests/11172.json"
req = urllib.request.Request(url, None, headers)

with urllib.request.urlopen(req) as file:
    ptlist = json.load(file)

#   results
url = baseurl + "data/regions/44/44021.json"
req = urllib.request.Request(url, None, headers)

with urllib.request.urlopen(req) as file, open('2022_pres.csv', 'a') as p_out, open('2022_sen.csv', 'a') as sen_out, open('2022_ptlist.csv', 'a') as hrep_out:
#   regions json
    region = json.load(file)

    for r_key in region['srs']:
        req = urllib.request.Request(
            baseurl + "data/regions/" + region['srs'][r_key]['url'] + ".json", 
            None, headers
            )
        
        with urllib.request.urlopen(req) as file:
#           provinces json
            province = json.load(file)
            
            for p_key in province['srs']:
                req = urllib.request.Request(
                    baseurl + "data/regions/" + province['srs'][p_key]['url'] + ".json",
                    None, headers
                )

                with urllib.request.urlopen(req) as file:
                    citymun = json.load(file)

                    for cm_key in citymun['srs']:
                        req = urllib.request.Request(
                            baseurl + "data/regions/" + citymun['srs'][cm_key]['url'] + ".json",
                            None, headers
                        )

                        with urllib.request.urlopen(req) as file:
                            brgy = json.load(file)

                            for b_key in brgy['srs']:
                                req = urllib.request.Request(
                                    baseurl + "data/regions/" + brgy['srs'][b_key]['url'] + ".json",
                                    None, headers
                                )

                                with urllib.request.urlopen(req) as file:
                                    precinct = json.load(file)

                                    for pct in precinct['pps']:
                                        req = urllib.request.Request(
                                            baseurl + "data/results/" + pct['vbs']['url'] + ".json",
                                            None, headers
                                        )

                                        with urllib.request.urlopen(req) as file:
                                            result = json.load(file)
