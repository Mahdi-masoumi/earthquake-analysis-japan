import unittest
import pandas as pd

class TestEarthquakeData(unittest.TestCase):
    def setUp(self):
        self.df = pd.read_csv("earthquake_cleaned.csv")

    def test_emptyfile(self):
        self.assertFalse(self.df.empty)

    def test_col(self):
        columns_ = [
            "time", "latitude", "longitude", "depth", "mag",
            "region", "category"
        ]
        for col in columns_:
            self.assertIn(col, self.df.columns)

    def test_num(self):
        num_columns = ["latitude", "longitude", "depth", "mag"]
        for col in num_columns:
            self.assertTrue(pd.api.types.is_numeric_dtype(self.df[col]))
            self.assertTrue((self.df[col] >= 0).all())

    def test_chvalue(self):
        important_columns = ["time", "latitude", "longitude", "depth", "mag"]
        for col in important_columns:
            self.assertFalse(self.df[col].isnull().any())

    def test_magstats(self):
        mean_mag = self.df["mag"].mean()
        e_mag = self.df["mag"].std()
        self.assertTrue(1 <= mean_mag <= 10)
        self.assertTrue(e_mag < 3)
if __name__=="__main__":
        unittest.main()
