# Pablo Abad 2017
#
# Toshl database program

from ToshlEntry import ToshlEntry

class ToshlSyncApp:

    def __init__(self, database, classifier, ui, io, account, doAskForOverwrite=False):
        self.database = database
        self.classifier = classifier
        self.ui = ui
        self.doAskForOverwrite = doAskForOverwrite
        self.io = io
        self.account = account

    def sync(self, bankEntries):
        for entry in bankEntries:
            self.handleEntry(entry)

    def handleEntry(self, bankEntry):
        manuallyClassified = False
        category, tag = self.classifier.classify(bankEntry)
        if category is None:
            category, tag = self.ui.classifyManually(bankEntry)
            manuallyClassified = True

        if category is not None:
            toshlEntry = self._createToshlEntry(bankEntry, category, tag)
            similarEntry = self.database.getSimilarEntry(toshlEntry)
            if similarEntry is not None and self.askForOverwrite(similarEntry) == False:
                self.io.log("Skipping entry because to a similar transfer was found.")
                return
            else:
                self.database.addEntry(toshlEntry)
                if manuallyClassified:
                    self.classifier.update(bankEntry, category, tag)
        else:
            self.io.log("Skipping transfer")

    def askForOverwrite(self, toshlEntry):
        if self.doAskForOverwrite:
            self.ui.askForOverwrite(toshlEntry)
        else:
            return False

    def _createToshlEntry(self, bankEntry, category, tag):
        transferMatch = ToshlEntry(date=bankEntry.date,
                                   effectiveDate=bankEntry.effectiveDate,
                                   account=self.account,
                                   category=category,
                                   tag=tag,
                                   message=bankEntry.account + ' - ' + bankEntry.purpose + ' - ' + bankEntry.message,
                                   amount=bankEntry.amount)
        return transferMatch