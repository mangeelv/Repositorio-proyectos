import os
import random
import pymysql
import pandas as pd
import configuration as config
from neo4j import GraphDatabase
import os


def menu():
    """Print the menu of the program."""
    
    print(""" ========== MENU ==========
          
    1. Similarities between users with most reviews.
    2. Random products from a file, reviews and relationships.
    3. Users with different reviewed products.
    4. Popular articles and shared products.
    5. Exit.
==========================
    """)

def number_verify(number:str) -> int:
    """Verify that the input is a number"""
    
    egg = 0
    
    while number.isdigit() == False:
        number = input("Please enter a whole positive number: ").replace(" ", "") # Wrong format
        egg += 1
        
        if random.randint(1,10) == 5 or egg == 10:
            print("\nIt's not rocket science, just enter a whole positive number...\n")
            egg = 0
            
    return int(number)
            
def obtain_users_most_reviews(n_users:int, connection: pymysql.Connection):
    """Obtain the n_users with the most reviews"""
    
    cursor = connection.cursor()
    
    query = """SELECT people_id
               FROM product_reviews
               GROUP BY people_id
               ORDER BY COUNT(*) DESC
               LIMIT %s""" # Obtain n users with most reviews
               
    cursor.execute(query, [n_users])
    
    users = cursor.fetchall()
    
    clean_users = []
    
    for user in users:
        clean_users.append(user[0])
    
    cursor.close()
    
    return clean_users

def jaccard_similarity(list1:list, list2:list) -> float:
    """Calculate the Jaccard similarity between two lists"""
    
    set1 = set(list1)
    set2 = set(list2)
    
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    return intersection/union

def obtain_similar_profiles(user_ids:int, connection: pymysql.Connection):
    """Obtain the profiles that are similar to the user_id"""
    
    cursor = connection.cursor()
    
    similarities = {}
    
    for user_id in user_ids:
        
        query = """SELECT DISTINCT product_id
                   FROM product_reviews
                   WHERE product_id IN (SELECT product_id
                                        FROM product_reviews
                                        WHERE people_id = %s)""" # Obtain products reviewed by the user
                                        
        cursor.execute(query, [user_id])
        
        products = cursor.fetchall()
        
        cleaned_products = []
        
        for product in products:
            cleaned_products.append(product[0])
            
        similarities[user_id] = cleaned_products # Save the products reviewed by the user
        
    cursor.close()
    
    df_data = []
    
    jaccard_similarities = {}
    
    similarities = dict(sorted(similarities.items()))
    
    for id1 in similarities.keys():
        for id2 in similarities.keys():
            
            if id1 != id2 and id1 > id2: # Avoid duplicates
                similarity_score = jaccard_similarity(similarities[id1], similarities[id2]) # Calculate similarity
                
                df_data.append([id1, id2, similarity_score])
                jaccard_similarities[(id1, id2)] = similarity_score
    
    df = pd.DataFrame(df_data, columns=['Id1', 'Id2', 'Similarity']) 
    os.makedirs("data", exist_ok=True) 
    df.to_csv("data/similarities.csv", index=False) # Save the similarities
    
    return jaccard_similarities

def upload_similar_profiles(similarities:dict[tuple:float], user_ids:list, driver: GraphDatabase.driver):
    """Upload the similarities to the Neo4j database"""
    
    with driver.session() as session:
        query = """MATCH (n)
                   DETACH DELETE n"""
        
        session.run(query)
        
        for user_id in user_ids:
                query = """CREATE (u:User {id: $id})""" # Upload users
                
                session.run(query, id=user_id)        
            
        for key_1,key_2 in similarities.keys():
            if similarities[(key_1,key_2)] > 0:
                query = """MATCH (u1:User {id: $key1}), (u2:User {id: $key2})
                            CREATE (u1)-[:SIMILARITY {score: $score}]->(u2),
                                   (u2)-[:SIMILARITY {score: $score}]->(u1);""" # Upload similarities between users
                            
                session.run(query, key1=key_1, key2=key_2, score=similarities[(key_1,key_2)])

def similarities_work(connection: pymysql.Connection, driver: GraphDatabase.driver):
    """Main function to calculate the similarities between users, create a csv file and upload the data to Neo4j"""
    
    n_users = input("Enter the number of users to work with: ")
    n_users = number_verify(n_users)
    
    users = obtain_users_most_reviews(n_users, connection)
    print("Users obtained")
    
    similarities = obtain_similar_profiles(users, connection)
    print("Similarities obtained and saved")
    
    upload_similar_profiles(similarities, users, driver)
    print("Similarities uploaded to Neo4j")
    
    with driver.session() as session:
        
        query = """MATCH (id:User)-->(n:User)
                   WITH id, COUNT(n) AS num_neighbours
                   ORDER BY num_neighbours DESC
                   LIMIT 1
                   RETURN id, num_neighbours""" # Obtain the user with the most neighbours
        
        result = session.run(query)
        result = result.data()[0]

    print(f"The user with the most neighbours is {result['id']['id']} with {result['num_neighbours']} neighbours")
    
    
def random_products(file_name:str, random_objects:int, connection: pymysql.Connection) -> list:
    """Pick n random products from a defined file and return the ids."""
    
    cursor = connection.cursor()
    
    query = """SELECT product_id
                    FROM products
                    WHERE gender = %s""" # Obtain products
                    
    cursor.execute(query, [file_name])
    
    products = cursor.fetchall()
    
    cursor.close()
        
    random_products = random.sample(products, random_objects) # Pick x random products
    
    clean_products = []
    
    for product in random_products:
        clean_products.append(product[0])

    return clean_products

def product_reviews(connection: pymysql.Connection, product_ids:list) ->list:
    """Obtain the reviews of the products, the time and the score"""
    
    cursor = connection.cursor()
    
    reviews = {}
    
    for product_id in product_ids: 
            query = """SELECT people_id, overall, reviewTime
                    FROM product_reviews
                    WHERE product_id = %s""" # Obtain reviews
                    
            cursor.execute(query, [product_id])
            
            results = list(cursor.fetchall())
            
            reviews[product_id] = results
            
    cursor.close()
    
    return reviews

def upload_product_reviews(reviews:dict, driver: GraphDatabase.driver):
    """Upload product reviews to the Neo4j database"""
    
    with driver.session() as session:
        
        query = """MATCH (n) 
                   DETACH DELETE n"""
        
        session.run(query)
        
        for product_id in reviews.keys():
                query = """CREATE (p:Product {id: $id})""" # Upload products
                
                session.run(query, id=product_id)        
            
        for product_id in reviews.keys():
            for review in reviews[product_id]: 
                query = """CREATE (u:User {id: $user_id})""" # Upload users
                
                session.run(query, user_id=review[0])
            
            for review in reviews[product_id]: 
                query = """MATCH (p:Product {id: $product_id}), (u:User {id: $user_id})
                            CREATE (u)-[:REVIEW {score: $score, time: $time}]->(p)""" # Upload reviews
                            
                session.run(query, product_id=product_id, user_id=review[0], score=review[1], time=review[2])
            
def product_reviews_work(connection: pymysql.Connection, driver: GraphDatabase.driver):
    """Main function to upload the product reviews to the Neo4j database"""
    
    file_name = ""
    db_folder = "db"

    files = os.listdir(db_folder)
    
    relate_responses = {}

    for file in files:
        relate_responses[file.replace(".csv","").split("_")[0]] = file
        
    allowed_responses = list(relate_responses.keys())
    allowed_responses.append("Exit")

    print("\nFicheros disponibles:")
    for k, v in relate_responses.items():
        print(f"\t{k} - {v}")
        
    print("\tExit - Salir\n")
    
    file_name = ""
    
    while file_name not in allowed_responses: # Select the file to work with
        if file_name != "":
            print("Fichero no encontrado.")
            
        file_name = input("Select the file to work with: ").replace(" ", "").capitalize()

        
    if file_name != "Exit":
        
        try:
            number_of_reviews = input("Enter the number of products to upload: ")
            number_of_reviews = number_verify(number_of_reviews)
            
            products = random_products(file_name, number_of_reviews, connection)
            print("Products obtained")
            
            reviews = product_reviews(connection, products)
            print("Reviews obtained")
            
            upload_product_reviews(reviews, driver)
            print("Reviews uploaded to Neo4j")   
            
        except Exception as e:
            print(e)
                
            
def obtain_users_diff_reviews(connection: pymysql.Connection, n_users:int = 10)->tuple[dict, dict]:
    """Obtain the users with different reviews"""
    
    cursor = connection.cursor()
    
    query = """SELECT people_id
               FROM names""" # Obtain all users
               
    cursor.execute(query)
    
    id_names = cursor.fetchall()    
    
    id_clean_names = [id_name[0] for id_name in id_names]
        
    query = """SELECT DISTINCT gender, COUNT(product_id)
                FROM products
                GROUP BY gender""" # Obtain the number of products of each type
                
    cursor.execute(query)
    
    gender_count = cursor.fetchall()
    
    gender_limits = {}
    genders = []
    limits = []
    
    for i in gender_count:
        genders.append(i[0])
        limits.append(i[1])
        
    for i in range(len(genders)): # Calculate the limits of the product types
        limit = 0
        
        for j in range(i+1):
            limit += limits[j]
            
        gender_limits[genders[i]] = limit
            
    query = """SELECT GROUP_CONCAT(product_id)
               FROM product_reviews
               WHERE people_id = %s""" # Obtain the products the user has reviewed
               
    user_reviews = {}

    while n_users > 0:
        user = random.choice(id_clean_names) # Pick a random user
        
        id_clean_names.remove(user)
        
        cursor.execute(query, user)
        
        product_reviews = cursor.fetchall()
        
        product_reviews = product_reviews[0][0].split(",") # Obtain the product ids

        if len(product_reviews) > 1: # Check if the user has reviewed more than one product
            
            enough_types = set()
            
            for product_review in product_reviews:
                for i in range(len(gender_limits)):

                    if int(product_review) < gender_limits[genders[i]]: # Check the type of the product
                        enough_types.add(genders[i])
                        
                        break
                    
                if len(enough_types) > 1: # Check if the user has reviewed products of different types
                    n_users -= 1
                    
                    user_reviews[user] = product_reviews
                    
                    break
                
    return user_reviews, gender_limits

def consumed_objects(product_id:int, connection) -> int:
    """Checks number of times the product has been reviewed"""
    
    cursor = connection.cursor()
    
    query = """SELECT COUNT(*)
               FROM product_reviews
               WHERE product_id = %s""" # Obtain the number of reviews for the product
               
    cursor.execute(query, product_id)
    
    result = cursor.fetchall()
    
    cursor.close()
    
    return result[0][0]

def upload_diff_reviews(user_reviews:dict, gender_limits:dict, driver: GraphDatabase.driver, connection: pymysql.Connection):
    """Upload the users with different reviews to the Neo4j database"""
    
    with driver.session() as session:
        
        query = """MATCH (n)
                   DETACH DELETE n"""
        
        session.run(query)
        
        for user in user_reviews.keys():   
                query = """CREATE (u:User {id: $id})""" # Upload users
                
                session.run(query, id = user)
        
        genders = []
        
        for gender in gender_limits.keys():
                query = """CREATE (ot:ObjectType {gender: $gender})""" # Upload product types
                
                session.run(query, gender = gender)       
                genders.append(gender) 
            
        for user in user_reviews.keys():
            for review in user_reviews[user]:
                for i in range(len(gender_limits)):
                    
                    if review.isdigit() and int(review) < gender_limits[genders[i]]: # Check the type of the product
                        times_consumed = consumed_objects(review, connection)
                        query = """MATCH (u:User {id: $user_id}), (ot:ObjectType {gender: $gender})
                                    CREATE (u)-[:REVIEW {consumed: $times_consumed}]->(ot)""" # Upload relation user - product type
                                    
                        session.run(query,user_id = user,gender =  genders[i], times_consumed = times_consumed)
                        
                        break
                    
def diff_reviews_work(connection: pymysql.Connection, driver: GraphDatabase.driver):
    """Main function to upload the users with different reviews to the Neo4j database"""
    
    number_of_users = input("Enter the number of users to work with: ")
    number_of_users = number_verify(number_of_users)
    
    user_reviews,gender_limits = obtain_users_diff_reviews(connection, number_of_users)
    print("Users obtained")
    
    upload_diff_reviews(user_reviews, gender_limits, driver, connection)
    print("Users uploaded to Neo4j")
    
    
def extract_popular_articles(connection: pymysql.Connection) -> tuple[dict, list]:
    """Extract a number of articles beyond a threshold of reviews."""
    
    n_articles = input("Enter the number of articles to extract: ")
    n_articles = number_verify(n_articles)
    
    threshold_reviews = input("Enter the threshold of reviews: ") # Threshold of reviews
    threshold_reviews = number_verify(threshold_reviews)
    
    cursor = connection.cursor()
    
    query = """SELECT product_id, GROUP_CONCAT(people_id)
               FROM product_reviews
               GROUP BY product_id
               HAVING COUNT(*) < %s
               ORDER BY COUNT(*) DESC
               LIMIT %s""" # Obtain the n products with less reviews than the threshold
               
    cursor.execute(query, [threshold_reviews, n_articles])
    
    articles = cursor.fetchall()
    
    cursor.close()
    
    clean_articles = {}

    for article in articles: # Save the articles and the people that have reviewed them
        clean_articles[article[0]] = [int(messy_id) for messy_id in article[1].split(",")]
    
    people_ids = set()
    
    for product_id in clean_articles.keys(): # Obtain the people that have reviewed the articles
        for person in clean_articles[product_id]:
            people_ids.add(person)      
              
    people_ids = list(people_ids)
    people_ids.sort()
    
    return clean_articles, people_ids

def extract_shared_products(people_ids:list, connection: pymysql.Connection) -> dict:
    """Extract the products that have been reviewed by the same people."""
    
    cursor = connection.cursor()
    
    bought_products = {}
    
    for person in people_ids:
        
        query = """SELECT product_id
                   FROM product_reviews
                   WHERE people_id = %s""" # Obtain the products reviewed by the user
                   
        cursor.execute(query, person)
        
        products = cursor.fetchall()
        
        products = [product[0] for product in products]
        
        bought_products[person] = products # Save the products
        
    cursor.close()
    
    shared_products = {}
    
    for i in range(len(people_ids)):
        for j in range(i+1, len(people_ids)):
            
            share_product = len(set(bought_products[people_ids[i]]).intersection(set(bought_products[people_ids[j]]))) # Calculate the shared products
            
            if share_product > 0:
                shared_products[(people_ids[i], people_ids[j])] = share_product # Save the shared products between the users
            
    return shared_products

def upload_popular_arcticles_relations(articles:dict, shared_products:dict, people_ids:list, driver: GraphDatabase.driver):
    """Upload the popular articles and the shared products of the reviewers to the Neo4j database."""
        
    with driver.session() as session:
        
        query = """MATCH (n)
                   DETACH DELETE n"""
        
        session.run(query)
        
        for product in articles.keys():
            query = """CREATE (p:Product {id: $product_id})""" # Upload products
            
            session.run(query, product_id = product)
            
        for person in people_ids:
            query = """CREATE (p:Person {id: $people_id})""" # Upload users
            
            session.run(query, people_id = person)
            
        for product in articles.keys():
            for person in articles[product]:
                query = """MATCH (pro:Product {id: $product_id}), (per:Person {id: $people_id})
                            CREATE (per)-[:REVIEWED]->(pro)""" # Upload the relation user - product
                                
                session.run(query, product_id = product, people_id = person)
                
        for person_1, person_2 in shared_products.keys():
            query = """MATCH (p1:Person {id: $person_1}), (p2:Person {id: $person_2})
                        CREATE (p1)-[:SHARED_BOUGHT {products: $products}]->(p2)
                        CREATE (p2)-[:SHARED_BOUGHT {products: $products}]->(p1)""" # Upload the relation user - user with shared products
                        
            session.run(query, person_1 = person_1, person_2 = person_2, products = shared_products[(person_1, person_2)])
            
def popular_articles_work(connection: pymysql.Connection, driver: GraphDatabase.driver):
    """Main function to upload the popular articles and shared products of the reviewers to the Neo4j database."""
    
    articles, people_ids = extract_popular_articles(connection)    
    print("Articles obtained")
    
    shared_products = extract_shared_products(people_ids, connection)
    print("Shared products obtained")
    
    upload_popular_arcticles_relations(articles, shared_products, people_ids, driver)
    print("Articles and shared products uploaded to Neo4j")
    
    if len(articles) == 0:
        print("No articles were found with the given parameters.")
    

if __name__ == "__main__":
    
    connection = pymysql.connect( # SQL connection
    host = "localhost",
    user = config.sql_user,
    password = config.sql_password,
    db = "amazon_reviews"
    )
    
    uri = "neo4j://localhost:7687" # Neo4j connection
    driver = GraphDatabase.driver(uri, auth=(config.neo4j_user, config.neo4j_password))
    
    working = True
    
    print("Welcome to the Neo4j analysis program.\n")
    
    while working:
            
            menu()
            
            response = input("Enter the number of the option: ")
            response = number_verify(response)
            
            print("\n")
            
            if response == 1:
                print("\nWorking with similarities between users with most reviews...\n")
                similarities_work(connection, driver)
                
            elif response == 2:
                print("\nWorking with random products from a file, reviews and relationships...\n")
                product_reviews_work(connection, driver)
                
            elif response == 3:
                print("\nWorking with users with different reviewed products...\n")
                diff_reviews_work(connection, driver)
                
            elif response == 4:
                print("\nWorking with popular articles and shared products...\n")
                popular_articles_work(connection, driver)
                
            elif response == 5:
                working = False
                
            else:
                print("Sorry, that option has not been implemented yet.")
            
            if response != 5:
                print("\n")
            
    connection.close()
    driver.close()
    
    print("Thank you for using the Neo4j analysis program.")