# Pablo Abad 2017
#
# Toshl database program

import datetime, requests
from legacy.log import Log

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

class ToshlTransfer:
    def __init__(self, date, effective_date, account, category, tag, message, amount):
        self.date = date
        self.effectiveDate = effective_date
        self.account = account
        self.category = category
        self.tag = tag
        self.message = message
        self.amount = amount
        self._currency = {u'rate': 1.0, u'code': u'EUR', u'main_rate': 1.0, u'fixed': False}

    def __str__(self):
        ustr = "(%s, %s, %s, %s, %s, %s, %f)" % (self.date.isoformat(),
                                                 self.effectiveDate.isoformat(),
                                                 self.account.encode('utf-8'),
                                                 self.category.encode('utf-8'),
                                                 self.tag.encode('utf-8'),
                                                 self.message.encode('utf-8'),
                                                 self.amount)
        return ustr

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def isCloseAmount(a, b, rel_tol=1e-09, abs_tol=0.0):
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

    def searchForSimilarTransferInToshl(self, token, database):
        time_from = (self.date - datetime.timedelta(days=1)).isoformat()
        time_to = (self.date + datetime.timedelta(days=1)).isoformat()
        categories = database._getCategoryId(self.category) if self.category != "" else ""
        tags = database._getTagId(self.tag) if self.tag != "" else ""
        response = requests.get('https://api.toshl.com/entries?from=%s&to=%s' % (time_from, time_to),
                                auth=(token, ""))
        if response.status_code == 200:
            entries = response.json()
            for entry in entries:
                if ApiToshlDatabase.isCloseAmount(entry["amount"], self.amount): # We check basically only amount similarity
                    transfer_date = datetime.datetime.strptime(entry["date"], "%Y-%m-%d").date()
                    transferMatch = ToshlTransfer(transfer_date, transfer_date, self.account, self.category, self.tag,
                                                  entry["desc"], entry["amount"])
                    return transferMatch

        return None

    def prettyPrint(self):
        print 'Account:  ' + self.account
        print 'Date:     ' + self.date.isoformat()
        print 'Category: ' + self.category
        print 'Tag:      ' + self.tag
        print 'Desc.:    ' + self.message
        print 'Amount:   ' + str(self.amount)

    def sendToToshl(self, token, database):
        isATMExtract = (self.category == database.atmCategory())
        if isATMExtract:
            cashAccount = database._getAccountId("Efectivo")
            payload = {u'amount': self.amount,
                       u'currency': self._currency,
                       u'date': self.date.isoformat(),
                       u'desc': self.message,
                       u'account': database._getAccountId(self.account),
                       u'transaction': {
                           u'account': cashAccount,
                           u'currency': self._currency
                       }}

        else:
            payload = {u'amount': self.amount,
                       u'currency': self._currency,
                       u'date': self.date.isoformat(),
                       u'desc': self.message,
                       u'account': database._getAccountId(self.account)}

            if self.tag != '':
                payload[u'tags'] = [database._getTagId(self.tag)]

            if self.category != '':
                payload[u'category'] = database._getCategoryId(self.category)

        Log.debug('Sending transfer to Toshl: ' + str(payload))
        response = requests.post('https://api.toshl.com/entries', json=payload, auth=(token, ""))
        if response.status_code != 201:
            Log.debug('Error sending data to Toshl')
            Log.debug(' Status code: ' + str(response.status_code))
            Log.debug(' Payload: ' + response.content)
            exit(1)
        else:
            Log.debug('Transfer successfully writen to Toshl')
