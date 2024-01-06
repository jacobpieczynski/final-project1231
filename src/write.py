import csv

def write_csv(results):
    with open('era_whip.csv', 'w', newline='') as csvfile:
        fieldnames = ['Team', 'ERA', 'Wins', 'WHIP']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(results[result])