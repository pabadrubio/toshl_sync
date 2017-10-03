# Pablo Abad 2017
#
# Toshl database program

import datetime


class ToshlTransfer:
    def __init__(self, date, effective_date, account, category, tag, message, amount):
        self.date = date
        self.effectiveDate = effective_date
        self.account = account
        self.category = category
        self.tag = tag
        self.message = message
        self.amount = amount

    def __str__(self):
        return "(%s, %s, %s, %s, %s, %s, %f)" % (self.date.isoformat(), self.effectiveDate.isoformat(), self.account,
                                                 self.category, self.tag, self.message, self.amount)

    def __repr__(self):
        return self.__str__()

    def searchForSimilarTransferInToshl(self):
        return None

    def sendToToshl(self, token):
        pass
