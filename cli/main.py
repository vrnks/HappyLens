import pandas as pd

def load_and_prepare_data(filepath: str) -> pd.DataFrame:
    """
    Load happiness data from a CSV file, filter for the year 2024,
    and drop unnecessary columns.
    
    Args:
        filepath (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: Cleaned dataset for the year 2024.
    """
    df = pd.read_csv(filepath)
    df = df[df["Year"] == 2024]
    df = df.drop(columns=['Year', 'Rank', 'upperwhisker', 'lowerwhisker'])
    return df


# List of factors considered in the happiness score
factors = ['GDP', 'SocialSupport', 'LifeExpectancy', 'Freedom', 'Generosity', 'Corruption']

def get_user_weights() -> dict:
    """
    Prompt the user to input custom weights for each factor.
    
    Returns:
        dict: Dictionary of user-defined weights for each factor.
    """
    print("Please enter weights for each factor (between 0 and 1).")
    weights = {}
    for factor in factors:
        while True:
            try:
                w = float(input(f"{factor}: "))
                if 0 <= w <= 1:
                    weights[factor] = w
                    break
                else:
                    print("Please enter a value between 0 and 1.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    return weights

def compute_scores(df: pd.DataFrame, weights: dict) -> pd.DataFrame:
    """
    Compute a personalized score for each country based on user-defined weights.
    
    Args:
        df (pd.DataFrame): DataFrame containing happiness data.
        weights (dict): Weights assigned by the user for each factor.
        
    Returns:
        pd.DataFrame: Top 10 countries ranked by the personalized score.
    """
    df = df.copy()
    for factor in factors:
        df[factor] = pd.to_numeric(df[factor], errors='coerce')
    
    df['Score'] = sum(df[factor] * weights[factor] for factor in factors)
    return df[['Country', 'HappinessScore', 'Score']].sort_values(by='Score', ascending=False).head(10)

def main():
    """
    Main function to execute the CLI for recommending countries based on user preferences.
    """
    filepath = "/HappyLens/data/happiness_data.csv"
    df = load_and_prepare_data(filepath)
    weights = get_user_weights()
    result = compute_scores(df, weights)
    
    print("\nYour personalized Top-10 countries based on your weights:")
    print(result.to_string(index=False))

if __name__ == "__main__":
    main()