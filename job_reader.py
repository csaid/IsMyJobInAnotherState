from indeed import IndeedClient
from bs4 import BeautifulSoup
import urllib2
import json
import pickle


def get_states():
    f = open('state_names.json')
    states = json.load(f)
    f.close()
    return states


def get_unemployed():
    states = get_states()
    bls_url = "http://www.bls.gov/news.release/laus.t03.htm"
    page = urllib2.urlopen(bls_url)
    soup = BeautifulSoup(page)
    lines = soup.find("pre").get_text().split('\n')
    unemployed = {}
    for line in lines:
        if '.' in line:
            bls_state = line.partition('.')[0]
            if bls_state in states.values():
                unemployed[bls_state] = 1000 * \
                    float(line.split()[8].replace(',', ''))

    return unemployed

# Use Indeed.com's job taxonomy
def initialize_dict(client):
    url = "http://www.indeed.com/find-jobs.jsp"
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    results = {}
    category_rows = soup.find(id='categories').find_all('td')

    # Gather Indeed's job categories
    for row in category_rows:
        category_url = "http://www.indeed.com" + row.find('a')['href']
        category_name = row.find('a').get_text()
        results[category_name] = {}
        sub_page = urllib2.urlopen(category_url)
        sub_soup = BeautifulSoup(sub_page)
        subcategory_rows = sub_soup.find(id='titles').find_all('td')

        # For each job category, grab the subcategories
        for srow in subcategory_rows:
            subcategory_name = srow.find(class_='job').find('a').get_text()
            results[category_name][subcategory_name] = {}

    return results


# Find number of job postings in each subcategory/state combination.
def get_jobs(client, results):
    states = get_states()

    for category, sub_categories in results.iteritems():
        for sub_category in sub_categories:
            for state in states.values():
                print(category)
                print(sub_category)
                print(state)

                params = {
                    'q': 'title:(' + sub_category + ')',
                    'l': state,
                    'userip': "1.2.3.4",
                    'useragent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)"
                }
                count = client.search(**params)['totalResults']

                results[category][sub_category][state] = count

    return results

# Get the job posting / unemployment ratio


def get_scores(results, unemployed):
    states = get_states()
    scores = {}

    for category, sub_categories in results.iteritems():
        scores[category] = {}
        for sub_category in sub_categories:

            # Only grab jobs that have at least 3 postings in each state
            vals = sorted(results[category][sub_category].values())
            min_val = vals[0]
            if min_val >= 3 or sub_category == 'Bartender':
                scores[category][sub_category] = {}
                for state in states.values():
                    scores[category][sub_category][state] = results[
                        category][sub_category][state] / unemployed[state]

        # Remove categories that didn't have any sufficiently large
        # subcategories
        if len(scores[category]) == 0:
            del scores[category]
            print(category)

    return scores


# Get unemployment counts from BLS
unemployed = get_unemployed()

# Get job posting counts from Indeed.com
# You will need to edit the line below to use your own publisher ID
client = IndeedClient(publisher=EnterYourOwnPublisherIDHere)
results = initialize_dict(client)
results = get_jobs(client, results)
pickle.dump(results, open('results.pickle', "wb"))

# Get job posting / unemployment ratios
scores = get_scores(results, unemployed)
json.dump(scores, open('scores.json', "wb"))
