from multiprocessing import Pool
from langdetect import detect
import pymysql
import json

def english_filter(obj):
    try:
        if obj[2] != "No description" and detect(obj[1])!= "ru" and detect(obj[2]) != "ru": 
            return {"ID":obj[0],"TITLE": obj[1],"DESCRIPTION": obj[2],"MATERIAL":obj[3],"COLOR":obj[4]}
    except:
        print(obj)

if __name__ == '__main__':
    user  = "newton_admin"
    pass_word = "uJ8vB7gC8ylO9e"
    host = "178.159.45.204" 
    db_name = "newton"

    connection  = pymysql.connect(host=host,user=user,passwd=pass_word,database=db_name)
    cursor = connection.cursor()
    request_to_db = """SELECT op.model, od.name, od.description, atr.material, atr.color 
    FROM `oc_product` as op 
    JOIN oc_product_description as od 
    ON od.product_id = op.product_id and od.language_id = 2 
    JOIN 
        (SELECT DISTINCT ocp.product_id, 
            (SELECT text from oc_product_attribute Where attribute_id = 15 
                and product_id = ocp.product_id and language_id =2) as material, 
            (SELECT text from oc_product_attribute Where attribute_id = 33 
                and product_id = ocp.product_id and language_id =2) as color 
                FROM oc_product_attribute as ocp WHERE language_id=2) as atr 
    ON od.product_id = atr.product_id"""

    cursor.execute(request_to_db)
    ex = list(cursor.fetchall())
    with Pool(4) as p:
        res = p.map(english_filter,ex)
        
    with open("full_res_from_db.json","w+",encoding="utf-8") as file:
        json.dump(res,file) 