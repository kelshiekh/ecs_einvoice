from __future__ import unicode_literals
from re import A
import frappe
from frappe import auth
import datetime
import json, ast, requests
from frappe.utils import money_in_words
import urllib.request


#url = 'https://system.classatrading.com/api/method/classa.functions.sales_invoice_add'
#headers = {'content-type': 'application/json; charset=utf-8'}
#response = requests.post(url, json=data , headers=headers)
#frappe.msgprint(response.text)

@frappe.whitelist()
def login():
    api_base_url = frappe.db.get_single_value('EInvoice Settings', 'api_base_url')
    id_server_base_url = frappe.db.get_single_value('EInvoice Settings', 'id_server_base_url')
    client_id = frappe.db.get_single_value('EInvoice Settings', 'client_id')
    client_secret = frappe.db.get_single_value('EInvoice Settings', 'client_secret')
    generated_access_token = frappe.db.get_single_value('EInvoice Settings', 'generated_access_token')

    
    #url = 'https://system.classatrading.com/api/method/classa.functions.sales_invoice_add'
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(id_server_base_url, data={
        'grant_type':'client_credentials',
        'client_id':client_id,
        'client_secret':client_secret,
        'scope': 'InvoicingAPI'
    } , headers=headers)
    #message = response.text(access_token)
    #print(response.json[key])
    json = response.json()
    token = ""
    for key in json:
        if key == "access_token":
            #token = json[key]
            frappe.db.sql(""" update `tabSingles` set value = '{new_token}' where doctype= 'EInvoice Settings' and field = 'generated_access_token' """.format(new_token=json[key]))
    #print(response.status_code)
    #print(response.content)
    #frappe.msgprint(api_base_url)
    pass

@frappe.whitelist()
def submit_invoice():
    '''
    api_base_url = frappe.db.get_single_value('EInvoice Settings', 'api_base_url')
    id_server_base_url = frappe.db.get_single_value('EInvoice Settings', 'id_server_base_url')
    client_id = frappe.db.get_single_value('EInvoice Settings', 'client_id')
    client_secret = frappe.db.get_single_value('EInvoice Settings', 'client_secret')
    generated_access_token = frappe.db.get_single_value('EInvoice Settings', 'generated_access_token')
    headers = {'content-type': 'application/json;charset=utf-8',
    "Authorization":"Bearer" + generated_access_token,
    "Content-Length" : "376"
    }
    response = requests.post(api_base_url, json=data  , headers=headers)
    print(response.text)
    print(response.status_code)
    print(response.content)
    #print(generated_access_token)
    #frappe.msgprint(api_base_url)
    '''
    pass
