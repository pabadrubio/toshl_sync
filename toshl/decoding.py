# Pablo Abad 2017
#
# Toshl database program

import csv

from toshl.transfer import ToshlTransfer

class Decoder:
    def __init__(self, toshlDatabase, decodingFile, decodingHistoryFile):
        self._decoding_hints = self._load_decoding_file(decodingFile)
        self._decoding_history = self._load_decoding_file(decodingHistoryFile)
        self.decodingHistoryFile = decodingHistoryFile
        self.toshlDatabase = toshlDatabase

    def try_to_decode(self, csvTransfer):
        decoded_transfer = self.try_to_decode_with_hints(csvTransfer, self._decoding_hints)
        if decoded_transfer is None:
            decoded_transfer = self.try_to_decode_with_hints(csvTransfer, self._decoding_history)
        return decoded_transfer

    def decode_with_feedback(self, csvTransfer):
        # Show the transfer:
        print '-----------------------------------------------'
        print 'Account: ' + csvTransfer.account
        print 'Purpose: ' + csvTransfer.purpose
        print 'Message: ' + csvTransfer.message
        print 'Date   : ' + str(csvTransfer.date)
        print 'Amount : ' + str(csvTransfer.amount)
        print '-----------------------------------------------'
        print 'Choose a category:'
        category = self.choose_from_list(self.toshlDatabase.getCategories())
        print 'Choose a tag:'
        tag = self.choose_from_list(self.toshlDatabase.getTags())
        transfer = ToshlTransfer(csvTransfer.date, csvTransfer.effectiveDate, 'ING diba', category, tag,
                                 csvTransfer.account + ' - ' + csvTransfer.purpose + ' - ' + csvTransfer.message,
                                 csvTransfer.amount)
        # Add to history ...
        self._add_to_history_file(DecodingHint(csvTransfer.account, csvTransfer.purpose, csvTransfer.message,
                                               category, tag))
        return transfer

    def choose_from_list(self, elements):
        index = 0
        elementsPerRow = 4
        while index < len(elements):
            lastInRow = min(len(elements), index + elementsPerRow)
            while index < lastInRow:
                e = elements[index]
                print '%2d. %-30s' % (index+1, (e[:26] + '..') if len(e) > 28 else e),
                index += 1
            print ''
        selection = int(raw_input("Please choose (0 for None)"))
        return '' if (selection == 0) else elements[selection-1]

    def _load_decoding_file(self, decodingFile):
        decoding_hints = []
        with open(decodingFile, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            reader.next()  # Skip header
            for row in reader:
                hint = DecodingHint(row[0], row[1], row[2], row[3], row[4])
                decoding_hints.append(hint)
        return decoding_hints

    def try_to_decode_with_hints(self, csvTransfer, decoding_hints):
        for hint in decoding_hints:
            if hint.account not in csvTransfer.account:
                continue
            if hint.purpose not in csvTransfer.purpose:
                continue
            if hint.message not in csvTransfer.message:
                continue
            # Match found!
            transfer = ToshlTransfer(csvTransfer.date, csvTransfer.effectiveDate, 'ING diba', hint.category, hint.tag,
                                     csvTransfer.account + ' - ' + csvTransfer.purpose + ' - ' + csvTransfer.message,
                                     csvTransfer.amount)
            return transfer
        return None

    def _add_to_history_file(self, decodingHint):
        self._decoding_history.append(decodingHint)
        with open(self.decodingHistoryFile, "a") as f:
            f.write(decodingHint.account + ";" + decodingHint.purpose + ";" + decodingHint.message + ";" +
                    decodingHint.category + ";" + decodingHint.tag + '\n')


class DecodingHint:
    def __init__(self, account, purpose, message, category, tag):
        self.account = account
        self.purpose = purpose
        self.message = message
        self.category = category
        self.tag = tag

