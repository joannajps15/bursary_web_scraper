from psycopg2 import Error
from flask import abort

import psycopg2
import os

def create_scrape_result_tables():
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

        #AWARD_INFO--------------------------------------------------
        drop_award_info_table = '''
            DROP TABLE IF EXISTS award_info RESTART IDENTITY CASCADE;
        '''
        cursor.execute(drop_award_info_table)

        create_award_info_table = '''
            CREATE TABLE IF NOT EXISTS award_info (
                AWARD_ID SERIAL PRIMARY KEY,
                AWARD_NAME VARCHAR(100) NOT NULL,
                LINK VARCHAR(250) NOT NULL,
                SELECTION VARCHAR(100),
                CITIZEN_STATUS VARCHAR(50),
                VALUE_DESC TEXT,
                AWARD_DESC TEXT,
                ELIGIBILITY_SELECTION TEXT         
            );
        '''
        cursor.execute(create_award_info_table)

        #LEVELS--------------------------------------------------
        drop_award_level_table = '''
            DROP TABLE IF EXISTS award_level RESTART IDENTITY CASCADE;
        '''
        cursor.execute(drop_award_level_table)

        create_award_level_table = '''
            CREATE TABLE IF NOT EXISTS award_level (
                AWARD_ID INT,
                AWARD_LEVEL VARCHAR(50),
                PRIMARY KEY (AWARD_ID, AWARD_LEVEL),
                FOREIGN KEY (AWARD_ID) REFERENCES award_info(AWARD_ID)
                    ON UPDATE CASCADE
                    ON DELETE SET NULL
            );
        '''
        cursor.execute(create_award_level_table)

        #AWARD_TYPE--------------------------------------------------
        drop_award_type_table = '''
            DROP TABLE IF EXISTS award_type RESTART IDENTITY CASCADE;
        '''
        cursor.execute(drop_award_type_table)

        create_award_type_table = '''
            CREATE TABLE IF NOT EXISTS award_type (
                AWARD_ID INT,
                AWARD_TYPE VARCHAR(50),
                PRIMARY KEY (AWARD_ID, AWARD_TYPE),
                FOREIGN KEY (AWARD_ID) REFERENCES award_info(AWARD_ID)
                    ON UPDATE CASCADE
                    ON DELETE SET NULL

            );
        '''
        cursor.execute(create_award_type_table)
        
        #AFFILIATION--------------------------------------------------
        drop_award_affiliation_table = '''
            DROP TABLE IF EXISTS award_affiliation RESTART IDENTITY CASCADE;
        '''
        cursor.execute(drop_award_affiliation_table)

        create_award_affiliation_table = '''
            CREATE TABLE IF NOT EXISTS award_affiliation (
                AWARD_ID INT,
                AWARD_AFFILIATION VARCHAR(50),
                PRIMARY KEY (AWARD_ID, AWARD_AFFILIATION),
                FOREIGN KEY (AWARD_ID) REFERENCES award_info(AWARD_ID)
                    ON UPDATE CASCADE
                    ON DELETE SET NULL
            );
        '''
        cursor.execute(create_award_affiliation_table)

        #PROGRAM--------------------------------------------------
        drop_award_program_table = '''
            DROP TABLE IF EXISTS award_program RESTART IDENTITY CASCADE;
        '''
        cursor.execute(drop_award_program_table)

        create_award_program_table = '''
            CREATE TABLE IF NOT EXISTS award_program (
                AWARD_ID INT,
                AWARD_PROGRAM TEXT,
                PRIMARY KEY (AWARD_ID, award_program),
                FOREIGN KEY (AWARD_ID) REFERENCES award_info(AWARD_ID)
                    ON UPDATE CASCADE
                    ON DELETE SET NULL

            );
        '''
        cursor.execute(create_award_program_table)

        #TERM--------------------------------------------------
        drop_award_term_table = '''
            DROP TABLE IF EXISTS award_term RESTART IDENTITY CASCADE;
        '''
        cursor.execute(drop_award_term_table)

        create_award_term_table = '''
            CREATE TABLE IF NOT EXISTS award_term (
                AWARD_ID INT,
                AWARD_TERM VARCHAR(50),
                PRIMARY KEY (AWARD_ID, AWARD_TERM),
                FOREIGN KEY (AWARD_ID) REFERENCES award_info(AWARD_ID)
                    ON UPDATE CASCADE
                    ON DELETE SET NULL
            );
        '''
        cursor.execute(create_award_term_table)
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        connection.rollback()
        abort(500)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")