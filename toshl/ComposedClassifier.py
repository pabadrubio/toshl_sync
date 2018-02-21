# Pablo Abad 2017
#
# Toshl database program

class ComposedClassifier:
    def __init__(self, classifiers):
        self.classifiers = classifiers

    def classify(self, bankEntry):
        for classifier in self.classifiers:
            result = classifier.classify(bankEntry)
            if result[0] is not None:
                return result
        return None, None

    def update(self, bankEntry, category, tag):
        for classifier in self.classifiers:
            classifier.update(bankEntry, category, tag)
