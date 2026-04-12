from flask import abort
from bs4 import BeautifulSoup
from gevent.pool import Pool
from psycopg2 import Error

import psycopg2
import requests
import os

from routes.create_scrape_result_tables import *

# fetch all 700 pages concurrently
def fetch_all(urls):
    pool = Pool(25)
    return pool.map(lambda url: BeautifulSoup(requests.get(url).content, 'html.parser'), urls)

def scrape()->str:

    #initialize variables
    URL = "https://uwaterloo.ca/student-awards-financial-aid/awards/search-results?level=All&type=All&process=All&affiliation=All&program=All&term=All&citizenship=All&keyword="
    suffix = "&page="
    num = 0
    page = requests.get(URL) #page contains HTML content of url

    soup = BeautifulSoup(page.content, 'html.parser') #soup is a BeautifulSoup object which parses the html content from page.content
    soups = []

    #iterate through all pages (containing bursary/award links)
    while (num != 32):

        tags = soup.find_all("h2") #to store h2 tags

        #iterate through each h2 tag and get link from it
        for h2 in tags:
            link = h2.find("a")
            if(link != None):
                newURL = (link.get('href'))
                soups.append("https://uwaterloo.ca" + newURL)

        num += 1
        newSuffix = suffix + str(num)
        soup = BeautifulSoup(requests.get((URL+newSuffix)).content, 'html.parser')

    #iterates through all links and checks if awards apply to user based on specific criteria
    
    #fetch all 700 pages concurrently
    parsed_pages = fetch_all(soups)

    connection = None
    cursor = None

    try:
        #connect to db
        connection = psycopg2.connect(user=os.environ.get('DB_USER'),
                                    password=os.environ.get('DB_PASSWORD'),
                                    host=os.environ.get('DB_HOST'),
                                    port=os.environ.get('DB_PORT'),
                                    database=os.environ.get('DB_NAME'))    

        cursor = connection.cursor()

        #create tables
        create_scrape_result_tables(cursor)

        for (one, link) in zip(soups, parsed_pages):
            # create beautifulsoup object and access all div's with class = field-item even
            
            award_info_data = [None] * 7
            award_level_data = []
            award_type_data = []
            award_affiliation_data = []
            award_program_data = []
            award_term_data = []

            # award_info_data_0 : award_name
            award_info_data[0] = link.find(class_="uw-site--title").contents[1].string

            # award_info_data_1 : links
            award_info_data[1] = one

            div = [i.string for i in link.find_all("div", class_= "field-label")]
            raw_divs = link.find_all("div", class_="field-item even")
            vals = [i.contents[0].string for i in raw_divs]
            # vals = [i.contents[0].string for i in link.find_all("div", class_="field-item even")]
            vals = [i for i in vals if i != '\n']

            for i in range(len(div)):
                match (div[i]):
                    # award_level_data : level
                    case s if s.startswith("Level"):
                        award_level_data = [j.strip() for j in vals[i].split(',')]
                
                    # award_type_data : award_type
                    case s if s.startswith("Award type:"):
                        award_type_data =  [j.strip() for j in vals[i].split(',')]
                
                    # award_info_data_2 : selection
                    case s if s.startswith("Selection process:"):
                        award_info_data[2] = vals[i].strip()

                    # award_affiliation_data : affiliation
                    case s if s.startswith("Affiliation:"):
                        if vals[i]:
                            award_affiliation_data = [j.strip() for j in vals[i].split(',')]

                    # award_program_data : program
                    case s if s.startswith("Program"):
                        temp = []
                        if (';' in vals[i]):
                            temp2 = [j.strip() for j in vals[i].split(';')] #split btw faculties
                            for j in temp2:
                                temp += (j.split(',')) #split btw programs
                            for j in range(len(temp)):
                                if '→' in temp[j]:
                                    temp[j] = temp[j].split('→', 1)[1].strip()
                                else:                                
                                    temp[j] = temp[j].strip()
                            award_program_data = temp
                        elif '→' in vals[i]:
                            award_program_data.append(vals[i].split('→',1)[1])
                        else:
                            award_program_data.append(vals[i])
                        
                    # award_term_data : term
                    case s if s.startswith("Term:"):
                        award_term_data = [j.strip() for j in vals[i].split(',')]
                        
                    # award_info_data_3 : citizen_status
                    case s if s.startswith("Citizenship:"):
                        if ',' in vals[i]:
                            award_info_data[3] = 'All Students'
                        else:
                            award_info_data[3] = vals[i]

                    # award_info_data_4 : value_desc
                    case s if s.startswith("Value"):
                        if (vals[i] and '$' in vals[i]):
                            award_info_data[4] = vals[i][vals[i].find('$'):].split()[0]
                        else:
                            award_info_data[4] = vals[i]

                    # award_info_data_5 : award_desc
                    case s if s.startswith("Award description:"):
                        award_info_data[5] = vals[i]

                    # award_info_data_6 : eligibility_selection
                    case s if (s.startswith("Eligibility & selection criteria:") or s.startswith("Application details:")):
                        if (not award_info_data[6] and vals[i]):
                            award_info_data[6] = [j for j in raw_divs[i].get_text(', ', strip=True) if len(j) > 5]

            #insert into tables
            insert_award_info = '''
                INSERT INTO award_info (AWARD_NAME, LINK, SELECTION, CITIZEN_STATUS, VALUE_DESC, AWARD_DESC, ELIGIBILITY_SELECTION) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING AWARD_ID
            '''
            cursor.execute(insert_award_info, award_info_data)

            # retrieve award_id
            award_id = cursor.fetchone()[0]

            if award_level_data:
                award_level_data = [[award_id, i] for i in award_level_data]
                insert_level_info = '''
                    INSERT INTO award_level (AWARD_ID, AWARD_LEVEL) 
                    VALUES (%s, %s)
                '''
                cursor.executemany(insert_level_info, award_level_data)

            if award_type_data:
                award_type_data = [[award_id, i] for i in award_type_data]
                insert_type_info = '''
                    INSERT INTO award_type (AWARD_ID, AWARD_TYPE) 
                    VALUES (%s, %s)
                '''
                cursor.executemany(insert_type_info, award_type_data)

            if award_affiliation_data:
                award_affiliation_data = [[award_id, i] for i in award_affiliation_data]
                insert_affiliation_info = '''
                    INSERT INTO award_affiliation (AWARD_ID, AWARD_AFFILIATION) 
                    VALUES (%s, %s)
                '''
                cursor.executemany(insert_affiliation_info, award_affiliation_data)

            if award_program_data:
                award_program_data = [[award_id, i] for i in set(award_program_data)]
                insert_program_info = '''
                    INSERT INTO award_program (AWARD_ID, AWARD_PROGRAM) 
                    VALUES (%s, %s)
                '''
                cursor.executemany(insert_program_info, award_program_data)

            if award_term_data:
                award_term_data = [[award_id, i] for i in award_term_data]
                insert_term_data = '''
                    INSERT INTO award_term (AWARD_ID, AWARD_TERM) 
                    VALUES (%s, %s)
                '''
                cursor.executemany(insert_term_data, award_term_data)
            
            connection.commit()

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        connection.rollback()
        abort(500)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            
    return 'Success'