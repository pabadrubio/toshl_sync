# Pablo Abad 2017-2018
#
# Toshl database program

import csv
import cPickle
from difflib import SequenceMatcher
import os
import os.path
from shutil import copyfile

def longest_common_substring(a, b):
    match = SequenceMatcher(None, a, b).find_longest_match(0, len(a), 0, len(b))
    return a[match.a: match.a + match.size]

# Each classification group contains a list of classification substrings
class ClassificationGroup:
    def __init__(self, minimumHintLength = 6):
        self.hints = []  # List((substring, (category, tag))
        self.categoryToHint = {}  # Map((category, tag) -> [idx in accountSubStrings]
        self.minimumHintLength = minimumHintLength

    def getData(self):
        return (self.hints, self.categoryToHint, self.minimumHintLength)

    def setData(self, data):
        self.hints = data[0]
        self.categoryToHint = data[1]
        self.minimumHintLength = data[2]

    def classify(self, bankEntry):
        if len(self.hints) == 0:
            return (None, None)
        values = map(lambda hint: len(hint[0]) if hint[0] in bankEntry.account else 0, self.hints)
        maxIndex = max(xrange(len(values)), key=values.__getitem__)
        if values[maxIndex] > 0:
            return self.hints[maxIndex][1]
        else:
            return (None, None)

    def update(self, bankEntry, category, tag):
        if (category, tag) not in self.categoryToHint:
            self._addNewHint(bankEntry.account, category, tag)
            return

        categoryHints = map(lambda idx: self.hints[idx], self.categoryToHint[(category, tag)])
        lcss = map(lambda hint: longest_common_substring(hint[0], bankEntry.account), categoryHints)
        maxIndex = max(xrange(len(lcss)), key=lambda idx: len(lcss[idx]))

        hintIndexes = self.categoryToHint[(category, tag)]
        if len(lcss[maxIndex]) >= self.minimumHintLength:
            # We need to make sure reducing the lcss does not misclassify previous value.
            # In that case we add a new entry instead of replacing
            if self._checkNewHintFit(hintIndexes[maxIndex], lcss[maxIndex]):
                self.hints[hintIndexes[maxIndex]] = (lcss[maxIndex], (category, tag))
            else:
                self._addNewHint(lcss[maxIndex], category, tag)
        else:
            self._addNewHint(bankEntry.account, category, tag)

    def _addNewHint(self, account, category, tag):
        self.hints.append((account, (category, tag)))
        idx = len(self.hints) - 1
        if (category, tag) not in self.categoryToHint:
            self.categoryToHint[(category, tag)] = []
        self.categoryToHint[(category, tag)].append(idx)

    def _checkNewHintFit(self, previousHintIdx, newHint):
        # Make sure a previous hint is not classified now in a different hint, as this will be wrong
        account = self.hints[previousHintIdx][0]
        values = map(lambda hIdx: self._classifyValueWithHint(hIdx, previousHintIdx, len(newHint), account), xrange(len(self.hints)))
        maxIndex = max(xrange(len(values)), key=values.__getitem__)
        return self.hints[maxIndex][1] == self.hints[previousHintIdx][1]

    def _classifyValueWithHint(self, hintIdx, previousHintIdx, newHintLen, account):
        if (hintIdx == previousHintIdx):
            return newHintLen
        elif self.hints[hintIdx][0] in account:
            return len(self.hints[hintIdx][0])
        else:
            return 0

class SmartClassifier:
    def __init__(self, filename="", continousSave = False):
        self.expenses = ClassificationGroup()
        self.incomes = ClassificationGroup()
        self.filename = filename
        self.continousSave = continousSave
        if filename != "" and os.path.isfile(filename):
            self.load(filename)

    def classify(self, bankEntry):
        if bankEntry.amount > 0:
            return self.incomes.classify(bankEntry)
        else:
            return self.expenses.classify(bankEntry)

    def update(self, bankEntry, category, tag):
        if bankEntry.amount > 0:
            self.incomes.update(bankEntry, category, tag)
        else:
            self.expenses.update(bankEntry, category, tag)
        if self.continousSave:
            if os.path.isfile(self.filename):
                copyfile(self.filename, '_sclass.tmp')
            self.save()
            if os.path.isfile('_sclass.tmp'):
                os.remove('_sclass.tmp')

    def save(self, filename = ""):
        if filename == "":
            filename = self.filename
        f = open(filename, "wb")
        data = (self.expenses.getData(), self.incomes.getData())
        cPickle.dump(data, f)

    def load(self, filename):
        f = open(filename, "rb")
        data = cPickle.load(f)
        self.expenses.setData(data[0])
        self.incomes.setData(data[1])