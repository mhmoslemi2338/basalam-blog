import psycopg2
from pandas import DataFrame
import datetime
from app.toELASTIC import to_elastic

DB_host="localhost"
DB_name="post_log"
DB_user="postgres"
DB_pass="111"
DB_port="5432"


def create_TABLE():
    psql_conn=psycopg2.connect(dbname=DB_name,user=DB_user,
                            password=DB_pass,host=DB_host,port=DB_port)
    
    
    psql_cur=psql_conn.cursor()
    try:
    
        psql_cur.execute(""" CREATE TABLE all_posts (
                id bigserial primary key not null, 
                title VARCHAR(250) not null,
                body TEXT not null,
                likes   INT not null,
                comment TEXT[][] not null,
                createdate TIMESTAMP not null,
                likedate TIMESTAMP[][],
                commentdate TIMESTAMP[][]
                );
        """)
        
        psql_conn.commit()
    except:
        pass
    
    psql_cur.close()
    psql_conn.close()
    return




def add_post_psql(tmp):
    psql_conn=psycopg2.connect(dbname=DB_name,user=DB_user,
                            password=DB_pass,host=DB_host,port=DB_port)
    
    
    psql_cur=psql_conn.cursor()

    now = datetime.datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

    psql_cur.execute("""INSERT INTO all_posts (title,body,likes,comment,createdate)
                     VALUES(%s,%s,%s,%s,%s)""", 
                     ( tmp["title"]  ,tmp["body"],tmp["likes"],tmp["comment"],dt_string,))
    psql_conn.commit()

    psql_cur.execute('select MAX(id) from all_posts;')
    psql_conn.commit()
    id=psql_cur.fetchall()
    id=id[0][0]

    psql_cur.close()
    psql_conn.close()

    to_elastic(id)
    return



def all_DB():
    psql_conn=psycopg2.connect(dbname=DB_name,user=DB_user,
                            password=DB_pass,host=DB_host,port=DB_port)
    psql_cur=psql_conn.cursor()

    psql_cur.execute("SELECT * FROM all_posts;")

    tmp=psql_cur.fetchall()
    
    col_names = []
    for elt in psql_cur.description:
        col_names.append(elt[0])
    
    # Create the dataframe, passing in the list of col_names extracted from the description
    df = DataFrame(tmp, columns=col_names)

    psql_cur.close()
    psql_conn.close()
    
    return df.to_dict('records')


def get_single_post(id):
    psql_conn=psycopg2.connect(dbname=DB_name,user=DB_user,
                            password=DB_pass,host=DB_host,port=DB_port)
    psql_cur=psql_conn.cursor()
    my_id="'" + str(id) + "'"
    psql_cur.execute("SELECT * FROM all_posts where id=%s;"  %my_id)
    tmp=psql_cur.fetchall()
    
    col_names = []
    for elt in psql_cur.description:
        col_names.append(elt[0])
    df = DataFrame(tmp, columns=col_names)

    psql_cur.close()
    psql_conn.close()
    
    return df.to_dict('records')




def DB_like_post(id):
    psql_conn=psycopg2.connect(dbname=DB_name,user=DB_user,
                            password=DB_pass,host=DB_host,port=DB_port)
    
    psql_cur=psql_conn.cursor()   
    my_id="'" + str(id) + "'"
    psql_cur.execute("SELECT likes,likedate FROM all_posts where id=%s;"  %my_id)
    tmp=psql_cur.fetchall()
    if tmp!=[]:
        like=tmp[0][0]
        likedate_tmp=tmp[0][1]
        now = datetime.datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")  
        if likedate_tmp==None:
            in2="'{"+dt_string+"}'"
        else:
            element=''           
            for row in likedate_tmp:
                try:
                    tmp=row.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    tmp=row[0].strftime("%Y-%m-%d %H:%M:%S")
                tmp='{'+tmp+'},'
                element=element+tmp
            element=element+"{"+dt_string+"}"
            in2="'{"+element+"}'"   
    
  
        psql_cur.execute("""
                         UPDATE all_posts
                         SET likes = %s,
                             likedate = %s
                         WHERE id = %s;
                         """ %(like+1,in2,my_id,))
        psql_conn.commit()
    

        psql_cur.close()
        psql_conn.close()

        to_elastic(id)
        return 1   
    else:
        psql_cur.close()
        psql_conn.close() 
        return 0
            


def DB_comment_post(incomment):
    body=incomment["body"]
    id=incomment["id"]
    psql_conn=psycopg2.connect(dbname=DB_name,user=DB_user,
                            password=DB_pass,host=DB_host,port=DB_port)
    
    psql_cur=psql_conn.cursor()   
    my_id="'" + str(id) + "'"
    psql_cur.execute("SELECT comment,commentdate FROM all_posts where id=%s;"  %my_id)
    tmp=psql_cur.fetchall()
    
    if tmp!=[]:
        comment=tmp[0][0]
        commentdate_tmp=tmp[0][1]
        now = datetime.datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")  
        if commentdate_tmp==None:
            in2="'{"+dt_string+"}'"
        else:
            element=''           
            for row in commentdate_tmp:
                try:
                    tmp=row.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    tmp=row[0].strftime("%Y-%m-%d %H:%M:%S")
                tmp='{'+tmp+'},'
                element=element+tmp
            element=element+"{"+dt_string+"}"
            in2="'{"+element+"}'"   
    
       
        if comment==None:
            in_comment="'{"+body+"}'"
        else:
            element=''           
            for row in comment:
                tmp=row[0]
                tmp='{'+tmp+'},'
                element=element+tmp
            element=element+"{"+body+"}"
            in_comment="'{"+element+"}'" 
       
    
        psql_cur.execute("""
                         UPDATE all_posts
                         SET comment = %s,
                             commentdate = %s
                         WHERE id = %s;
                         """ %(in_comment,in2,my_id,))
        psql_conn.commit()
    

        to_elastic(id)
        psql_cur.close()
        psql_conn.close() 
        return 1   
    else:
        psql_cur.close()
        psql_conn.close() 
        return 0
        