import psycopg2
from psycopg2 import Error

connection = None
cursor = None

def create_tables()->int:
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
            ('Scholarships/awards',),
            ('Financial need awards/bursaries',),
            ('Athletic awards',),
            ('Entrepreneurial awards',),
            ('International experience awards',),
            ('Other travel funding',),
            ('Research awards',),
            ('Medals/Prizes',),
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
            ('Year One',),
            ('Year Two',),
            ('Year Three',),
            ('Year Four',),
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
                SELECTION VARCHAR(100) PRIMARY KEY
            );
        '''
        cursor.execute(create_selection_table)
        connection.commit()

        sel = [
            ('Students considered automatically - no application.',),
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
            ('Black',),
            ('Indigenous',),
            ('Mature learning',),
            ('Ontario first generation',),
            ('Part-time learner',),
            ('Refugee',),
            ('Varsity athlete',),
            ('Woman',),
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
            ('Arts',),
            ('Engineering',),
            ('Environment',),
            ('Health',),
            ('Mathematics',),
            ('Science',),
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
            ('Open to any program',None),
            ('ccounting and Financial Mgmt', 'Arts'),
            ('Anthropology', 'Arts'),
            ('Arts and Business', 'Arts'),
            ('Classical Studies', 'Arts'),
            ('Communication Arts','Arts'),
            ('Economics', 'Arts'),
            ('English Language and Literature', 'Arts'),
            ('Fine Arts', 'Arts'),
            ('French Studies', 'Arts'),
            ('Gender and Social Justice', 'Arts'),
            ('Germanic and Slavic Studies', 'Arts'),
            ('Global Business and Digital Arts', 'Arts'),
            ('History', 'Arts'),
            ('International Trade (minor)', 'Arts'),
            ('Liberal Studies', 'Arts'),
            ('Medieval Studies', 'Arts'),
            ('Music', 'Arts'),
            ('Peace and Conflict Studies', 'Arts'),
            ('Philosophy', 'Arts'),
            ('Political Science', 'Arts'),
            ('Psychology','Arts'),
            ('Religious Studies','Arts'),
            ('Sexuality, Relationships, and Families','Arts'),
            ('Social Development Studies','Arts'),
            ('Sociology and Legal Studies','Arts'),
            ('Spanish and Latin American Studies','Arts'),
            ('Sustainability and Financial Management','Arts'),
            ('Architecture','Engineering'),
            ('Architectural Engineering','Engineering'),
            ('Biomedical Engineering','Engineering'),
            ('Chemical Engineering','Engineering'),
            ('Civil Engineering','Engineering'),
            ('Computer Engineering','Engineering'),
            ('Electrical Engineering','Engineering'),
            ('Environmental Engineering','Engineering'),
            ('Geological Engineering','Engineering'),
            ('Management Engineering','Engineering'),
            ('Mechanical Engineering','Engineering'),
            ('Mechatronics Engineering','Engineering'),
            ('Nanotechnology Engineering','Engineering'),
            ('Systems Design Engineering','Engineering'),
            ('software Engineering','Engineering'),
            ('Climate and Environmental Change','Environment'),
            ('Environment and Business','Environment'),
            ('Environment, Resources and Sustainability','Environment'),
            ('Geography and Environmental Mgmt','Environment'),
            ('Geography and Aviation','Environment'),
            ('Geomatics','Environment'),
            ('International Development','Environment'),
            ('Knowledge Integration','Environment'),
            ('Planning','Environment'),
            ('Kinesiology','Health'),
            ('Public Health and Health Sciences','Health'),
            ('Recreation and Leisure Studies','Health'),
            ('Computing and Financial Mgmt','Mathematics'),
            ('Actuarial Science','Mathematics'),
            ('Applied Mathematics','Mathematics'),
            ('Bioinformatics','Mathematics'),
            ('Business and CS (Double Degree)','Mathematics'),
            ('Business and Math (Double Degree)','Mathematics'),
            ('Combinatorics and Optimization','Mathematics'),
            ('Computational Mathematics','Mathematics'),
            ('Computer Science','Mathematics'),
            ('Data Science','Mathematics'),
            ('Information Technology Mgmt','Mathematics'),
            ('Math/Fin.Analysis and Risk Mgmt','Mathematics'),
            ('Mathematical Economics','Mathematics'),
            ('Mathematical Finance','Mathematics'),
            ('Mathematical Optimization','Mathematics'),
            ('Mathematical Physics','Mathematics'),
            ('Mathematics','Mathematics'),
            ('Mathematics/CPA','Mathematics'),
            ('Mathematics/Business Admin','Mathematics'),
            ('Mathematics/Teaching','Mathematics'),
            ('Pure Mathematics','Mathematics'),
            ('Scientific Computation/Applied Mathematics','Mathematics'),
            ('Statistics','Mathematics'),
            ('Biochemistry','Science'),
            ('Biology','Science'),
            ('Biomedical Sciences','Science'),
            ('Biotechnology/CPA','Science'),
            ('Biotechnology/Economics','Science'),
            ('Chemistry','Science'),
            ('Earth and Environmental Sciences','Science'),
            ('Materials and Nanosciences','Science'),
            ('Mathematical Physics','Science'),
            ('Medicinal Chemistry','Science'),
            ('Optometry','Science'),
            ('Pharmacy','Science'),
            ('Physics and Astronomy','Science'),
            ('Psychology','Science'),
            ('Science','Science'),
            ('Science and Business','Science'),
            ('Science and Aviation','Science'),
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
            ('Winter',),
            ('Spring',),
            ('Fall',),
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
            ('Canadian citizen/permanent resident',),
            ('International/study permit student',),
            ('both',),
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
                LINK VARCHAR(250) NOT NULL,
                AWARD_NAME VARCHAR(100),
                LEVEL TEXT[],
                AWARD_TYPE TEXT[],     
                SELECTION TEXT[],
                AFFILIATION TEXT[],
                PROGRAM TEXT[], 
                TERM TEXT[],
                CITIZEN_STATUS VARCHAR(50),
                VALUE_DESC TEXT,
                AWARD_DESC TEXT,
                ELIGIBILITY_SELECTION TEXT,
                PRIMARY KEY (LINK, AWARD_NAME),
                FOREIGN KEY (CITIZEN_STATUS) REFERENCES citizenship(CITIZEN_STATUS)
                    ON DELETE SET NULL
            );
        '''
        cursor.execute(create_results_table)
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
    create_tables()