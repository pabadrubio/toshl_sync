# Pablo Abad 2017-2018
#
# Toshl database program

import csv


def toFloat(unicodeValue, default):
    if len(unicodeValue) == 0:
        return default
    else:
        return float(unicodeValue)


class HintsFileClassifier:
    def __init__(self, decodingFile):
        self.decoding_hints = self._load_decoding_file(decodingFile)

    def classify(self, bankEntry):
        for hint in self.decoding_hints:
            if hint.account not in bankEntry.account:
                continue
            if hint.purpose not in bankEntry.purpose:
                continue
            if hint.message not in bankEntry.message:
                continue
            if -bankEntry.amount < hint.minValue or -bankEntry.amount > hint.maxValue:
                continue
            return hint.category, hint.tag

        return None, None

    def update(self, bankEntry, category, tag):
        pass

    def _load_decoding_file(self, decodingFile):
        decoding_hints = []
        with open(decodingFile, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            reader.next()  # Skip header
            for row in reader:
                hint = DecodingHint(unicode(row[0], 'iso-8859-1'),
                                    unicode(row[1], 'iso-8859-1'),
                                    unicode(row[2], 'iso-8859-1'),
                                    toFloat(unicode(row[3], 'iso-8859-1'), float("-inf")),
                                    toFloat(unicode(row[4], 'iso-8859-1'), float("+inf")),
                                    unicode(row[5], 'iso-8859-1'),
                                    unicode(row[6], 'iso-8859-1'))
                decoding_hints.append(hint)
        return decoding_hints

class DecodingHint:
    def __init__(self, account, purpose, message, minValue, maxValue, category, tag):
        self.account = account
        self.purpose = purpose
        self.message = message
        self.minValue = minValue
        self.maxValue = maxValue
        self.category = category
        self.tag = tag
