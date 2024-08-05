from datetime import datetime
import psycopg2
import random
import json
import uuid
from config import getParameters

# Simulating database connection (Replace with actual database operations)
def get_db_connection():
    try:
        conn = psycopg2.connect(host='localhost', dbname='snack_serenity', user='postgres', password='frank123', port='5432')
        return conn
    except Exception as e:
        print("Error establishing database connection:", str(e))
        return None


def check_existing_user(mobile):
    try:
        existing_user = True
        print("Checking existing user or not")
        conn = get_db_connection()
        if conn is None:
            return False  # Return false if the connection couldn't be established
        cursor = conn.cursor()
        fetch_query = "SELECT mobile_number FROM public.user_master WHERE mobile_number = %s"
        cursor.execute(fetch_query, (str(mobile),))
        result = cursor.fetchall()
        if len(result) == 0:
            existing_user = False
            # Insert user if not exists
            insert_query = "INSERT INTO public.user_master (user_uuid, mobile_number) VALUES (%s, %s)"
            cursor.execute(insert_query, (str(uuid.uuid4()), str(mobile)))
            conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error while checking existing user: {e}")
        return False
    return existing_user

def read_write_transaction(jsonfile, mobile):
    try:
        print("Updating OTP.")
        conn = get_db_connection()
        if conn is None:
            return False  # Return false if the connection couldn't be established
        cursor = conn.cursor()
        otp_data = {"otp": jsonfile['otp']}  # Store OTP as a JSON object
        query = "UPDATE public.user_master SET otp_key=%s WHERE mobile_number=%s"
        value = (json.dumps(otp_data), str(mobile))
        cursor.execute(query, value)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error in read_write_transaction: {e}")
        return False

def send_sms(mobile_number):
    try:
        print("Sending the SMS")
        otp = generate_otp()
        otp_log_date = str(datetime.now())
        return True, otp, otp_log_date
    except Exception as e:
        print(f"Error while sending SMS: {e}")
        return False, None, None

def generate_otp():
    try:
        print("Generating OTP.")
        otp_number = random.randint(100000, 999999)
        return otp_number
    except Exception as e:
        print(f"Error while generating OTP: {e}")
        return None
    
    
def create_user_with_otp(mobile, otp):
    try:
        print("Inserting new user with OTP")
        conn = get_db_connection()
        if conn is None:
            return False  # Return false if the connection couldn't be established
        cursor = conn.cursor()
        otp_data = {"otp": otp}
        insert_query = """
            INSERT INTO public.user_master (mobile_number, otp_key)
            VALUES (%s, %s)
            ON CONFLICT (mobile_number) 
            DO UPDATE SET otp_key = EXCLUDED.otp_key, updated_at = CURRENT_TIMESTAMP;
        """
        cursor.execute(insert_query, (str(mobile), json.dumps(otp_data)))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error while inserting user with OTP: {e}")
        return False
