import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO #used for in-memory binary data
# in this project we will be storing the images and displaying

class DataCleaner:
    # @staticmethod - a decorator used to define a static method within class.
    # static method - belongs to the class (not instance of the class) - no self, or cls
    # @staticmethod - used to define a function - which is standalone and will not be dependent on the class, well structured format for class
    @staticmethod
    def clean(df: pd.DataFrame, outlier_threshold: float = 3.0) -> pd.DataFrame:
        """
        Intelligently Clean DataFrame by:
        1. Auto-Detecting columns types
        2. Handling missing values
        3. Treating outliers
        4. Standardizing data types
        5. Converting to proper dtypes
        6. Removing duplicates

        Paramters:
        df (pd.DataFrame): The input dataframe to be cleaned.
        outlier_threshold (float): Z-score The threshold for identifying outliers. Default is 3.0.

        Returns:
        pd.DataFrame: The cleaned dataframe.
        """
        df = df.copy() # create a copy of the dataframe to avoid modifying the original data

        # 1. Auto-Detecting columns types and converting to proper dtypes
        for column in df.columns:
            # skip if all null values:
            if df[column].isna().all():
                continue
            columns_type = DataCleaner.__detect_column_tuype(df[column])
            df[column] = DataCleaner.__convert_type(df[column], columns_type)

        # 2. Missing Values
        df = DataCleaner.__handle_missing_values(df)

        # 3. Outliers (for numeric columns only)
        df = DataCleaner.__handle_outliers(df, threshold = outlier_threshold)

        # Final Standardiztion
        df = DataCleaner.__standardize_data_types(df)

        return df
    
    @staticmethod
    def __detect_column_tuype(series: pd.Series) -> str:
        """
        Detect the most likely data type of a column
        """
        # count the non-null values
        non_null = series.dropna()
        if len(non_null) == 0:
            return "string" # default if all null
        
        # test for datatime
        try:
            pd.to_datatime(non_null, errors = "raise")
            return "datetime"
        except:
            pass

        # test for numeric
        try:
            pd.to_numeric(non_null, errors = "raise")
            return "numeric"
        except:
            pass

        # Check for boolean
        unique_values = non_null.astype(str).str.lower().unique()
        if set(unique_values) <= {"true", "false", "0", "1", "yes", "no"}:
            return "boolean"


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