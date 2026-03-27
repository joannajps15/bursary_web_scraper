#Libraries
import psycopg2
from psycopg2 import Error
from flask import abort
from create_scrape_result_tables import *

connection = None
cursor = None


def query_db(filters) -> str:

    connection = None
    cursor = None
    res = []

    try:
        #connect to db
        connection = psycopg2.connect(user="postgres",
                                    password="postGres#321",
                                    host="127.0.0.1",
                                    port="5432",
                                    database="web_scraper_db")    

        cursor = connection.cursor()

        if (not filters):
            # query the db, given the params and return results
            db_query = '''
                SELECT 
                    info.award_id,
                    info.award_name,
                    info.link, 
                    info.selection, 
                    info.citizen_status,
                    info.value_desc, 
                    info.award_desc,
                    info.eligibility_selection,
                    array_agg(DISTINCT levels.award_level) AS levels,
                    array_agg(DISTINCT types.award_type)  AS types,
                    array_agg(DISTINCT program.award_program) AS programs,
                    array_agg(DISTINCT term.award_term) AS terms,
                    array_agg(DISTINCT affil.award_affiliation) AS affiliations
                FROM award_info AS info
                LEFT JOIN award_level AS levels ON levels.award_id = info.award_id
                LEFT JOIN award_type AS types ON types.award_id = info.award_id
                LEFT JOIN award_program AS program ON program.award_id = info.award_id
                LEFT JOIN award_term AS term ON term.award_id = info.award_id
                LEFT JOIN award_affiliation AS affil ON affil.award_id = info.award_id
                GROUP BY info.award_id;
            '''
            cursor.execute(db_query)
            res = cursor.fetchall()
        
        else:
            # 0: pre-query all programs matching faculty filter
            if 'All' not in filters['faculty']:
                program_query = '''
                    SELECT program from program 
                    WHERE faculty = ANY(%s)
                '''
                cursor.execute(program_query, filters['faculty'])
                program_result = cursor.fetchall() # list of programs corresponding to faculty
                filters['program'].extend(program_result)
            filters.pop('faculty')

            # 1:many db award_id aggregation
            keys = list(filters.keys())
            award_tables = ['award_type', 'award_level', 'award_affiliation', 'award_program', 'award_term', 'award_info']
            params = []
            filter_id_query = ""

            for i in range(len(keys)):
                if 'All' not in filters[keys[i]]:
                    if len(filter_id_query) > 0: filter_id_query += " UNION "
                    filter_id_query += "SELECT DISTINCT award_id FROM " + award_tables[i]
                    filter_id_query += " WHERE " + award_tables[i] + " = ANY (%s)"
                    params.append(filters[keys[i]])                   

            #2:left-join on results            
            db_query = f'''
                SELECT 
                    info.award_id,
                    info.award_name,
                    info.link, 
                    info.selection, 
                    info.citizen_status,
                    info.value_desc, 
                    info.award_desc,
                    info.eligibility_selection,
                    array_agg(DISTINCT levels.award_level) AS levels,
                    array_agg(DISTINCT types.award_type)  AS types,
                    array_agg(DISTINCT program.award_program) AS programs,
                    array_agg(DISTINCT term.award_term) AS terms,
                    array_agg(DISTINCT affil.award_affiliation) AS affiliations
                FROM award_info AS info
                JOIN ({filter_id_query}) AS filter_id_result ON filter_id_result.award_id = info.award_id
                LEFT JOIN award_level AS levels ON levels.award_id = info.award_id
                LEFT JOIN award_type AS types ON types.award_id = info.award_id
                LEFT JOIN award_program AS program ON program.award_id = info.award_id
                LEFT JOIN award_term AS term ON term.award_id = info.award_id
                LEFT JOIN award_affiliation AS affil ON affil.award_id = info.award_id
                GROUP BY info.award_id
            '''
            cursor.execute(db_query, params)
            res = cursor.fetchall()

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        connection.rollback()
        abort(500)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    
    return res