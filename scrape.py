#import necessary library

#Libraries
import requests
from bs4 import BeautifulSoup
import xlsxwriter
import sys

#Main method
def main(year, term, program, athlete):

    if(athlete == "True"):
        ath = True
    else:
        ath = False

    #initialize variables
    URL = "https://uwaterloo.ca/student-awards-financial-aid/awards/search-results?affiliation=All&citizenship=All&keyword=&level=All&process=All&program=All&term=All&type=All"
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


    #REMOVED: writes all soups to a text file
    # with open("Output.txt", "w") as text_file:
    #     for one in soups:
    #         text_file.write(one)
    #         text_file.write("\n")

    #as of now, all links will be stored in soups

    # #iterates through all links and checks if awards apply to user based on specific criteria
    newSoups = []

    for one in soups:
        #create beautifulsoup object and access all div's with class = field-item even
        link = BeautifulSoup(requests.get(one).content, 'html.parser')

        div = link.find_all("div", class_ = "field-item even")
        check = [False, False, False]

        for two in div:

            if (two.string != None):

                #Checks Athlete
                if(not ath):
                    if("Athlet" in two.string):
                        break

                #Check Lvl
                if(not(check[0]) and year in two.string):
                    check[0] = True
                    # print("lvl: ", check[0])
                
                #Check Program
                if(not(check[1]) and ("Open to any program" in two.string) or program in two.string):
                    check[1] = True
                    if ("→" in two.string and not program in two.string):
                        check[1] = False
                    # print("program: ", check[1])
            
                #Check Term
                if(not(check[2]) and term in two.string):
                    check[2] = True
                    # print("term", check[2])
                
                #Adds website to newSoups
                if (check[0] and check[1] and check[2]):
                    # print(two.string, ": ", ("https://uwaterloo.ca" + one))
                    newSoups.append(one)
                    break

    #REMOVED: writing newSoups to textfile
    with open("links.txt", "w") as text_file:
        for one in newSoups:
            text_file.write(one)
            text_file.write("\n")

    #Initialize Worksheet

    #REMOVED: reading links from site
    # with open("links.txt", "r") as text_file:
    #         lines = text_file.readlines()

    workbook = xlsxwriter.Workbook('test.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column_pixels(0, 4, 200)

    worksheet.write("A1", "Link")
    worksheet.write("B1", "Name")
    worksheet.write("C1", "Award Description")
    worksheet.write("D1", "Eligibility Criteria")
    worksheet.write("E1", "Value Descrption")
    worksheet.write("F1", "Selection Process")

    i = 1
    j = 0

    for line in newSoups:

    # #iterates through all links and filters through specific datasets using Python
    # for one in newSoups:

        #Link
        worksheet.write(i, j, line)

        #process in Excel sheet!!
        
        line2 = line.strip()
        link = BeautifulSoup(requests.get(line2).content, 'html.parser')

        #Title
        title = link.find("div", class_ = "uw-site--title")
        h = title.find("h1")
        if(h != None):
            # print(h.string, "\n")
            worksheet.write(i,(j+1), h.string)

        # #Award Desc
        desc = link.find_all("p")
        # span = link.find('span')
        for text in desc:
            if text.string != None:
                # print(all.string, "\n")
                worksheet.write(i, (j+2), text.string)
                break

        # #Eligibility

        #eligibility criteria dont seem to be working....
        elig = link.find_all("li")
        words = ""
        for point in elig:
            #Eligibility
            if point.find("a") == "None" and point.string != None:
                words = words + "; " + point.string 
        
        worksheet.write(i, (j+3), words)
        # # print(words)

        div = link.find_all("div", class_ = "field-item even")

        for two in div:
            if two.string != None:
                #Value 
                if "$" in two.string or "varies" in two.string:
                    worksheet.write(i, (j+4), two.string)
                    # print(two.string)
                
                #Selection
                if "pplication" in two.string:
                    worksheet.write(i, (j+5), two.string)
                    # print(two.string)

        i+=1

    workbook.close()


if __name__ == "__main__":

    year = sys.argv[1]
    term = sys.argv[2]
    program = sys.argv[3]
    athlete = sys.argv[4]
    
    main(year, term, program, athlete)
    
    # main()