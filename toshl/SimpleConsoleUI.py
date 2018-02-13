# Pablo Abad 2017
#
# Toshl database program

class SimpleConsoleUI():
    def __init__(self, io, database):
        self.io = io
        self.database = database

    def classifyManually(self, bankEntry):
        # Show the entry:
        self.io.stdout('-----------------------------------------------')
        self.io.stdout('Account: ' + bankEntry.account)
        self.io.stdout('Purpose: ' + bankEntry.purpose)
        self.io.stdout('Message: ' + bankEntry.message)
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


    def _choose_from_list(self, elements, label, create_function):
        index = 0
        elementsPerRow = 4
        while index < len(elements):
            lastInRow = min(len(elements), index + elementsPerRow)
            while index < lastInRow:
                e = elements[index]
                self.io.stdoutnnl('%2d. %-30s' % (index+1, ((e[:26] + '..') if len(e) > 28 else e)))
                index += 1
            self.io.stdout('')

        selection = self.io.getString("Please choose (E for skip, N for None, G to add a new expense type, I for a new Income type)")
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
        else:
            selectionIdx = int(selection)
            return elements[selectionIdx-1]

    def _choose_category_from_list(self, elements):
        return self._choose_from_list(elements, "category", lambda name, t: self.database.addCategory(name, t))

    def _choose_tag_from_list(self, elements, category):
        return self._choose_from_list(elements, "tag", lambda name, t: self.database.addTag(name, t, category))
