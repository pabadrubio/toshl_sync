# Pablo Abad 2017-2018
#
# Toshl database program

import requests

class ToshlApi():
    def __init__(self, token, io):
        self.token = token
        self.io = io
        self._currency = {u'rate': 1.0, u'code': u'EUR', u'main_rate': 1.0, u'fixed': False}

    def loadAccounts(self):
        """ Returns a json list of accounts """
        response = requests.get('https://api.toshl.com/accounts', auth=(self.token, ""))
        if response.status_code == 200:
            return response.json()
        else:
            self.io.log("Error in APIToshlDatabase:loadAccounts - http response:" + str(response))
            raise Exception("Connection error: Can not get Toshl accounts")

    def loadCategories(self):
        """ Returns a json list of categories """
        response = requests.get('https://api.toshl.com/categories?per_page=200', auth=(self.token, ""))
        if response.status_code == 200:
            return response.json()
        else:
            self.io.log("Error in APIToshlDatabase:loadCategories - http response:" + str(response))
            raise Exception("Connection error: Can not get Toshl categories")

    def loadTags(self):
        """ Returns a json list of tags """
        response = requests.get('https://api.toshl.com/tags?per_page=200', auth=(self.token, ""))
        if response.status_code == 200:
            return response.json()
        else:
            self.io.log("Error in APIToshlDatabase:loadTags - http response:" + str(response))
            raise Exception("Connection error: Can not get Toshl tags")

    def addCategory(self, category, type):
        """ Adds a new category with the given name and type(income or expense) """
        payload = {u'name': category,
                   u'type': type}
        self.io.log('Adding category to Toshl: ' + str(payload))
        response = requests.post('https://api.toshl.com/categories', json=payload, auth=(self.token, ""))
        if response.status_code != 201:
            self.io.log('Error sending data to Toshl')
            self.io.log(' Status code: ' + str(response.status_code))
            self.io.log(' Payload: ' + response.content)
            raise Exception("Connection error: Can not add category")
        else:
            self.io.log('Category successfully added to Toshl')

    def addTag(self, tag, type, categoryId):
        payload = {u'name': tag,
                   u'type': type,
                   u'category': categoryId}
        self.io.log('Adding Tag to Toshl: ' + str(payload))
        response = requests.post('https://api.toshl.com/tags', json=payload, auth=(self.token, ""))
        if response.status_code != 201:
            self.io.log('Error sending data to Toshl')
            self.io.log(' Status code: ' + str(response.status_code))
            self.io.log(' Payload: ' + response.content)
            raise Exception("Connection error: Can not add tag")
        else:
            self.io.log('Tag successfully added to Toshl')

    def getTransfers(self, timeFrom, timeTo):
        response = requests.get('https://api.toshl.com/entries?from=%s&to=%s' % (timeFrom, timeTo),
                                auth=(self.token, ""))
        if response.status_code == 200:
            return response.json()
        else:
            return []

    def addAtmEntry(self, amount, date, message, categoryId, tagId, accountId, cashAccountId):
        payload = {u'amount': amount,
                   u'currency': self._currency,
                   u'date': date.isoformat(),
                   u'desc': message,
                   u'account': accountId,
                   u'transaction': {
                       u'account': cashAccountId,
                       u'currency': self._currency
                   },
                   u'category': categoryId,
                   u'tags': [tagId]}
        self.io.log('Sending transfer to Toshl: ' + str(payload))
        response = requests.post('https://api.toshl.com/entries', json=payload, auth=(self.token, ""))
        if response.status_code != 201:
            self.io.log('Error sending data to Toshl')
            self.io.log(' Status code: ' + str(response.status_code))
            self.io.log(' Payload: ' + response.content)
            raise Exception("Connection error: Can not add atm transfer")
        else:
            self.io.log('Entry successfully writen to Toshl')

    def addEntry(self, amount, date, message, categoryId, tagId, accountId):
        payload = {u'amount': amount,
                   u'currency': self._currency,
                   u'date': date.isoformat(),
                   u'desc': message,
                   u'account': accountId,
                   u'category': categoryId,
                   u'tags': [tagId]}
        self.io.log('Sending transfer to Toshl: ' + str(payload))
        response = requests.post('https://api.toshl.com/entries', json=payload, auth=(self.token, ""))
        if response.status_code != 201:
            self.io.log('Error sending data to Toshl')
            self.io.log(' Status code: ' + str(response.status_code))
            self.io.log(' Payload: ' + response.content)
            raise Exception("Connection error: Can not add atm transfer")
        else:
            self.io.log('Entry successfully writen to Toshl')
