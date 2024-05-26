import os
import json
import pymysql
import pymongo
import configuration as config


def obtain_ids(document:json, document_name:str, product_id:dict, people_id:dict) -> tuple[int, bool, int, bool]:
    """Obtains the product and people ids while maintaining integrity."""
        
    gender = document_name.replace(".json","").split("_")[0].replace("db/","")
    
    not_product_id = True
    not_people_id = True
    
    if document["reviewerID"] not in people_id.keys():
        people_id[document["reviewerID"]] = len(people_id)
        
    else:
        not_people_id = False

    if (document["asin"],gender) not in product_id.keys():
        product_id[(document["asin"],gender)] = len(product_id)
        
    else:
        not_product_id = False
        
    return product_id[(document["asin"],gender)], not_product_id, product_id, people_id[document["reviewerID"]], not_people_id, people_id

def sql_prepare(conexion:pymysql.connections.Connection) -> str:
    """Creates the SQL database and tables."""
    
    db = "amazon_reviews"
    
    cursor = conexion.cursor() # Cursor
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db}")
    cursor.execute(f"USE {db}")
    
    # Create tables
    # Names
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS names ( 
                        people_id INT PRIMARY KEY,
                        ReviewerName VARCHAR(100))""")
    
    # Products
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS products (
                        product_id INT PRIMARY KEY,
                        asin VARCHAR(20),
                        gender VARCHAR(20))""")
    
    # People
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS people (
                        people_id INT PRIMARY KEY,
                        reviewerID VARCHAR(50))""")
    
    # Reviews
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS product_reviews (
                        product_id INT,
                        people_id INT,
                        helpful_1 INT,
                        helpful_2 INT,
                        overall FLOAT,
                        unixReviewTime INT,
                        reviewTime VARCHAR(20),
                        PRIMARY KEY (product_id, people_id),
                        FOREIGN KEY (product_id) REFERENCES products(product_id),
                        FOREIGN KEY (people_id) REFERENCES people(people_id))""")
    
    cursor.close()
    
    return db

def insert_data(conexion:pymysql.connections.Connection, collection:pymongo, file_path:str, read_lines:int, db:str, product_id:dict, people_id:dict) -> None:
    """Inserts data from the files to SQL and MongoDB databases."""
    
    cursor = conexion.cursor()
    
    cursor.execute(f"USE {db}") # Select database
    
    with open(file_path, "r") as file:
            if read_lines != -1:
                for _ in range(read_lines):
                                    
                    line = file.readline().strip()
                    
                    if line:
                        document = json.loads(line) # LOAD LINE
                        
                        product_id_val, not_product_id, product_id, people_id_val, not_people_id, people_id = obtain_ids(document, file_path, product_id, people_id) # Obtener ids
                        
                        new_document = { # Insert MongoDB
                            "product_id": product_id_val,
                            "people_id": people_id_val,
                            "reviewText": document["reviewText"],
                            "summary": document["summary"],
                            "filename":file_path.replace(".csv","").split("_")[0].replace("db/","")
                        }
                        
                        collection.insert_one(new_document)
                        
                        # Insert SQL
                        try: # Names
                            if not_people_id:
                                cursor.execute("""INSERT INTO names (people_id, ReviewerName) 
                                                    VALUES (%s,%s)""", [people_id_val, document["reviewerName"]])
                            
                        except KeyError as e:
                            print(e)
                            
                        # Products
                        if not_product_id:
                            cursor.execute("""INSERT INTO products (product_id, asin, gender)
                                                VALUES (%s, %s, %s)""", [product_id_val, document["asin"], file_path.replace(".csv","").split("_")[0].replace("db/","")])
                        
                        # People
                        if not_people_id:
                            cursor.execute("""INSERT INTO people (people_id, reviewerID)
                                                VALUES (%s, %s)""", [people_id_val, document["reviewerID"]])
                        
                        # Reviews
                        cursor.execute("""INSERT INTO product_reviews (product_id, people_id, helpful_1, helpful_2, overall, unixReviewTime, reviewTime)
                                            VALUES (%s, %s, %s, %s, %s, %s, %s)""", [product_id_val, people_id_val, document["helpful"][0], document["helpful"][1], document["overall"], document["unixReviewTime"], document["reviewTime"]])
                                                
            else:
                for line in file:
                    
                    if line.strip():
                        document = json.loads(line) # LOAD LINE
                        
                        product_id_val, not_product_id, product_id, people_id_val, not_people_id, people_id = obtain_ids(document, file_path, product_id, people_id) # Obtener ids
                        
                        new_document = { # Insert MongoDB
                            "product_id": product_id_val,
                            "people_id": people_id_val,
                            "reviewText": document["reviewText"],
                            "summary": document["summary"],
                            "filename":file_path.replace(".csv","").split("_")[0].replace("db/","")
                        }
                        
                        collection.insert_one(new_document)
                        
                        # Insert SQL
                        try: # Names
                            if not_people_id:
                                cursor.execute("""INSERT INTO names (people_id, ReviewerName) 
                                                    VALUES (%s,%s)""", [people_id_val, document["reviewerName"]])
                            
                        except KeyError as e:
                            print(e)
                            
                        # Products
                        if not_product_id:
                            cursor.execute("""INSERT INTO products (product_id, asin, gender)
                                                VALUES (%s, %s, %s)""", [product_id_val, document["asin"], file_path.replace(".csv","").split("_")[0].replace("db/","")])
                        
                        # People
                        if not_people_id:
                            cursor.execute("""INSERT INTO people (people_id, reviewerID)
                                                VALUES (%s, %s)""", [people_id_val, document["reviewerID"]])
                        
                        # Reviews
                        cursor.execute("""INSERT INTO product_reviews (product_id, people_id, helpful_1, helpful_2, overall, unixReviewTime, reviewTime)
                                            VALUES (%s, %s, %s, %s, %s, %s, %s)""", [product_id_val, people_id_val, document["helpful"][0], document["helpful"][1], document["overall"], document["unixReviewTime"], document["reviewTime"]])
                                                
    conexion.commit()
    
    cursor.close()  
    
def sql_mongo_data_upload(user:str, password:str, read_lines:int, files:list[str], product_id:dict, people_id:dict):
    """Creates sql and mongo databases and uploads data from files to them."""

    conexion = pymysql.connect(
    host = "localhost",
    user = user,
    password = password,
    )
    
    db_name = sql_prepare(conexion) # Create SQL database
        
    client = pymongo.MongoClient("mongodb://localhost:27017/") # MongoDB conexion
    db = client[db_name]
    collection = db["reviews"]
    
    for file in files: # Upload data
        insert_data(conexion, collection, file, read_lines, db_name, product_id, people_id)
        

if __name__ == "__main__":
    
    product_id = {}
    people_id = {}
    
    sql_mongo_data_upload(config.sql_user, config.sql_password , config.lines, config.files_list, product_id, people_id) 
        
    os.makedirs("ids", exist_ok=True)
    
    clean_product_id = {}
    
    for k,v in product_id.items(): # Json keys can't be tuples
        clean_product_id[str(k).replace("(","").replace(")","").replace(" ","").replace("\'","")] = v
    
    with open("ids/product_id.json", "w") as file: # Save product ids
        json.dump(clean_product_id, file)
        
    with open("ids/people_id.json", "w") as file: # Save people_ids
        json.dump(people_id, file)