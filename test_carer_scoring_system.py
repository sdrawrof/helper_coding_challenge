# Testing class for carer_scoring_system.py
import unittest
from carer_scoring_system import CarerScorer
import numpy as np

class TestCarerScorer(unittest.TestCase):
    testObj = CarerScorer("data.csv")

    def test_input_string(self):
        # Test whether the given string is a csv file or not
        file_types = ["data.pdf", "data.xml", "data.docx"]
        for f in file_types:
            self.assertRaises(IOError, CarerScorer, f)

    def test_calc_years_experience(self):
        # Test whether a 2d array is returned
        self.assertIs(type(self.testObj.calc_years_experience()), np.ndarray)
        self.assertEqual(np.ndim(self.testObj.calc_years_experience()), 2)

    def test_calc_average_review(self):
        # Test whether a 2d array is returned
        self.assertIs(type(self.testObj.calc_average_review()), np.ndarray)
        self.assertEqual(np.ndim(self.testObj.calc_years_experience()), 2)

    def test_calc_num_prev_clients(self):
        # Test whether a 2d array is returned
        self.assertIs(type(self.testObj.calc_num_prev_clients()), np.ndarray)
        self.assertEqual(np.ndim(self.testObj.calc_num_prev_clients()), 2)

    def test_calc_days_since_logon(self):
        # Test whether a 2d array is returned
        self.assertIs(type(self.testObj.calc_days_since_logon()), np.ndarray)
        self.assertEqual(np.ndim(self.testObj.calc_days_since_logon()), 2)

    def test_calc_image_problems(self):
        # Test whether a 2d array is returned
        self.assertIs(type(self.testObj.calc_image_problems()), np.ndarray)
        self.assertEqual(np.ndim(self.testObj.calc_image_problems()), 2)

    def test_calc_final_score(self):
        # Test whether the inputs are all correct arrays and have not been modified incorrectly in their functions
        self.assertRaises(TypeError,
                          self.testObj.calc_final_score(self.testObj.calc_years_experience(),
                                                        self.testObj.calc_average_review(),
                                                        self.testObj.calc_num_prev_clients(),
                                                        self.testObj.calc_days_since_logon(),
                                                        self.testObj.calc_image_problems()), np.ndarray)
        self.assertEqual(np.ndim(self.testObj.calc_final_score(self.testObj.calc_years_experience(),
                                                        self.testObj.calc_average_review(),
                                                        self.testObj.calc_num_prev_clients(),
                                                        self.testObj.calc_days_since_logon(),
                                                        self.testObj.calc_image_problems())), 2)


if __name__ == '__main__':
    unittest.main()
