import csv

def write_csv(results, filename="era_whip.csv"):
    with open(filename, 'w', newline='') as csvfile:
        #fieldnames = ['Team', 'ERA', 'Wins', 'WHIP']
        fieldnames = ['Gameid', 'Home', 'Visitor', 'Date', 'OBP Difference', 'AVG Difference', 'SLG Difference', 'OPS Difference', 'ERA Difference', 'WHIP Difference', 'K9 Difference', 'BB9 Difference', 'Home Recency Adv', 'Run Differential', 'Head to Head', 'Home Win']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(results[result])