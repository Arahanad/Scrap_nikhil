import mysql.connector
from helper_class import *

class DATABASE():

    def __init__(self):

        self.hostaddress = 'localhost'
        self.username = 'root'
        self.password = '   '
        
        self.database = 'user'
        self.port = '3306'
        self.mydb = ''
        self.mycursor = ''

        #tables
        self.connection = ''
        self.tb_data_1 = 'bizex'

        self.is_db_initialzed = False


    def connect_sql(self):  

        if self.is_db_initialzed:
            return True

        print("Connecting to MySQL Server at: " , self.hostaddress)

        self.mydb = mysql.connector.connect(
            host=self.hostaddress, 
            user=self.username, 
            passwd=self.password, 
            database=self.database 
        )
        self.mycursor = self.mydb.cursor()
        self.is_db_initialzed = True

        print("Successfully Conencted to Database")


    def getting_all_tables(self):
        print("Getting all tables..")
        all_tables = []

        command = "show tables;"
        self.execute_sql(command)

        data = self.mycursor.fetchall()
        for tb in data:
            all_tables.append(tb[0])

        return all_tables

    def close_db(self):

        if self.is_db_initialzed:
            self.mydb.close()
            self.mycursor.close()
            self.is_db_initialzed = False

    def is_listing_exists(self, listing_id):
        command = '''SELECT * FROM bizex where website_url like %s ''' 

        val = [listing_id]

        self.execute_sql(command,val)
        records = self.mycursor.fetchone() 

        return records
    

    def insert_new_listing(self, listing_hash, title, description, industry, location, 
            asking_price, revenue, ebitda, cash_flow, agent_name, agent_company,
            agent_phone, website_url
        ):


        command = '''INSERT into bizex (hash, title, description, industry, location, 
                                    asking_price, revenue, ebitda, cash_flow, agent_name, agent_company, 
                                    agent_phone, website_url) \
                            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '''
                            
        val = [ listing_hash, title, description, industry, location, asking_price, revenue, ebitda, cash_flow, agent_name, agent_company, agent_phone, website_url]

        self.execute_sql(command,val)
        self.committing_sql()
        # print()
        # print('*'*50)
        # print("1 record inserted, ID:" , str(self.mycursor.lastrowid))
        # print(str(self.mycursor.rowcount) , "record inserted.")
        # print('*'*50)
        # print()
        return self.mycursor.lastrowid

    def updating_listing(self, listing_hash, title, description, asking_price, 
            revenue, ebitda, cash_flow, agent_name, agent_company, agent_phone, website_url, listing_db_id, current_datetime
        ):

        command = ''' UPDATE bizex SET  hash = %s, title = %s, description = %s, asking_price = %s, revenue = %s, ebitda = %s, cash_flow = %s, agent_name = %s, agent_company = %s, agent_phone = %s, website_url= %s, updated_at = %s where id=%s ''' 
        val = [listing_hash, title, description, asking_price, revenue, ebitda, cash_flow, agent_name, agent_company, agent_phone, website_url, current_datetime, listing_db_id]

        self.execute_sql(command,val)
        # print('*'*20)
        # print(self.mycursor.rowcount, "record updated.")
        # print('*'*20)
        self.committing_sql()

        # print("Data Updated in DB Successfully...")
        # print('#'*50)

    def execute_sql(self,sql, val):
        #print("Command: ", command)

        self.mycursor.execute(sql, val)

        return self.mycursor

    def committing_sql(self):
        # print("Committing the Command")
        self.mydb.commit()



if __name__ == "__main__":
    handle = DATABASE()
    handle.connect_sql()
    print(handle.getting_all_tables())
    handle.close_db()