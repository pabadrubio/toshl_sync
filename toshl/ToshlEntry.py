# Pablo Abad 2017
#
# Toshl database program

class ToshlEntry:
    def __init__(self, date, effectiveDate, account, category, tag, message, amount):
        self.date = date
        self.effectiveDate = effectiveDate
        self.account = account
        self.category = category
        self.tag = tag
        self.message = message
        self.amount = amount

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

    def prettyPrint(self, io):
        io.stdout('Account:  ' + self.account)
        io.stdout('Date:     ' + self.date.isoformat())
        io.stdout('Category: ' + self.category)
        io.stdout('Tag:      ' + self.tag)
        io.stdout('Desc.:    ' + self.message)
        io.stdout('Amount:   ' + str(self.amount))
