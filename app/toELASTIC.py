
import psycopg2
#from psycopg2.extras import RealDictCursor

from elasticsearch import Elasticsearch
DB_host="localhost"
DB_name="post_log"
DB_user="postgres"
DB_pass="111"
DB_port="5432"


id=5

def to_elastic(id):
    psql_conn=psycopg2.connect(dbname=DB_name,user=DB_user,
                              password=DB_pass,host=DB_host,port=DB_port)
    psql_cur=psql_conn.cursor()
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    
    my_id="'" + str(id) + "'"
      
    psql_cur.execute("""with t as (
                                    select
              title,body,likes , comment , createdate,likedate,commentdate
                                    from all_posts
                                    where id=%s
                                  
                                  
                                  )
                                  select json_agg(t) from t;""" %my_id
                      )
      
    psql_conn.commit()
        
    data=psql_cur.fetchall()
    data=data[0][0]
      
    psql_cur.close()
    psql_conn.close()
    
    try:
        es.create(index="posts", id=id, body=data[0])
    except:
        es.update(index="posts",id=id, body={"doc": data[0]})
    es.close()




#es.bulk(index="posts",doc_type="_doc",id=5, body=data[0])


    


def clear_elastic():
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    es.indices.delete(index='test-index', ignore=[400, 404])
    es.close()


#clear_elastic()





#es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
#s = es.search( index="test-index")
#es.close()





