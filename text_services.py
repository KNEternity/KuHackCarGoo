from twilio.rest import Client
import keys
import datetime
from dateutil.relativedelta import relativedelta

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
    target_number = '+13167681963'
    return target_number

def maintenance_texts(start_date, timeframe):
    dates = (start_date.split('-'))
    dates[2] = int(dates[2])
    dates[2] += timeframe
    dates[2] = str(dates[2])
    return dates


def main():
    number = get_target_number()
    texts = 'Hi! You have just signed up for CarGO maintenance services! Reply STOP to unsubscribe'
    
    preset_date = maintenance_texts('2023-04-15', 0)
    print(preset_date)
    current_date = str(datetime.date.today()).split('-')
    print(current_date)
    if current_date == preset_date:
        send_text(number, texts)
        print (True)
    

main()
