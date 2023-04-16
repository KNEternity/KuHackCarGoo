from twilio.rest import Client
import keys
import datetime
from dateutil.relativedelta import relativedelta
import sqlite3

def send_text(target_number, text_info):
    client = Client(keys.account_sid, keys.auth_token)

    message = client.messages.create(
        body = text_info,
        from_ = keys.twilio_number,
        to = target_number
    )
    
def next_date_send():
    return (datetime.date.today() + datetime.timedelta(6*365/12)).isoformat()

def get_target_number():
    conn = sqlite3.connect('Hackathon.db')
    c = conn.cursor()
    c.execute('SELECT phone FROM users ORDER BY id DESC LIMIT 1')
    target_number = c.fetchone()[0]
    conn.close()
    return target_number

def maintenance_texts(start_date, timeframe):
    date_str = str(start_date)
    date_obj = datetime.datetime.strptime(date_str, '%m-%d-%Y')
    new_date_obj = date_obj + relativedelta(months=timeframe)
    new_date_str = new_date_obj.strftime('%m-%d-%Y')
    return(new_date_str)

def maintenances():
    target_number = get_target_number()
    conn = sqlite3.connect('Hackathon.db')
    c = conn.cursor()
    c.execute("SELECT oil_date, coolant_date, tire_alignment FROM maintenance WHERE phone = ?", (target_number))
    oil_date, coolant_date, tire_alignment = c.fetchone()
    print(oil_date, coolant_date, tire_alignment)
    conn.close()
    return [oil_date, coolant_date, tire_alignment]
                    
def main():
    number = get_target_number()
    if maintenances()[0]=='':
        oil_text=''
    else:
        oil_text = maintenance_texts(maintenances()[0],6)
        send_text(number, f'You will need to change your OIL around {oil_text}. We will send you another reminder when the date gets closer.')
    if maintenances()[1]=='':
        coolant_text=''
    else:
        coolant_text = maintenance_texts(maintenances()[1],24)
        send_text(number, f'You will need to change your COOLANT around {coolant_text}. We will send you another reminder when the date gets closer.')
    if maintenances()[2]=='':
        tire_alignment=''
    else:
        tire_alignment = maintenance_texts(maintenances()[2],18)
        send_text(number, f'You will need to adjust your TIRES around {tire_alignment}. We will send you another reminder when the date gets closer.')