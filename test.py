import unittest
import pandas as pd

class unittest_class(unittest.TestCase):
    def setUp(self):
        self.files = ["JAPAN_USGS_cleaned.csv",
            "JAPAN_GEOFON_cleaned.csv",
            "JAPAN_DATASET_cleaned.csv",
            "JAPAN_EMSC_cleaned.csv"]

    def test_emptyfile(self):  # Checking that the file is not empty.
        for file in self.files:
            df = pd.read_csv(file)
            self.assertFalse(df.empty)

    def test_col(self):  # Checking that these columns exist in the file.
        columns_ = ["time", "latitude", "longitude", "mag", "region", "depth", "tokyo_distance", "place"]
        for file in self.files:
            df = pd.read_csv(file)
            for col in columns_:
                self.assertIn(col, df.columns)

    def test_num(self):  # Checking that the values in these columns are numeric.
        num_columns = ["latitude", "longitude", "depth", "mag", "tokyo_distance"]
        for file in self.files:
            df = pd.read_csv(file)
            for col in num_columns:
                first_value = df[col].iloc[0]
                self.assertTrue(isinstance(first_value, (int, float)))
                self.assertTrue((df[col] >= 0).all())

    def test_chvalue(self):  # Checking that there are no NaN values
        ch_columns = ["time", "latitude", "longitude", "depth", "mag", "tokyo_distance", "region", "place"]
        for file in self.files:
            df = pd.read_csv(file)
            for col in ch_columns:
                for value in df[col]:
                    self.assertIsNotNone(value)

    def test_magstats(self):  # Checking the mean and standard deviation.
        for file in self.files:
            df = pd.read_csv(file)
            mean_mag = df["mag"].mean()
            std_mag = df["mag"].std()
            self.assertTrue(1 <= mean_mag <= 10)
            self.assertTrue(std_mag < 3)

if __name__ == "__main__":
    unittest.main()