import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO #used for in-memory binary data
# in this project we will be storing the images and displaying

class DataAnalyser:
    # @staticmethod - a decorator used to define a static method within class.
    # static method - belongs to the class (not instance of the class) - no self, or cls
    # @staticmethod - used to define a function - which is standalone and will not be dependent on the class, well structured format for class
    @staticmethod
    def clean(df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean Raw Data
        """
        for column in df.columns:
            if pd.api.types.is_string_dtype(df[column]):
                df[column] = df[column].fillna("Unknown").str.strip().str.lower()
            else:
                df[column] = df[column].fillna(df[column].median())
        return df
    @staticmethod
    def analyze(df: pd.DataFrame) -> dict:
        """
        Generate Insights
        """
        stats = {
            "Summary": df.describe().to_dict(),
            "Correlations": df.select_dtypes(include = "number").corr().to_dict()
        }

        plt.figure(figsize = (10, 6))
        sns.heatmap(df.corr(), annot = True, cmap = "coolwarm")
        buf = BytesIO()
        plt.savefig(buf, format = "png")
        plt.close()

        return {
            # stats takes all the key value pairs from the dictionary defined and unpacks them into the new dictionary being created
            # ** is used to avoid repetitions, while each time copying the same keys from stats - works like dynamic merging
            **stats,
            "correlation_plot": base64.b64encode(buf.getvalue().decode("utf-8"))
        }