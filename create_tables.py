import psycopg2
from psycopg2 import Error

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

    #AWARD_TYPE--------------------------------------------------
    create_citizen_table = '''
         DROP TABLE IF EXISTS award_type CASCADE;
    '''
    cursor.execute(create_citizen_table)
    connection.commit()

    create_award_type_table = '''
        CREATE TABLE IF NOT EXISTS award_type (
            AWARD_TYPE VARCHAR(50) PRIMARY KEY
        );
    '''
    cursor.execute(create_award_type_table)
    connection.commit()

    award_types = [
        ('scholarships/awards',),
        ('financial Need awards/bursaries',),
        ('athletic awards',),
        ('entrepreneurial awards',),
        ('international experience awards',),
        ('other travel funding',),
        ('research awards',),
        ('medals/prizes',),
    ]

    insert_award_type_table = '''
        INSERT INTO award_type (AWARD_TYPE) 
        VALUES (%s)
    '''
    cursor.executemany(insert_award_type_table, award_types)
    connection.commit()

    #LEVEL--------------------------------------------------
    create_citizen_table = '''
         DROP TABLE IF EXISTS level CASCADE;
    '''
    cursor.execute(create_citizen_table)
    connection.commit()

    create_level_table = '''
        CREATE TABLE IF NOT EXISTS level (
            LEVEL VARCHAR(50) PRIMARY KEY
        );
    '''
    cursor.execute(create_level_table)
    connection.commit()

    levels = [
        ('year one',),
        ('year two',),
        ('year three',),
        ('year four',),
    ]

    insert_level_table = '''
        INSERT INTO level (LEVEL) 
        VALUES (%s)
    '''
    cursor.executemany(insert_level_table, levels)
    connection.commit()

    #SELECTION PROCESS--------------------------------------------------
    create_citizen_table = '''
         DROP TABLE IF EXISTS selection CASCADE;
    '''
    cursor.execute(create_citizen_table)
    connection.commit()

    create_selection_table = '''
        CREATE TABLE IF NOT EXISTS selection (
            SELECTION VARCHAR(50) PRIMARY KEY
        );
    '''
    cursor.execute(create_selection_table)
    connection.commit()

    sel = [
        ('Students considered automatically - no application',),
        ('Application required',),
    ]

    insert_selection_table = '''
        INSERT INTO selection (SELECTION) 
        VALUES (%s)
    '''
    cursor.executemany(insert_selection_table, sel)
    connection.commit()

    #AFFILIATION--------------------------------------------------
    create_citizen_table = '''
         DROP TABLE IF EXISTS affiliation CASCADE;
    '''
    cursor.execute(create_citizen_table)
    connection.commit()

    create_affiliation_table = '''
        CREATE TABLE IF NOT EXISTS affiliation (
            AFFILIATION VARCHAR(50) PRIMARY KEY
        );
    '''
    cursor.execute(create_affiliation_table)
    connection.commit()

    affil = [
        ('black',),
        ('indigenous',),
        ('mature learning',),
        ('ontario first generation',),
        ('part-time learner',),
        ('refugee',),
        ('varsity athlete',),
        ('women',),
    ]

    insert_affiliation_table = '''
        INSERT INTO affiliation (AFFILIATION) 
        VALUES (%s)
    '''
    cursor.executemany(insert_affiliation_table, affil)
    connection.commit()

    #FACULTY--------------------------------------------------
    create_citizen_table = '''
         DROP TABLE IF EXISTS faculty CASCADE;
    '''
    cursor.execute(create_citizen_table)
    connection.commit()

    create_faculty_table = '''
        CREATE TABLE IF NOT EXISTS faculty (
            FACULTY VARCHAR(50) PRIMARY KEY
        );
    '''
    cursor.execute(create_faculty_table)
    connection.commit()

    facs = [
        ('arts',),
        ('engineering',),
        ('environment',),
        ('health',),
        ('mathematics',),
        ('science',),
    ]

    insert_faculty_table = '''
        INSERT INTO faculty (FACULTY) 
        VALUES (%s)
    '''
    cursor.executemany(insert_faculty_table, facs)
    connection.commit()

    #PROGRAM--------------------------------------------------
    create_citizen_table = '''
         DROP TABLE IF EXISTS program CASCADE;
    '''
    cursor.execute(create_citizen_table)
    connection.commit()

    create_program_table = '''
        CREATE TABLE IF NOT EXISTS program (
            PROGRAM VARCHAR(50) PRIMARY KEY,
            FACULTY VARCHAR(50),
            FOREIGN KEY (FACULTY) REFERENCES faculty(FACULTY)
                ON UPDATE CASCADE
                ON DELETE SET NULL
        );
    '''
    cursor.execute(create_program_table)
    connection.commit()

    programs = [
        ('open to any program',None),
        ('accounting and financial mgmt', 'arts'),
        ('anthropology', 'arts'),
        ('arts and business', 'arts'),
        ('classical studies', 'arts'),
        ('communication arts','arts'),
        ('economics', 'arts'),
        ('english language and literature', 'arts'),
        ('fine arts', 'arts'),
        ('french studies', 'arts'),
        ('gender and social justice', 'arts'),
        ('germanic and slavic studies', 'arts'),
        ('global business and digital arts', 'arts'),
        ('history', 'arts'),
        ('international trade (minor)', 'arts'),
        ('liberal studies', 'arts'),
        ('medieval studies', 'arts'),
        ('music', 'arts'),
        ('peace and conflict studies', 'arts'),
        ('philosophy', 'arts'),
        ('political science', 'arts'),
        ('psychology','arts'),
        ('religious studies','arts'),
        ('sexuality, relationships, and families','arts'),
        ('social development studies','arts'),
        ('sociology and legal studies','arts'),
        ('spanish and latin american studies','arts'),
        ('sustainability and financial management','arts'),
        ('architecture','engineering'),
        ('architectural engineering','engineering'),
        ('biomedical engineering','engineering'),
        ('chemical engineering','engineering'),
        ('civil engineering','engineering'),
        ('computer engineering','engineering'),
        ('electrical engineering','engineering'),
        ('environmental engineering','engineering'),
        ('geological engineering','engineering'),
        ('management engineering','engineering'),
        ('mechanical engineering','engineering'),
        ('mechatronics engineering','engineering'),
        ('nanotechnology engineering','engineering'),
        ('systems design engineering','engineering'),
        ('software engineering','engineering'),
        ('climate and environmental change','environment'),
        ('environment and business','environment'),
        ('environment, resources and sustainability','environment'),
        ('geography and environmental mgmt','environment'),
        ('geography and aviation','environment'),
        ('geomatics','environment'),
        ('international development','environment'),
        ('knowledge integration','environment'),
        ('planning','environment'),
        ('kinesiology','health'),
        ('public health and health sciences','health'),
        ('recreation and leisure studies','health'),
        ('computing and financial mgmt','mathematics'),
        ('actuarial science','mathematics'),
        ('applied mathematics','mathematics'),
        ('bioinformatics','mathematics'),
        ('business and cs (double degree)','mathematics'),
        ('business and math (double degree)','mathematics'),
        ('combinatorics and optimization','mathematics'),
        ('computational mathematics','mathematics'),
        ('computer science','mathematics'),
        ('data science','mathematics'),
        ('information technology mgmt','mathematics'),
        ('math/fin.analysis and risk mgmt','mathematics'),
        ('mathematical economics','mathematics'),
        ('mathematical finance','mathematics'),
        ('mathematical optimization','mathematics'),
        ('mathematical physics','mathematics'),
        ('mathematics','mathematics'),
        ('mathematics/cpa','mathematics'),
        ('mathematics/business admin','mathematics'),
        ('mathematics/teaching','mathematics'),
        ('pure mathematics','mathematics'),
        ('scientific computation/applied mathematics','mathematics'),
        ('statistics','mathematics'),
        ('biochemistry','science'),
        ('biology','science'),
        ('biomedical sciences','science'),
        ('biotechnology/cpa','science'),
        ('biotechnology/economics','science'),
        ('chemistry','science'),
        ('earth and environmental sciences','science'),
        ('materials and nanosciences','science'),
        ('mathematical physics','science'),
        ('medicinal chemistry','science'),
        ('optometry','science'),
        ('pharmacy','science'),
        ('physics and astronomy','science'),
        ('psychology','science'),
        ('science','science'),
        ('science and business','science'),
        ('science and aviation','science'),
    ]

    insert_program_table = '''
        INSERT INTO program (PROGRAM, FACULTY) 
        VALUES (%s, %s)
        ON CONFLICT (PROGRAM) DO NOTHING
    '''
    cursor.executemany(insert_program_table, programs)
    connection.commit()

    #TERM--------------------------------------------------
    create_citizen_table = '''
         DROP TABLE IF EXISTS term CASCADE;
    '''
    cursor.execute(create_citizen_table)
    connection.commit()

    create_term_table = '''
        CREATE TABLE IF NOT EXISTS term (
            TERM VARCHAR(50) PRIMARY KEY
        );
    '''
    cursor.execute(create_term_table)
    connection.commit()

    terms = [
        ('winter',),
        ('spring',),
        ('fall',),
    ]

    insert_term_table = '''
        INSERT INTO term (TERM) 
        VALUES (%s)
    '''
    cursor.executemany(insert_term_table, terms)
    connection.commit()

    #CITIZENSHIP--------------------------------------------------
    create_citizen_table = '''
         DROP TABLE IF EXISTS citizenship CASCADE;
    '''
    cursor.execute(create_citizen_table)
    connection.commit()

    create_citizen_table = '''
        CREATE TABLE IF NOT EXISTS citizenship (
            CITIZEN_STATUS VARCHAR(50) PRIMARY KEY
        );
    '''
    cursor.execute(create_citizen_table)
    connection.commit()

    statuses = [
        ('canadian citizen/permanent resident',),
        ('internationalstudy permit student',),
    ]

    insert_citizen_table = '''
        INSERT INTO citizenship (CITIZEN_STATUS) 
        VALUES (%s)
    '''
    cursor.executemany(insert_citizen_table, statuses)
    connection.commit()

    #WEB_SCRAPE_RESULS--------------------------------------------------
    create_citizen_table = '''
         DROP TABLE IF EXISTS results CASCADE;
    '''
    cursor.execute(create_citizen_table)
    connection.commit()

    create_results_table = '''
        CREATE TABLE IF NOT EXISTS results (
            LINK VARCHAR(100) NOT NULL,
            AWARD_NAME VARCHAR(100) PRIMARY KEY,
            LEVEL VARCHAR(100),
            AWARD_TYPE VARCHAR(100),
            SELECTION VARCHAR(100),
            AFFILIATION VARCHAR(100),
            PROGRAM SERIAL UNIQUE, 
            TERM VARCHAR(100),
            CITIZEN_STATUS VARCHAR(100),
            VALUE_DESC VARCHAR(100),
            AWARD_DESC VARCHAR(1000),
            ELIGIBILITY_SELECTION VARCHAR(500),

            FOREIGN KEY (LEVEL) REFERENCES level(LEVEL)
                ON DELETE SET NULL,

            FOREIGN KEY (AWARD_TYPE) REFERENCES award_type(AWARD_TYPE)
                ON DELETE SET NULL,

            FOREIGN KEY (SELECTION) REFERENCES selection(SELECTION)
                ON DELETE SET NULL,

            FOREIGN KEY (AFFILIATION) REFERENCES affiliation(AFFILIATION)
                ON DELETE SET NULL,

            FOREIGN KEY (TERM) REFERENCES term(TERM)
                ON DELETE SET NULL,

            FOREIGN KEY (CITIZEN_STATUS) REFERENCES citizenship(CITIZEN_STATUS)
                ON DELETE SET NULL
        );
    '''
    cursor.execute(create_results_table)
    connection.commit()

    #AWARD_PROGRAM INTERMEDIARY--------------------------------------------------
    create_award_program_table = '''
         DROP TABLE IF EXISTS award_program CASCADE;
    '''
    cursor.execute(create_award_program_table)
    connection.commit()

    create_award_program_table = '''
        CREATE TABLE IF NOT EXISTS award_program (
            AWARD_ID INT,
            PROGRAM VARCHAR(50),
            FACULTY VARCHAR(50),
            PRIMARY KEY (AWARD_ID, PROGRAM, FACULTY),
            FOREIGN KEY (AWARD_ID) REFERENCES results(PROGRAM)
                ON UPDATE CASCADE
                ON DELETE SET NULL,
            FOREIGN KEY (PROGRAM) REFERENCES program(PROGRAM)
                ON UPDATE CASCADE
                ON DELETE SET NULL,
            FOREIGN KEY (FACULTY) REFERENCES faculty(FACULTY)
                ON UPDATE CASCADE
                ON DELETE SET NULL
        );
    '''
    
    cursor.execute(create_award_program_table)
    connection.commit()     


except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
