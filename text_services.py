from twilio.rest import Client
import keys
import datetime
from dateutil.relativedelta import relativedelta


def send_initial_text(target_number):
    client = Client(keys.account_sid, keys.auth_token)

    message = client.messages.create(
        body = 'Hi! You have just signed up for CarGO maintenance services! Reply STOP to unsubscribe',
        from_ = keys.twilio_number,
        to = target_number
    )

    print(message.body)
    
def next_date_send():
    return (datetime.date.today() + datetime.timedelta(6*365/12)).isoformat()

def get_target_number():
    target_number = '+13167681963'
    return target_number

def maintenance_texts(start_date, timeframe):
    dates = (start_date.split('-'))
    for i in range(len(dates)):
        dates[i] = int(dates[i])
    date = datetime.date(dates[2], dates[0], dates[1])
    next_date = date + relativedelta(months=timeframe)
    new_date = next_date.strftime("%m-%d-%Y")
    return new_date




def main():
    number = get_target_number()
    send_initial_text(number)
    print('Done')
    
print(maintenance_texts('4-14-2023', 6))
