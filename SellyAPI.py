# -*- coding: utf-8 -*-
"""
Created on Sat May 19 19:50:32 2018

@author: Kate
"""

import requests
import json

class SellyAPI:
    def __init__(self,key,email):
        self.email = email
        self.key = key
        self.URL = 'https://selly.gg/api/v2/'
        
    def create(self,action,data,params={}):
        httpResp = requests.post(self.URL+action, auth=(self.email, self.key), 
                                 data=data, params=params)
        if httpResp.status_code == 200:
            return httpResp.text
        else:
            return (httpResp.status_code, httpResp.reason, httpResp.text) 
        
    def getInfo(self,action,data={},params={}):
        httpResp = requests.get(self.URL+action, auth=(self.email, self.key), 
                                 data=data, params=params)
        if httpResp.status_code == 200:
            return httpResp.text
        else:
            return (httpResp.status_code, httpResp.reason, httpResp.text)
    
    def updateInfo(self,action,data,params={}):
        httpResp = requests.put(self.URL+action, auth=(self.email, self.key), 
                                 data=data, params=params)
        if httpResp.status_code == 200:
            return httpResp.text
        else:
            return (httpResp.status_code, httpResp.reason, httpResp.text)
    
    def getAllCoupons(self):
        return self.getInfo('/coupons')
    
    def getCoupon(self, ID):
        return self.getInfo('/coupons/{}'.format(ID))
    
    def createCoupon(self, code, discount, pidList):
        data = {'coupon':{'code': code, 'discount': discount, 'product_ids':pidList}}     
        return self.create('/coupons', data)
               
    def updateCoupon(self, couponID, newCode, discount):
        data = {'coupon':{'code':newCode, 'discount': discount }}
        return self.updateInfo('/coupons/{}'.format(couponID), data)

    def orderStatus(number):
        statuses = {'0':'No payment has been received', 
                    '51':'PayPal dispute or reversal',
                    '52':'Order blocked due to risk level exceeding the maximum for the product',
                    '53':'Partial payment. When crypto currency orders do not receive the full amount required due to fees, etc',
                    '54':'Crypto currency transaction confirming',
                    '55':'Payment pending on PayPal. Most commonly due to e-checks.',
                    '56':'Refunded',
                    '100':'Payment Complete'
                    }
        return statuses[str(number)]
    
    def getOrder(self,ID):
        return self.getInfo('/orders/{}'.format(ID))
    
    def getAllOrders(self):
        return self.getInfo('/orders').json()

    def getProduct(self, PID):
        return self.getInfo('/products/{}'.format(PID))
    
    def getAllProducts(self):
        return self.getInfo('/products')

    def createProduct(self, title, description, stock, price, currency, 
                      productSerials, productType=2, bitcoin=False, ethereum=False, 
                      paypal=False, stripe=False, litecoin=False, dash=False, 
                      perfectMoney=False, bitcoinCash = False, ripple=False, 
                      private=False, unlisted=False,
                      sellerNote="Thank you for your purchase",
                      maxQuantity=None, minQuantity=1, custom={}):
        
        data = {
                "product":{
                    "title": title,
                    "description": description,
                    "stock": stock,
                    "price": price,
                    "currency": currency,
                    "product_type": productType,
                    "info":productSerials,
                    "bitcoin": bitcoin,
                    "paypal": paypal,
                    "stripe": stripe,
                    "litecoin": litecoin,
                    "dash": dash,
                    "ethereum": ethereum,
                    "perfect_money": perfectMoney,
                    "bitcoin_cash": bitcoinCash,
                    "ripple": ripple,
                    "private": private,
                    "unlisted": unlisted,
                    "seller_note": sellerNote,
                    "maximum_quantity": maxQuantity,
                    "minimum_quantity": minQuantity,
                    "custom": custom
                    }
                }

        return self.create('/products', data)
    
    def updateProduct(self, PID, title, description, stock, price, currency, 
                      productSerials, productType=2, bitcoin=False, ethereum=False, 
                      paypal=False, stripe=False, litecoin=False, dash=False, 
                      perfectMoney=False, bitcoinCash = False, ripple=False, 
                      private=False, unlisted=False,
                      sellerNote="Thank you for your purchase",
                      maxQuantity= None, minQuantity=1, custom={}):
        
        data = {"product": {"title": title,
                "description": description,
                "stock": stock,
                "price": price,
                "currency": currency,
                "info": productSerials,
                "product_type": productType,
                "bitcoin": bitcoin,
                "paypal": paypal,
                "stripe": stripe,
                "litecoin": litecoin,
                "dash": dash,
                "ethereum": ethereum,
                "perfect_money": perfectMoney,
                "bitcoin_cash": bitcoinCash,
                "ripple": ripple,
                "private": private,
                "unlisted": unlisted,
                "seller_note": sellerNote,
                "maximum_quantity": maxQuantity,
                "minimum_quantity": minQuantity,
                "custom": custom
                }}

        return self.updateInfo('/products/{}'.format(PID), data)
            
    def addStock(self, PID, amount, serialCodes):
        if len(serialCodes) > amount:
            print ('ERROR: You have inputted {} too many serial codes'.format(len(serialCodes)-amount))
        elif len(serialCodes) < amount:
            print ('ERRORL You have inputted {} too few serial codes').format(amount-len(serialCodes))
        else:
            product = self.getProduct(PID)
            productSerials = ', '.join(serialCodes)
            self.updateProduct(PID, product['title'], product['description'], product['stock']+amount, 
              product['price'], product['currency'], 
              productSerials, productType=product['product_type'], 
              bitcoin=product['bitcoin'], ethereum=product['ethereum'], 
              paypal=product['paypal'], stripe=product['stripe'], 
              litecoin=product['litecoin'], dash=product['litecoin'], 
              perfectMoney=product['perfect_money'], 
              bitcoinCash=product['bitcoin_cash'], 
              ripple=product['ripple'], private=product['private'], 
              unlisted=product['unlisted'], sellerNote=product['seller_note'],
              maxQuantity=product['maximum_quantity'], 
              minQuantity=product['minimum_quantity'], custom=product['custom'])