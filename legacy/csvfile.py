# Pablo Abad 2017
#
# Toshl database program

import csv
import datetime

class CSVTransfer:
    def __init__(self, date, effectiveDate, account, message, purpose, amount):
        self.date = date
        self.effectiveDate = effectiveDate
        self.account = account
        self.message = message
        self.purpose = purpose
        self.amount = amount

    def __str__(self):
        return "(%s, %s, %s, %s, %s, %f)" % (self.date.isoformat(), self.effectiveDate.isoformat(), self.account,
                                             self.message, self.purpose, self.amount)

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def fromFileRow(row):
        date = datetime.datetime.strptime(row[0], "%d.%m.%Y").date()
        effectiveDate = datetime.datetime.strptime(row[1], "%d.%m.%Y").date()
        account = unicode(row[2], 'iso-8859-1')
        purpose = unicode(row[3], 'iso-8859-1')
        message = unicode(row[4], 'iso-8859-1')
        amount = float(row[5].replace(".","").replace(",","."))
        return CSVTransfer(date, effectiveDate, account, message, purpose, amount)

def loadCSVTransfersFile(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        while reader.next()[0] != "Buchung":
            pass
        transfers = map(lambda row : CSVTransfer.fromFileRow(row), reader)
        transfers.sort(key = lambda transfer: transfer.date)
        return transfers
