# Pablo Abad 2017-2018
#
# Toshl database program

class BankEntry:
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
