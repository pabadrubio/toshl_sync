# Pablo Abad 2017
#
# Toshl database program
import json, requests, datetime
from toshl.log import Log

class ToshlDatabase():
    def __init__(self, token):
        self.token = token
        self.reload()

    def reload(self):
        # Must check locale
        self.loadAccounts(self.token)
        self.loadCategories(self.token)
        self.loadTags(self.token)

    def atmCategory(self):
        return "Extraer dinero de cajero"

    def loadAccounts(self, token):
        response = requests.get('https://api.toshl.com/accounts', auth=(token, ""))
        if response.status_code == 200:
            allAccounts = response.json()
            self._accountIds = {}
            for account in allAccounts:
                self._accountIds[account["name"]] = account["id"]
            self._accounts = self._accountIds.keys()
        else:
            print response
            raise Exception("Connection error: Can not get Toshl accounts")

    def loadCategories(self, token):
        response = requests.get('https://api.toshl.com/categories?per_page=200', auth=(token, ""))
        if response.status_code == 200:
            allCategories = response.json()
            self._categoriesIds = {}
            self._categoriesIds[self.atmCategory()] = -1
            for category in allCategories:
                self._categoriesIds[category["name"]] = category["id"]
            self._categories = [self.atmCategory()] + self._categoriesIds.keys()
        else:
            print response
            raise Exception("Connection error: Can not get Toshl categories")

    def loadTags(self, token):
        response = requests.get('https://api.toshl.com/tags?per_page=200', auth=(token, ""))
        if response.status_code == 200:
            allTags = response.json()
            self._tagsIds = {}
            for tag in allTags:
                self._tagsIds[tag["name"]] = tag["id"]
            self._tags = self._tagsIds.keys()
        else:
            print response
            raise Exception("Connection error: Can not get Toshl tags")

    def getAccounts(self):
        return self._accounts

    def getCategories(self):
        return self._categories

    def getTags(self):
        return self._tags

    def getAccountsMap(self):
        return self._accountIds

    def getCategoriesMap(self):
        return self._categoriesIds

    def getTagsMap(self):
        return self._tagsIds

    def getAccountId(self, account):
        return self._accountIds[account]

    def getTagId(self, tag):
        return self._tagsIds[tag]

    def getCategoryId(self, category):
        return self._categoriesIds[category]

    def listTransfers(self, token):
        time_from = datetime.date(2017, 5, 1).isoformat()
        time_to = datetime.date(2017, 10, 1).isoformat()
        response = requests.get('https://api.toshl.com/entries?from=%s&to=%s' % (time_from,  time_to), auth=(token, ""))
        if response.status_code == 200:
            entries = response.json()
            for entry in entries:
                print entry

    def addCategory(self, category, type):
        payload = {u'name': category,
                   u'type': type}
        Log.debug('Adding category to Toshl: ' + str(payload))
        response = requests.post('https://api.toshl.com/categories', json=payload, auth=(self.token, ""))
        if response.status_code != 201:
            Log.debug('Error sending data to Toshl')
            Log.debug(' Status code: ' + str(response.status_code))
            Log.debug(' Payload: ' + response.content)
            exit(1)
        else:
            Log.debug('Category successfully added to Toshl')
            self.reload()

    def addTag(self, tag, type, categoryId):
        payload = {u'name': tag,
                   u'type': type,
                   u'category': categoryId}
        Log.debug('Adding Tag to Toshl: ' + str(payload))
        response = requests.post('https://api.toshl.com/tags', json=payload, auth=(self.token, ""))
        if response.status_code != 201:
            Log.debug('Error sending data to Toshl')
            Log.debug(' Status code: ' + str(response.status_code))
            Log.debug(' Payload: ' + response.content)
            exit(1)
        else:
            Log.debug('Tag successfully added to Toshl')
            self.reload()