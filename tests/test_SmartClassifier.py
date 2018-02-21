# Pablo Abad 2017-2018
#
# Toshl database program

import unittest
import datetime
from toshl.SmartClassifer import ClassificationGroup, SmartClassifier, longest_common_substring
from toshl.BankEntry import BankEntry


def _entry(account, ammount = -1):
    date = datetime.date(2017, 5, 13)
    return BankEntry(date, date, account, "", "", ammount)


class LCSTest(unittest.TestCase):
    def setUp(self):
        self.longMessage = True

    def test_lcs(self):
        self.assertEqual("", longest_common_substring("", ""))
        self.assertEqual("", longest_common_substring("a", ""))
        self.assertEqual("", longest_common_substring("", "b"))
        self.assertEqual("", longest_common_substring("a", "b"))
        self.assertEqual("abcd", longest_common_substring("abcde", "tdsabcds"))


class ClassificationGroupTest(unittest.TestCase):
    def setUp(self):
        self.unit = ClassificationGroup(minimumHintLength=3)
        self.longMessage = True

    def test_empty(self):
        self.assertEqual((None, None), self.unit.classify(_entry('abcde')), 'TestBasic: Classifier failed')

    def test_basic(self):
         self.unit.update(_entry('abcde'), 'c1', 't1')
         self.assertEqual(('c1', 't1'), self.unit.classify(_entry('abcde')), 'TestBasic: Classifier failed')

    def test_negative(self):
        self.unit.update(_entry('abcde'), 'c1', 't1')
        self.assertEqual((None, None), self.unit.classify(_entry('abcd')), 'TestBasic: Classifier failed')

    def test_longest_match(self):
        self.unit.update(_entry('abcde'), 'c1', 't1')
        self.unit.update(_entry('abcdefg'), 'c1', 't2')
        self.assertEqual(('c1', 't1'), self.unit.classify(_entry('abcde')), 'TestBasic: Classifier abcde')
        self.assertEqual(('c1', 't2'), self.unit.classify(_entry('abcdefg')), 'TestBasic: Classify abcdefg')

    def test_sub_match(self):
        self.unit.update(_entry('abcde'), 'c1', 't1')
        self.assertEqual(('c1', 't1'), self.unit.classify(_entry('ooooabcdefgoooo')), 'TestBasic: Classifier failed')

    def test_hint_minimise(self):
        self.unit.update(_entry('abcff'), 'c1', 't1')
        self.assertEqual((None, None), self.unit.classify(_entry('abc')), 'TestBasic: Classifier failed before minimize')
        self.unit.update(_entry('abckk'), 'c1', 't1')
        self.assertEqual(('c1', 't1'), self.unit.classify(_entry('abc')), 'TestBasic: Classifier failed after minimize')

    def test_no_add(self):
        self.unit.update(_entry('abcdd'), 'c1', 't1')
        self.unit.update(_entry('abcd'), 'c1', 't2')
        self.unit.update(_entry('abcff'), 'c1', 't1')
        self.assertEqual(('c1', 't1'), self.unit.classify(_entry('abcdd')), 'TestBasic: abcdd failed')
        self.assertEqual(('c1', 't1'), self.unit.classify(_entry('abc')), 'TestBasic: abc failed')
        self.assertEqual(('c1', 't2'), self.unit.classify(_entry('abcd')), 'TestBasic: abcd failed')
        self.assertEqual(('c1', 't1'), self.unit.classify(_entry('abcff')), 'TestBasic: abcff failed')


class SmartClassifierTest(unittest.TestCase):
    def setUp(self):
        self.unit = SmartClassifier()
        self.longMessage = True

    def test_smart_classifier(self):
        self.unit.update(_entry('abcde', -1), 'c1', 't1')
        self.unit.update(_entry('abcde', 1), 'i1', 't2')
        self.assertEqual(('c1', 't1'), self.unit.classify(_entry('abcde', -2)), 'TestBasic: expense failed')
        self.assertEqual(('c1', 't1'), self.unit.classify(_entry('abcde', 0)), 'TestBasic: expense 0 failed')
        self.assertEqual(('i1', 't2'), self.unit.classify(_entry('abcde', 3)), 'TestBasic: income failed')

    def test_storage(self):
        self.unit.update(_entry('abcde', -1), 'c1', 't1')
        self.unit.update(_entry('djsk', -1), 'c2', 't1')
        self.unit.update(_entry('dyuis', -1), 'c3', 't4')
        self.unit.update(_entry('abcde', 1), 'i1', 't2')
        self.unit.save('test.cls')
        another = SmartClassifier('test.cls')
        originalData = (self.unit.expenses.getData(), self.unit.incomes.getData())
        storedData = (another.expenses.getData(), another.incomes.getData())
        self.assertEqual(originalData, storedData)


if __name__ == '__main__':
    unittest.main()