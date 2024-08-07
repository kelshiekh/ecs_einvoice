from __future__ import unicode_literals
from re import A
import frappe
from frappe import auth
import datetime
import json, ast, requests
from frappe.utils import money_in_words
import urllib.request
from datetime import datetime, timedelta
from json import dumps
import pytz



@frappe.whitelist()
def test(name):
    api_base_url = frappe.db.get_single_value('EInvoice Settings', 'api_base_url')
    id_server_base_url = frappe.db.get_single_value('EInvoice Settings', 'id_server_base_url')
    client_id = frappe.db.get_single_value('EInvoice Settings', 'client_id')
    client_secret = frappe.db.get_single_value('EInvoice Settings', 'client_secret')
    generated_access_token = frappe.db.get_single_value('EInvoice Settings', 'generated_access_token')
    environment = frappe.db.get_single_value('EInvoice Settings', 'environment')
    activity_code = frappe.db.get_single_value('EInvoice Settings', 'activity_code')
    company_type = frappe.db.get_single_value('EInvoice Settings', 'company_type')
    company = frappe.db.get_single_value('EInvoice Settings', 'company')
    tax_id = frappe.db.get_single_value('EInvoice Settings', 'tax_id')
    branch_id = frappe.db.get_single_value('EInvoice Settings', 'branch_id')
    country = frappe.db.get_single_value('EInvoice Settings', 'country')
    governate = frappe.db.get_single_value('EInvoice Settings', 'governate')
    region_city = frappe.db.get_single_value('EInvoice Settings', 'region_city')
    street = frappe.db.get_single_value('EInvoice Settings', 'street')
    building_number = frappe.db.get_single_value('EInvoice Settings', 'building_number')
    postal_code = frappe.db.get_single_value('EInvoice Settings', 'postal_code')
    floor = frappe.db.get_single_value('EInvoice Settings', 'floor')
    room = frappe.db.get_single_value('EInvoice Settings', 'room')
    landmark = frappe.db.get_single_value('EInvoice Settings', 'landmark')
    additional_info = frappe.db.get_single_value('EInvoice Settings', 'additional_info')
    data = {}
    documents = []
    temp = {}


    ## Enviroment
    if environment == "Pre-Production":
        documentTypeVersion = "0.9"
    else:
        documentTypeVersion = "1.0"
    temp["documentTypeVersion"] = documentTypeVersion
    

    
    ## Document Type Invoice , Credit Note, Debit Note
    invoice = frappe.get_doc("Sales Invoice", name)
    if invoice.is_return == 0 and invoice.is_debit_note ==0 :
        temp["documentType"] = "I"

    elif invoice.is_return == 1:
        temp["documentType"] = "C"
      
    elif invoice.is_debit_note ==1:
        temp["documentType"] = "D"
       

    ## activity Code
    temp["taxpayerActivityCode"]= activity_code

    # Invoice Data
    invoice = frappe.get_doc("Sales Invoice", name)
    temp["internalID"] = name
    temp["dateTimeIssued"] = str(invoice.posting_date)+ "T"+ str(invoice.posting_time + timedelta(hours=-2))  +"Z" #"2022-03-11T02:04:45Z"#str(invoice.creation)
    temp["purchaseOrderReference"] = invoice.po_no
    temp["purchaseOrderDescription"] = str(invoice.po_date)
    #so = frappe.db.sql(""" select sales_order from `tabSales Invoice Item` where parent = '{parent}'  """.format(parent=invoice.name),as_dict=0)
    #if so :
    #    temp["salesOrderReference"] = so[0][0]
    #    so_detail = frappe.get_doc("Sales Order", so[0][0])
    #    temp["salesOrderDescription"] = str(so_detail.transaction_date)
    temp["proformaInvoiceNumber"] = "Null"

    

    
    temp["signatures"] = [
                {
                    "signatureType": "I",
                    "value": "MIIGywYJKoZIhvcNAQcCoIIGvDCCBrgCAQMxDTALBglghkgBZQMEAgEwCwYJKoZIhvcNAQcFoIID/zCCA/swggLjoAMCAQICEEFkOqRVlVar0F0n3FZOLiIwDQYJKoZIhvcNAQELBQAwSTELMAkGA1UEBhMCRUcxFDASBgNVBAoTC0VneXB0IFRydXN0MSQwIgYDVQQDExtFZ3lwdCBUcnVzdCBDb3Jwb3JhdGUgQ0EgRzIwHhcNMjAwMzMxMDAwMDAwWhcNMjEwMzMwMjM1OTU5WjBgMRUwEwYDVQQKFAxFZ3lwdCBUcnVzdCAxGDAWBgNVBGEUD1ZBVEVHLTExMzMxNzcxMzELMAkGA1UEBhMCRUcxIDAeBgNVBAMMF1Rlc3QgU2VhbGluZyBEZW1vIHVzZXIyMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApmVGVJtpImeq\u002BtIJiVWSkIEEOTIcnG1XNYQOYtf5\u002BDg9eF5H5x1wkgR2G7dvWVXrTsdNv2Q\u002Bgvml9SdfWxlYxaljg2AuBrsHFjYVEAQFI37EW2K7tbMT7bfxwT1M5tbjxnkTTK12cgwxPr2LBNhHpfXp8SNyWCxpk6eyJb87DveVwCLbAGGXO9mhDj62glVTrCFit7mHC6bZ6MOMAp013B8No9c8xnrKQiOb4Tm2GxBYHFwEcfYUGZNltGZNdVUtu6ty\u002BNTrSRRC/dILeGHgz6/2pgQPk5OFYRTRHRNVNo\u002BjG\u002BnurUYkSWxA4I9CmsVt2FdeBeuvRFs/U1I\u002BieKg1wIDAQABo4HHMIHEMAkGA1UdEwQCMAAwVAYDVR0fBE0wSzBJoEegRYZDaHR0cDovL21wa2ljcmwuZWd5cHR0cnVzdC5jb20vRWd5cHRUcnVzdENvcnBvcmF0ZUNBRzIvTGF0ZXN0Q1JMLmNybDAdBgNVHQ4EFgQUqzFDImtytsUbghbmtnl2/k4d5jEwEQYJYIZIAYb4QgEBBAQDAgeAMB8GA1UdIwQYMBaAFCInP8ziUIPmu86XJUWXspKN3LsFMA4GA1UdDwEB/wQEAwIGwDANBgkqhkiG9w0BAQsFAAOCAQEAxE3KpyYlPy/e3\u002B6jfz5RqlLhRLppWpRlKYUvH1uIhCNRuWaYYRchw1xe3jn7bLKbNrUmey\u002BMRwp1hZptkxFMYKTIEnNjOKCrLmVIuPFcfLXAQFq5vgLDSbnUhG/r5D\u002B50ndPucyUPhX3gw8gFlA1R\u002BtdNEoeKqYSo9v3p5qNANq12OuZbkhPg6sAD4dojWoNdlkc8J2ML0eq4a5AQvb4yZVb\u002BezqJyqKj83RekRZi0kMxoIm8l82CN8I/Bmp6VVNJRhQKhSeb7ShpdkZcMwcfKdDw6LW02/XcmzVl8NBBbLjKSJ/jxdL1RxPPza7RbGqSx9pfyav5\u002BAxO9sXnXXc5jGCApIwggKOAgEBMF0wSTELMAkGA1UEBhMCRUcxFDASBgNVBAoTC0VneXB0IFRydXN0MSQwIgYDVQQDExtFZ3lwdCBUcnVzdCBDb3Jwb3JhdGUgQ0EgRzICEEFkOqRVlVar0F0n3FZOLiIwCwYJYIZIAWUDBAIBoIIBCjAYBgkqhkiG9w0BCQMxCwYJKoZIhvcNAQcFMBwGCSqGSIb3DQEJBTEPFw0yMTAyMDEyMzUwMjFaMC8GCSqGSIb3DQEJBDEiBCD5bGXJu9uJZIPMGXK98UrHzJM/V2U/WAO6BErxpX5wdTCBngYLKoZIhvcNAQkQAi8xgY4wgYswgYgwgYUEIAJA8uO/ek3l9i3ZOgRtPhGWwwFYljbeJ7yAgEnyYNCWMGEwTaBLMEkxCzAJBgNVBAYTAkVHMRQwEgYDVQQKEwtFZ3lwdCBUcnVzdDEkMCIGA1UEAxMbRWd5cHQgVHJ1c3QgQ29ycG9yYXRlIENBIEcyAhBBZDqkVZVWq9BdJ9xWTi4iMAsGCSqGSIb3DQEBAQSCAQB13E1WX\u002BzbWppfJi3DBK9MMSB1TXuxcNkGXQ19OcRUUAaAe2K\u002BisobYrUCZbi3ygc2AWOMyafboxjjomzrnvXKrFgspT4wAFPYaAGFzKWq\u002BW/nqMhIqJVIpS/NM7Al4HvuBA5iGuZEQFusElB0yIxOIiYDI4v8Ilkff4/duj/V2CNaN5cqXLOpL5RP6Y5i\u002BVsPGb89t/L0dSIldGN0JqaqarqYo5/RwsUFJJq01DFpPGNbOIX3gSCDmycfhJPS9csnne9Zt\u002BabNpja5ZR6KA8JMe4DHes7FDZqHBNHdC\u002BRDXT4crqmnyiJjizULu6MqDc0Fv3vrMMWDLRlwDecgq7i"
                }
    ]
    
    temp["issuer"] = {
                "address": {
                    "branchID": branch_id,
                    "country": country,
                    "governate": governate,
                    "regionCity": region_city,
                    "street": street,
                    "buildingNumber": building_number,
                    "postalCode": postal_code,
                    "floor": floor,
                    "room": room,
                    "landmark": landmark,
                    "additionalInformation": additional_info
                },
                "type": company_type,
                "id": tax_id,
                "name": company
            }
    c_address = frappe.get_doc("Address", invoice.customer_address)
    customer = frappe.get_doc("Customer" , invoice.customer)
    if customer.customer_type =="Company":
        customer_type= "B"
    else:
        customer_type= "A"
    temp["receiver"] = {
                "address": {
                    "country": c_address.county,
                    "governate": c_address.state,
                    "regionCity": c_address.city,
                    "street": c_address.address_line1,
                    "buildingNumber": c_address.building_number,
                    "postalCode": c_address.pincode,
                    "floor": c_address.floor,
                    "room": c_address.room,
                    "landmark": c_address.landmark,
                    "additionalInformation": c_address.additional_info
                },
                "type": customer_type,
                "id": customer.tax_id,
                "name": customer.customer_name
            }
            
    invoiceLines =[]
    for x in invoice.items:
        item_tax_rate = frappe.db.sql(""" select tax_rate from `tabItem Tax Template Detail` where parent = '{parent}' """.format(parent=x.item_tax_template), as_dict=0)
        salesTotal = round((x.rate + x.discount_amount), 5)
        invoiceLines.append({
            "description": x.item_name,
            "itemType": x.eta_item_type,
            "itemCode": x.eta_item_code,
            "unitType": x.uom,
            "quantity": x.qty,
            "internalCode": x.item_code,


    
            "salesTotal": round((salesTotal * x.qty), 5),
            "total": round(((x.rate + (x.rate*item_tax_rate[0][0]/100))*x.qty), 5),
            "valueDifference": 0.00,
            "totalTaxableFees": 0,
            "netTotal": round(x.amount, 5),
            "itemsDiscount": round((x.discount_amount * x.qty), 5),
            "unitValue": {
                        "currencySold": invoice.currency,
                        "amountEGP": round(salesTotal, 5)
                    },
            "discount": {
                        "rate": round(x.discount_percentage, 5),
                        "amount": round((x.discount_amount * x.qty), 5)
                    },
            "taxableItems": [
                        {
                            "taxType": x.tax_code,
                            "amount": round((x.net_amount*item_tax_rate[0][0]/100), 5),
                            "subType": "V009",
                            "rate": item_tax_rate[0][0]
                        },
            ]
        })

    
    temp["invoiceLines"] = invoiceLines

    temp["taxTotals"] = [
                {
                    "taxType": "T1",
                    "amount": round(invoice.total_taxes_and_charges,5)
                }
            ]
    total_discount = 0
    for z in invoice.items:
        total_discount += (z.discount_amount * z.qty)

    temp["totalAmount"] = round(invoice.grand_total,5)
    temp["totalDiscountAmount"] = round(total_discount,5)
    temp["netAmount"] = round(invoice.net_total,5)
    temp["extraDiscountAmount"] = round(invoice.discount_amount,5)
    temp["totalItemsDiscountAmount"] = round(total_discount,5)

    new_total =0
    for v in invoice.items:
        new_total += (v.qty*v.rate)+ (v.qty*v.discount_amount)
    
    temp["totalSalesAmount"] = round(new_total,5)
    


    #Append temp dict into document list then assign document to data
    documents.append(temp)

    data['documents'] = documents
    
    #frappe.msgprint(json.dumps(data))

    headers = {'content-type': 'application/json;charset=utf-8',
    "Authorization":"Bearer " + generated_access_token,
    "Content-Length" : "376"
    }
    response = requests.post(api_base_url, data=json.dumps(data)  , headers=headers)
    frappe.msgprint(json.dumps(data))
    #return response
    frappe.msgprint(response.content)
    #jsons = response.json()
    #for key in jsons:
    #    if key == "acceptedDocuments":
    #        frappe.msgprint(jsons[key])
    