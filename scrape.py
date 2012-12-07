import csv
from pyquery import PyQuery as pq

GRDA_URL = 'http://www.texastransparency.org/budget/reports/' \
            'General_Revenue_Dedicated_Accounts.php'
DETAILED_URL = 'https://cpafmprd.cpa.state.tx.us/fiscalmoa/fund.jsp?num='


def main():
    try:
        f = open("scrape_results.csv", "wb")
        writer = csv.writer(f)

        writer.writerow([
            "id",
            "account_name",
            "fy2011ending",
            "fy2013revenues",
            "fy2013hb1",
            "adjustments",
            "revbalances",
            "purpose",
            "agency",
            "notes",
        ])

        page = pq(GRDA_URL)
        account_names = [i.text for i in page.find('caption a')]

        for (i,tr) in enumerate([i('tr')[1] for i in page('table').items()][:-1]):
            payload = []
            payload.append(account_names[i][:4].encode('utf8'))  # id
            payload.append(account_names[i][20:].encode('utf8'))  # account_name

            print 'Working on {0} (id: {1})'.format(payload[1], payload[0])
            for td in tr.findall('td'):
                payload.append(td.text)  # grabs each <td> with the totals

            dpage = pq(DETAILED_URL + payload[0])
            purpose = dpage.find('#purpose div.detail').text()  # purpose
            agency = dpage.find('#admin_agencies a').text()  # agency
            note = dpage.find('#notes div.detail').text()  # notes
            payload.append(purpose.strip().encode('utf8') if purpose else '')
            payload.append(agency.strip()[6:].encode('utf8') if agency else '')
            payload.append(note.strip().encode('utf8') if note else '')

            writer.writerow(payload)
        f.close()
    except KeyboardInterrupt:
        f.close()
        print "Stopping this train..."

if __name__ == '__main__':
    main()
