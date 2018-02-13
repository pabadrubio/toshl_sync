# Pablo Abad 2017
#
# Toshl database program

class FancyConsoleUI():
    def __init__(self, io, database):
        self.io = io
        self.database = database

    def classifyManually(self, bankEntry):
        # Show the entry:
        self.io.stdout('-----------------------------------------------')
        self.io.stdout('Account: ' + bankEntry.account.encode('utf-8'))
        self.io.stdout('Purpose: ' + bankEntry.purpose.encode('utf-8'))
        self.io.stdout('Message: ' + bankEntry.message.encode('utf-8'))
        self.io.stdout('Date   : ' + str(bankEntry.date))
        self.io.stdout('Amount : ' + str(bankEntry.amount))
        self.io.stdout('-----------------------------------------------')
        self.io.stdout('Choose a category:')
        category = self._choose_category_from_list(self.database.getCategories())
        if category is not None and category != '':
            self.io.stdout('Choose a tag:')
            tag = self._choose_tag_from_list(self.database.getTags(), category)
        else:
            tag = ''

        if category is None or tag is None:
            return None, None

        return category, tag

    def askForOverwrite(self, toshlEntry):
        self.io.stdout('-----------------------------------------------')
        self.io.stdout('A similar entry was found:')
        toshlEntry.prettyPrint()
        self.io.stdout('-----------------------------------------------')
        selection = self.io.getString("Overwrite? (Enter yes to overwrite)")
        return selection == "yes"

    def _escaped(self, text):
        if isinstance(text, str):
            us = unicode(text, 'utf-8')
        else:
            us = text
        escaped = us.lower().replace(u'\xe1',u'a').replace(u'\xe9',u'e').replace(u'\xed',u'i').replace(u'\xf3',u'o').replace(u'\xfa',u'u').replace(u'\xf1',u'n')
        return escaped

    def _choose_from_list(self, allElements, elementsFilter, escape_function):
        index = 0
        elementsPerRow = 4
        elements = list(filter(lambda x: self._escaped(elementsFilter) in self._escaped(x), allElements))
        while index < len(elements):
            lastInRow = min(len(elements), index + elementsPerRow)
            while index < lastInRow:
                e = elements[index]
                self.io.stdoutnnl('%2d. %-30s' % (index+1, ((e[:26] + '..') if len(e) > 28 else e)))
                index += 1
            self.io.stdout('')
        self.io.stdout('Choose: ' + elementsFilter)

        while True:
            key = self.io.getChar()
            if key == chr(27):
                selection = escape_function()
                return selection
            elif (key == chr(10) or key == chr(13)) and len(elements) == 1:
                return elements[0]
            elif '1' <= key <= '9' and len(elements) < 9:
                return elements[ord(key) - ord('1')]
            elif key == chr(8) and len(elementsFilter) > 0:
                return self._choose_from_list(allElements, elementsFilter[:-1], escape_function)
            elif 'a' <= key <= 'z' or 'A' <= key <= 'Z':
                return self._choose_from_list(allElements, elementsFilter + key.lower(), escape_function)

    def _especial_selection(self, label, create_function):
        self.io.stdoutnnl("Please choose (E for skip, N for None, G to add a new expense type, I for a new Income type)")
        selection = self.io.getChar()
        if selection.upper() == "N":
            return ''
        elif selection.upper() == "G":
            name = self.io.getString("Enter the name for the new expense " + label + ":")
            create_function(name, "expense")
            return name
        elif selection.upper() == "I":
            name = self.io.getString("Enter the name for the new income " + label + ":")
            create_function(name, "income")
            return name
        elif selection.upper() == "E":
            return None
        elif selection.upper() == "Q":
            raise KeyboardInterrupt

    def _choose_category_from_list(self, elements):
        return self._choose_from_list(elements, '', lambda: self._especial_selection("category", lambda name, t: self.database.addCategory(name, t)))

    def _choose_tag_from_list(self, elements, category):
        return self._choose_from_list(elements, '', lambda: self._especial_selection("tag", lambda name, t: self.database.addTag(name, t, category)))
