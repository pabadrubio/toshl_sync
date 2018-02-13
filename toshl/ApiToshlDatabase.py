# Pablo Abad 2017
#
# Toshl database program

import datetime
from ToshlEntry import ToshlEntry

class ApiToshlDatabase():
    def __init__(self, api):
        self.api = api
        self._accountIds = {}
        self._accounts = []
        self._categoriesIds = {}
        self._categories = []
        self._tagsIds = {}
        self._tags = []
        self._reload()

    def getCategories(self):
        return self._categories

    def getTags(self):
        return self._tags

    def addCategory(self, category, type):
        self.api.addCategory(category, type)
        self.reload()

    def addTag(self, tag, type, category):
        categoryId = self._getCategoryId(category)
        self.api.addTag(tag, type, categoryId)
        self.reload()

    def getSimilarEntry(self, toshlEntry):
        timeFrom = (toshlEntry.date - datetime.timedelta(days=1)).isoformat()
        timeTo = (toshlEntry.date + datetime.timedelta(days=1)).isoformat()
        entries = self.api.getTransfers(timeFrom, timeTo)
        for entry in entries:
            # We check basically only amount similarity
            if ApiToshlDatabase.isCloseAmount(entry["amount"], toshlEntry.amount) and \
                    entry["account"] == self._getAccountId(toshlEntry.account):

                transferDate = datetime.datetime.strptime(entry["date"], "%Y-%m-%d").date()
                transferMatch = ToshlEntry(date=transferDate,
                                           effectiveDate=transferDate,
                                           account=toshlEntry.account,
                                           category=toshlEntry.category,
                                           tag=toshlEntry.tag,
                                           message=entry["desc"],
                                           amount=entry["amount"])
                return transferMatch

        return None

    def addEntry(self, toshlEntry):
        isATMExtract = (toshlEntry.category == self._atmCategory())
        if isATMExtract:
            self.api.addAtmEntry(amount= toshlEntry.amount,
                                 date= toshlEntry.date,
                                 message= toshlEntry.message,
                                 categoryId= self._getCategoryId(toshlEntry.category),
                                 tagId= self._getTagId(toshlEntry.tag),
                                 accountId= self._getAccountId(toshlEntry.account),
                                 cashAccountId= self._getAccountId("Efectivo"))

        else:
            self.api.addEntry(amount=toshlEntry.amount,
                              date=toshlEntry.date,
                              message=toshlEntry.message,
                              categoryId=self._getCategoryId(toshlEntry.category),
                              tagId=self._getTagId(toshlEntry.tag),
                              accountId=self._getAccountId(toshlEntry.account))

    def _reload(self):
        self._loadAccounts()
        self._loadCategories()
        self._loadTags()

    def _atmCategory(self):
        return "Extraer dinero de cajero"

    def _loadAccounts(self):
        allAccounts = self.api.loadAccounts()
        self._accountIds = {}
        for account in allAccounts:
            self._accountIds[account["name"]] = account["id"]
        self._accounts = self._accountIds.keys()

    def _loadCategories(self):
        allCategories = self.api.loadCategories()
        self._categoriesIds = {}
        for category in allCategories:
            self._categoriesIds[category["name"]] = category["id"]
        self._categories = [self._atmCategory()] + self._categoriesIds.keys()
        self._categoriesIds[self._atmCategory()] = -1

    def _loadTags(self):
        allTags = self.api.loadTags()
        self._tagsIds = {}
        for tag in allTags:
            self._tagsIds[tag["name"]] = tag["id"]
        self._tags = self._tagsIds.keys()

    def _getAccountId(self, account):
        return self._accountIds[account]

    def _getTagId(self, tag):
        return self._tagsIds[tag]

    def _getCategoryId(self, category):
        return self._categoriesIds[category]

    @staticmethod
    def isCloseAmount(a, b, rel_tol=1e-09, abs_tol=0.0):
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
