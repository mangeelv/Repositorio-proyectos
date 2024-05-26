import os
import json
import configuration as config
from load_data import sql_mongo_data_upload


def previous_ids():
    """Get the previous ids from the folder ids."""
    
    global product_id, people_id
    
    with open("ids/people_id.json") as file:
        people_id = json.load(file)
        
    with open("ids/product_id.json") as file:
        product_id = json.load(file)
        
    format_product_id = {}    
    
    for k,v in product_id.items():
        format_product_id[(k.split(",")[0], k.split(",")[1])] = v
        
    product_id = format_product_id
    
            
if __name__ == "__main__":
    
    if len(config.new_files_list) > 0:
        try:
            
            previous_ids()
            
                        
            sql_mongo_data_upload(config.sql_user, config.sql_password , config.lines, config.new_files_list, product_id, people_id) 
                
            os.makedirs("ids", exist_ok=True)
            
            clean_product_id = {}
            
            for k,v in product_id.items(): # Json keys can't be tuples
                clean_product_id[str(k).replace("(","").replace(")","").replace(" ","").replace("\'","")] = v
            
            with open("ids/product_id.json", "w") as file: # Save product ids
                json.dump(clean_product_id, file)
                
            with open("ids/people_id.json", "w") as file: # Save people_ids
                json.dump(people_id, file)
                
        except FileNotFoundError:
            print("The files werent found in the \"db\" directory.")

    else:
        print("No new files to insert.")