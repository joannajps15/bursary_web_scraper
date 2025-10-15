#import necessary library

#Libraries
import requests
from bs4 import BeautifulSoup
# import xlsxwriter

import psycopg2
from psycopg2 import Error

connection = None
cursor = None

def scrape() -> int:

    #initialize variables
    URL = "https://uwaterloo.ca/student-awards-financial-aid/awards/search-results?level=All&type=All&process=All&affiliation=All&program=All&term=All&citizenship=All&keyword="
    # URL = "https://uwaterloo.ca/student-awards-financial-aid/awards/search-results?affiliation=All&citizenship=All&keyword=&level=All&process=All&program=All&term=All&type=All"
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
                # print(newURL)
                soups.append("https://uwaterloo.ca" + newURL)

        num += 1
        newSuffix = suffix + str(num)
        soup = BeautifulSoup(requests.get((URL+newSuffix)).content, 'html.parser')

    #iterates through all links and checks if awards apply to user based on specific criteria

    connection = None
    cursor = None

    try:
        #connect to db
        connection = psycopg2.connect(user="postgres",
                                    password="postGres#321",
                                    host="127.0.0.1",
                                    port="5432",
                                    database="web_scraper_db")    

        cursor = connection.cursor()


        for one in soups:
            #create beautifulsoup object and access all div's with class = field-item even
            link = BeautifulSoup(requests.get(one).content, 'html.parser')
            
            data = [None] * 12

            # 0 : links
            data[0] = one
            # 1 : award_name
            data[1] = link.find(class_="uw-site--title").contents[1].string

            div = [i.string for i in link.find_all("div", class_= "field-label")]
            vals = [i.contents[0].string for i in link.find_all("div", class_="field-item even")]
            vals = [i for i in vals if i != '\n']

            for i in range(len(div)):
                match (div[i]):
                    # 2 : level
                    case s if s.startswith("Level"):
                        lvl = vals[i].split(',') # returns a list of all levels
                        data[2] = [i.strip() for i in lvl]
                
                    # 3 : award_type
                    case s if s.startswith("Award type:"):
                        awd_type = vals[i].split(',')
                        data[3] =  [i.strip() for i in awd_type]
                
                    # 4 : selection
                    case s if s.startswith("Selection process:"):
                        sel = vals[i].split(',')
                        data[4] =  [i.strip() for i in sel]

                    # 5 : affiliation
                    case s if s.startswith("Affiliation:"):
                        affil = vals[i].split(',')
                        data[5] = [i.strip() for i in affil]

                    # 6 : program
                    case s if s.startswith("Program"):
                        temp = []
                        if (';' in vals[i]):
                            temp2 = [j.strip() for j in vals[i].split(';')]
                            for j in temp2:
                                temp += (j.split(','))
                            for j in range(len(temp)):
                                if '→' in temp[j]:
                                    temp[j] = temp[j].split('→', 1)[1]
                            data[6] = temp
                        else:
                            if '→' in vals[i]:
                                vals[i] = vals[i].split('→',1)[1]
                            data[6] = [vals[i]]
                        
                    # 7 : term
                    case s if s.startswith("Term:"):
                        term = vals[i].split(',')
                        data[7] = [i.strip() for i in term]
                        
                    # 8 : citizen_status
                    case s if s.startswith("Citizenship:"):
                        if ',' in vals[i]:
                            data[8] = 'both'
                        else:
                            data[8] = vals[i]

                    # 9 : value_desc
                    case s if s.startswith("Value"):
                        data[9] = vals[i]

                    # 10 : award_desc
                    case s if s.startswith("Award description:"):
                        data[10] = vals[i]

                    # 11 : eligibility_selection
                    case s if s.startswith("Eligibility & selection criteria:"):
                        data[11] = vals[i]
                
                    case s if s.startswith("Application details:"):
                        data[11] = vals[i]

            #insert into tables
            print(data)
            insert_term_table = '''
                INSERT INTO results (LINK, AWARD_NAME, LEVEL, AWARD_TYPE, SELECTION, AFFILIATION, PROGRAM, TERM, CITIZEN_STATUS, VALUE_DESC, AWARD_DESC, ELIGIBILITY_SELECTION) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_term_table, data)
            connection.commit()

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return 0
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            return 1

if __name__ == "__main__":
    scrape()