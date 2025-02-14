# Mercari Price Suggestion Challenge

This project is a solution for the Mercari Price Suggestion Challenge, which involves predicting product prices based on various textual and categorical features. The script processes the dataset, performs feature engineering, trains a Ridge regression model, and generates price predictions.

## Project Structure
```
.
├── mercari_price_suggest.py  # Main script for data processing and model training
├── README.md                 # Documentation
├── submission.csv            # Final output file with predicted prices
├── kaggle.json               # Kaggle API credentials (not included, must be provided by the user)
└── mercari_data/             # Folder containing dataset files
```

## Prerequisites
Ensure you have the following dependencies installed:
- Python 3.x
- Kaggle API (`pip install kaggle`)
- Required Python libraries:
  ```sh
  pip install numpy pandas seaborn matplotlib scikit-learn scipy lightgbm
  ```
- `kaggle.json` file (API credentials) must be placed in the working directory.
- Unix utilities such as `unzip` and `7z` installed.

## Dataset
The dataset is sourced from the [Mercari Price Suggestion Challenge](https://www.kaggle.com/c/mercari-price-suggestion-challenge). It includes product listings with various attributes such as name, category, brand, item condition, and description.

## How to Run
1. Place `kaggle.json` in the working directory.
2. Run the script:
   ```sh
   python mercari_price_suggest.py
   ```
3. The script will:
   - Download and extract the dataset.
   - Perform exploratory data analysis (EDA).
   - Process and clean the dataset.
   - Encode categorical features and vectorize textual features.
   - Train a Ridge regression model and make predictions.
   - Save the final predictions to `submission.csv`.

## Output
The script generates a `submission.csv` file containing the predicted prices for test data:
```
test_id,price
0,10.45
1,20.32
2,5.99
...
```

## Notes
- This script was initially developed as a Jupyter notebook and converted into a standalone Python script.
- Ensure that all required dependencies are installed before running the script.
- The Ridge regression model is used due to the presence of multicollinearity in the dataset.

## License
This project is for educational purposes. Use it at your own discretion.

