from flask import Flask, render_template, request, redirect, url_for
import re
import threading
from twilio.rest import Client
import keys
import datetime
from dateutil.relativedelta import relativedelta
import sqlite3

from twilio.rest import Client
import keys
import datetime

app = Flask(__name__)

con = sqlite3.connect('Hackathon.db')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users
            (phone, oil, coolant, tire)''')
con.commit()
con.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form1', methods=['GET', 'POST'])
def form1():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        if not re.match(r'^\+[1-9]\d{1,14}$', phone_number) or len(phone_number) != 12:
            return render_template('form1.html', error='Invalid phone number format. Please enter a number in the format +13161234567.')
        
        try:
            send_text(phone_number, 'Hi! Welcome to CarGOO!')
        except:
            return render_template('form1.html', error='Invalid phone number. Make sure you enetered your number correctly!')
        
        def run_thread():
            con = sqlite3.connect('Hackathon.db')
            cur = con.cursor()
            cur.execute(f'''INSERT OR IGNORE INTO users (phone, oil, coolant, tire) VALUES (?, NULL, NULL, NULL)''', (phone_number,))
            con.commit()
            con.close()
            
        thread = threading.Thread(target=run_thread)
        thread.start()
        thread.join()
        
        return redirect(url_for('form2', phone_number=phone_number))
    return render_template('form1.html')


@app.route('/form2', methods=['GET', 'POST'])
def form2():
    phone_number = request.args.get('phone_number', '')
    oil_change = False
    coolant_change = False
    tire_alignment = False
    oil_change_date = ''
    coolant_change_date = ''
    tire_alignment_date = ''

    if request.method == 'POST':
        if 'oil_change' in request.form:
            oil_change = True
        if 'coolant_change' in request.form:
            coolant_change = True
        if 'tire_alignment' in request.form:
            tire_alignment = True
        oil_change_date = request.form.get('oil_change_date')
        print(oil_change_date)
        coolant_change_date = request.form.get('coolant_change_date')
        print(coolant_change_date)
        tire_alignment_date = request.form.get('tire_alignment_date')
        print(tire_alignment_date)

        if oil_change and not oil_change_date:
            return render_template('form2.html', error='Please enter the date of your last oil change')
        if coolant_change and not coolant_change_date:
            return render_template('form2.html', error='Please enter the date of your last coolant change')
        if tire_alignment and not tire_alignment_date:
            return render_template('form2.html', error='Please enter the date of your last tire alignment')
        
        if oil_change == False and coolant_change == False and tire_alignment == False:
            return render_template('form2.html', error='Please choose an option')
        
        if (oil_change_date+coolant_change_date+tire_alignment_date).isalpha():
            return render_template('form2.html', error='Please check the formatting')
        
        if not ('-' in (oil_change_date+coolant_change_date+tire_alignment_date)):
            return render_template('form2.html', error='Please check the formatting')
    
        initial_texts()
        def run_thread():
            con = sqlite3.connect('Hackathon.db')
            cur = con.cursor()
            cur.execute(f'''UPDATE users SET oil = {oil_change_date}, coolant = {coolant_change_date}, tire = {tire_alignment_date} WHERE phone = {phone_number}''')
            con.commit()
            con.close()
                
        thread = threading.Thread(target=run_thread)
        thread.start()
        thread.join()
        return redirect('/thanks')

    return render_template('form2.html', oil_change=oil_change, coolant_change=coolant_change, tire_alignment=tire_alignment, oil_change_date=oil_change_date, coolant_change_date=coolant_change_date, tire_alignment_date=tire_alignment_date)

@app.route('/thanks', methods=['GET', 'POST'])
def thanks():
    return render_template('thanks.html')


def send_text(target_number, text_info):
    client = Client(keys.account_sid, keys.auth_token)

    message = client.messages.create(
        body = text_info,
        from_ = keys.twilio_number,
        to = target_number
    )
    

def get_target_number():
    conn = sqlite3.connect('Hackathon.db')
    cur = conn.cursor()
    for i in cur.execute('''SELECT phone FROM users'''):
                target_number = i[0]
    conn.close()
    return target_number

def maintenance_texts(start_date, timeframe):
    raise ValueError(start_date)
    date_str = str(start_date)
    raise ValueError(date_str)
    date_obj = datetime.datetime.strptime(date_str.replace('-', ' '), '%m %d %Y')
    new_date_obj = date_obj + relativedelta(months=timeframe)
    new_date_str = new_date_obj.strftime('%m-%d-%Y')
    return new_date_str

def maintenances(number):
    target_number =number
    conn = sqlite3.connect('Hackathon.db')
    c = conn.cursor()
    c.execute(f"SELECT oil, coolant, tire FROM users WHERE phone = '{target_number}'") 
    oil_date, coolant_date, tire_alignment = c.fetchone()
    conn.close()
    return [oil_date, coolant_date, tire_alignment]
                    
def initial_texts():
    number = get_target_number()
    if maintenances(number)[0]=='':
        oil_text=''
    else:
        oil_text = maintenance_texts(maintenances(number)[0],6)
        send_text(number, f'You will need to change your OIL around {oil_text}. We will send you another reminder when the date gets closer.')
    if maintenances(number)[1]== '':
        coolant_text=''
    else:
        coolant_text = maintenance_texts(maintenances(number)[1],24)
        send_text(number, f'You will need to change your COOLANT around {coolant_text}. We will send you another reminder when the date gets closer.')
    if maintenances(number)[2]=='':
        tire_alignment=''
    else:
        tire_alignment = maintenance_texts(maintenances(number)[2],18)
        send_text(number, f'You will need to adjust your TIRES around {tire_alignment}. We will send you another reminder when the date gets closer.')
    return

if __name__ == '__main__':

    app.run(debug=True)