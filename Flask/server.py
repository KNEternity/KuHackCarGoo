from flask import Flask, render_template, request, redirect, url_for
import re
from main import *

app = Flask(__name__)

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
        
        with open('numbers.txt', 'w') as numbers:
            numbers.write(phone_number)
            
        return redirect(url_for('form2', phone_number=phone_number))
    return render_template('form1.html')



@app.route('/form2', methods=['GET', 'POST'])
def form2():
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
        coolant_change_date = request.form.get('coolant_change_date')
        tire_alignment_date = request.form.get('tire_alignment_date')
        if oil_change and not oil_change_date:
            return render_template('form2.html', error='Please enter the date of your last oil change')
        if coolant_change and not coolant_change_date:
            return render_template('form2.html', error='Please enter the date of your last coolant change')
        if tire_alignment and not tire_alignment_date:
            return render_template('form2.html', error='Please enter the date of your last tire alignment')
        
        if oil_change == False and coolant_change == False and tire_alignment == False:
            return render_template('form2.html', error='Please choose an option')
        
        test_list = []
        test_list.append(oil_change_date)
        test_list.append(coolant_change_date)
        test_list.append(tire_alignment_date)
        res = [str(i or '') for i in test_list]
        
        if (res[0]+res[1]+res[2]).isalpha():
            return render_template('form2.html', error='Please check the formatting')
        
        if not ('-' in (res[0]+res[1]+res[2])):
            return render_template('form2.html', error='Please check the formatting')
        with open('dates.txt', 'w') as dates:
            for i in res:
                dates.write(i + '\n')

        main()
        return redirect('/thanks')

    return render_template('form2.html', oil_change=oil_change, coolant_change=coolant_change, tire_alignment=tire_alignment, oil_change_date=oil_change_date, coolant_change_date=coolant_change_date, tire_alignment_date=tire_alignment_date)

@app.route('/thanks', methods=['GET', 'POST'])
def thanks():
    return render_template('thanks.html')


if __name__ == '__main__':
    app.run(debug=True)
    
