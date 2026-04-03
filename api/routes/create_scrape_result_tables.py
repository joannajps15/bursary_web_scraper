def create_scrape_result_tables(cursor)->int:
        #AWARD_INFO--------------------------------------------------
        truncate_award_info_table = '''
            TRUNCATE TABLE award_info RESTART IDENTITY CASCADE;
        '''
        cursor.execute(truncate_award_info_table)

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
        truncate_award_level_table = '''
            TRUNCATE TABLE award_level RESTART IDENTITY CASCADE;
        '''
        cursor.execute(truncate_award_level_table)

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
        truncate_award_type_table = '''
            TRUNCATE TABLE award_type RESTART IDENTITY CASCADE;
        '''
        cursor.execute(truncate_award_type_table)

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
        truncate_award_affiliation_table = '''
            TRUNCATE TABLE award_affiliation RESTART IDENTITY CASCADE;
        '''
        cursor.execute(truncate_award_affiliation_table)

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
        truncate_award_program_table = '''
            TRUNCATE TABLE award_program RESTART IDENTITY CASCADE;
        '''
        cursor.execute(truncate_award_program_table)

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
        truncate_award_term_table = '''
            TRUNCATE TABLE award_term RESTART IDENTITY CASCADE;
        '''
        cursor.execute(truncate_award_term_table)

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