# Pablo Abad 2017-2018
#
# Toshl database program

import csv
import datetime
from BankEntry import BankEntry

class INGTransfersLoader:

    def loadTransfers(self, filename):
        """ Returns a date ordered list of BankTransfer from CSV file """
        with open(filename, 'r') as csvFile:
            reader = csv.reader(csvFile, delimiter=';')
            while reader.next()[0] != "Buchung":
                pass
            transfers = map(lambda row: INGTransfersLoader._fromFileRow(row), reader)
            transfers.sort(key=lambda transfer: transfer.date)
            return transfers

    @staticmethod
    def _fromFileRow(row):
        date = datetime.datetime.strptime(row[0], "%d.%m.%Y").date()
        effectiveDate = datetime.datetime.strptime(row[1], "%d.%m.%Y").date()
        account = unicode(row[2], 'iso-8859-1')
        purpose = unicode(row[3], 'iso-8859-1')
        message = unicode(row[4], 'iso-8859-1')
        amount = float(row[5].replace(".","").replace(",","."))
        return BankEntry(date, effectiveDate, account, message, purpose, amount)
