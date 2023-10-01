import datetime 
import requests
import time
import json
from django.http import HttpResponse
def generate_order_number(pk):
    current_date = datetime.date.today().strftime('%Y%m%d%H%M%S')
    order_number = f'MUNCHIES{current_date}{str(pk)}'
    return order_number


def check_callback(order):
    desired_transaction = order.order_number
    callback_url = 'https://thekultureke.com/api/mpesa_transactions'
    
    while True:
        all_transactions = requests.get(callback_url)
        response_data = all_transactions.json()
        print(response_data)
        
        # Ensure response_data is a list of dictionaries
        if isinstance(response_data, list) and all(isinstance(item, dict) for item in response_data):
            # Iterate through the transactions in the response
            transaction_found = False
            for transaction in response_data:
                if transaction.get('transaction_reference') == desired_transaction:
                    print('Transaction found:', transaction)
                    transaction_found = True
                    break  # Exit the loop once the transaction is found
            
            if transaction_found:
                return HttpResponse('Payment successful')
        
        # Wait for some time before checking again (adjust the sleep duration as needed)
        time.sleep(10)


        
    
    
    