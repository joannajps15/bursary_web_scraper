#import necessary library

#Libraries
import requests
from bs4 import BeautifulSoup
import xlsxwriter

import psycopg2
from psycopg2 import Error

connection = None
cursor = None


#Main method
def main():

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


    with open("Output.txt", "w") as text_file:
        for one in soups:
            text_file.write(one)
            text_file.write("\n")

    # #as of now, all links will be stored in soups

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
            
            data = [0] * 11
            progs = [0] * 3
            # 0 : links
            data[0] = one
            # 1 : award_name
            data[1] = link.find(class_="uw-site--title").contents[1].string

            div = [i.string for i in link.find_all("div", class_= "field-label")]
            vals = [i.contents[0].string for i in link.find_all("div", class_="field-item even")]

            for i in range(len(div)):
                match (div[i]):
                    # 2 : level
                    case s if s.startswith("Level:"):
                        data[2] = vals[i]
                
                    # 3 : award_type
                    case s if s.startswith("Award type:"):
                        data[3] = vals[i]
                
                    # 4 : selection
                    case s if s.startswith("Selection process:"):
                        data[4] = vals[i]

                    # 5 : affiliation
                    case s if s.startswith("Affiliation:"):
                        data[5] = vals[i]

                    # 6 : faculty & program
                    case s if s.startswith("Program:"):
                        # create an array
                        # faculty, program
                        if ('→' in vals[i]):                       
                            parts = vals[i].split('→')
                            parts.insert(1, parts[1].split(','))
                            # we want faculty - program, faculty - program
                            progs = parts
                        else:
                            progs = vals[i]

                    # 7 : term
                    case s if s.startswith("Term:"):
                        data[6] = vals[i]

                    # 8 : citizen_status
                    case s if s.startswith("Citizenship:"):
                        data[7] = vals[i]

                    # 9 : value_desc
                    case s if s.startswith("Value description:"):
                        data[8] = vals[i]

                    # 10 : award_desc
                    case s if s.startswith("Award description:"):
                        data[9] = vals[i]

                    # 11 : eligibility_selection
                    case s if s.startswith("Eligibility & selection criteria:"):
                        data[10] = vals[i]
                
                    case s if s.startswith("Application details:"):
                        data[10] = vals[i]

            print(data)
            #insert into tables!
            insert_term_table = '''
                INSERT INTO results (LINK, AWARD_NAME, LEVEL, AWARD_TYPE, SELECTION, AFFILIATION, TERM, CITIZEN_STATUS, VALUE_DESC, AWARD_DESC, ELIGIBILITY_SELECTION) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_term_table, data)
            connection.commit()

            # insert_term_table = '''
            #     SELECT PROGRAM FROM results WHERE AWARD_NAME = (%s)   
            # '''
            # cursor.execute(insert_term_table, data[0])
            # rows = cursor.fetchall()
            # print(rows)
            # progs.insert(0,rows[0]) #given rows is likely a list, just the first element containing the index?

            # #now insert faculties and programs into award_program table
            # for i in range(len())
            # insert_term_table = '''
            #     INSERT INTO award_program (AWARD_ID, PROGRAM, FACULTY) 
            #     VALUES (%s)
            # '''
            # cursor.executemany(insert_term_table, data)
            # connection.commit()


            break



    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


if __name__ == "__main__":
    main()