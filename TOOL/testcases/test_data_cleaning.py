import pandas as pd
import numpy as np
from mod_datacleaning import data_cleaning
import unittest

class TestDataCleaning(unittest.TestCase):
    data = pd.read_csv("iris.csv")
    test_data = data
    test_data.loc[0,'a']=''
    
    def test_fix_missing(self):
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()                                                                                                                                                                                                                                                                                                                                                                                                                                                         