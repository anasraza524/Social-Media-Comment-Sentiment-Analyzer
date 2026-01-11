import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import os
import sys

# Increase recursion depth for massive datasets (Step 5 & 11)
sys.setrecursionlimit(2000)

# --- Step 10: Object-Oriented Programming ---
class BaseAnalyzer:
    """Base class for Sentiment Analysis (Step 10: OOP)"""
    def __init__(self, name):
        self.name = name

    def display_welcome(self):
        print(f"--- Welcome to {self.name} ---")

class SentimentAnalyzer(BaseAnalyzer):
    """Main analyzer class using Inheritance (Step 10: OOP)"""
    
    def __init__(self):
        super().__init__("Social Media Sentiment Analyzer")
        # --- Step 3: Data Structures (Dictionary with Intensity Weights) ---
        # Positive values (1-4), Negative values (-1 to -4)
        self.sentiment_weights = {
            # Positive
            'love': 3, 'great': 2, 'amazing': 3, 'happy': 2, 'fantastic': 3, 
            'excellent': 3, 'best': 4, 'clean': 1, 'fast': 1, 'perfectly': 2, 
            'quickly': 1, 'helpful': 2, 'recommend': 2, 'brilliant': 3, 'lit': 2,
            'fire': 2, 'awesome': 3, 'good': 1, 'nice': 1, 'love it': 4,
            
            # Negative
            'worst': -4, 'crash': -3, 'hate': -3, 'confusing': -2, 'annoying': -2, 
            'bugs': -2, 'slow': -1, 'poor': -2, 'refund': -3, 'bad': -2, 
            'terrible': -3, 'lagging': -2, 'broken': -3, 'ugly': -2, 'fail': -3,
            'useless': -3, 'disappointed': -2, 'frustrating': -2, 'trash': -3,
            
            # Neutral markers
            'okay': 0, 'average': 0, 'neutral': 0, 'opinion': 0, 'balanced': 0
        }
        self.negation_words = {'not', 'never', 'no', 'hardly', 'barely', 'dont', 'doesnt'}
        self.results = []

    # --- Step 6: String Handling & Regular Expressions ---
    def clean_text(self, text):
        """Cleans comment text using Regex (Step 6)"""
        if not isinstance(text, str):
            return ""
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Keep alphanumeric characters and some punctuation for better context if needed, 
        # but for simple keyword extraction, spaces-only is usually safer.
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return text.strip().lower()

    def validate_user_id(self, user_id):
        """Validates User ID using Regex and String Slicing (Step 6)"""
        pattern = r'^user_\d+$'
        if bool(re.match(pattern, user_id)):
            # Step 6: String Slicing (extract numeric part)
            numeric_part = user_id[5:]
            # Step 6: Formatting
            # print(f"Processing student record ID: {numeric_part:04}")
            return True
        return False

    # --- Step 5: Functions & Recursion ---
    def calculate_score(self, text):
        """Calculates weighted sentiment score with basic negation handling (Step 4 & 5)"""
        words = text.split()
        score = 0
        negate = False
        
        for word in words:
            # Check for negation
            if word in self.negation_words:
                negate = True
                continue
            
            # Apply weights
            if word in self.sentiment_weights:
                word_score = self.sentiment_weights[word]
                
                # If negated, flip the score (simplification)
                if negate:
                    score -= (word_score * 1.5) # Negation often adds more intensity to the flip
                    negate = False 
                else:
                    score += word_score
            elif negate:
                negate = False

        return score

    def process_records_recursive(self, records, index=0):
        """Processes comments using Recursion (Step 5)"""
        if index >= len(records):
            return []
        
        row = records.iloc[index]
        user_id = row['user_id']
        raw_text = row['comment_text']
        
        try:
            if not self.validate_user_id(user_id):
                # Skipping logic (Step 4)
                return self.process_records_recursive(records, index + 1)
            
            clean_text = self.clean_text(raw_text)
            score = self.calculate_score(clean_text)
            
            # Step 4: Control Flow
            if score > 0:
                sentiment = "Positive"
            elif score < 0:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"
                
            record = (user_id, sentiment, score) # Step 3: Tuple
            return [record] + self.process_records_recursive(records, index + 1)
            
        except Exception as e:
            return self.process_records_recursive(records, index + 1)

    # --- Step 7 & 8: File Handling, NumPy & Pandas ---
    def analyze(self, file_path):
        """Main analysis pipeline (Step 7 & 8)"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file {file_path} not found.")

        df = pd.read_csv(file_path)
        print(f"Loaded {len(df)} records from {file_path}")

        # --- Step 3: Sets (Remove duplicate IDs before processing) ---
        original_ids = list(df['user_id'])
        unique_ids = set(original_ids)
        if len(original_ids) != len(unique_ids):
            print(f"Removed {len(original_ids) - len(unique_ids)} duplicate User IDs using Sets.")
            df = df.drop_duplicates(subset='user_id')

        # Process via Recursion
        self.results = self.process_records_recursive(df)
        
        results_df = pd.DataFrame(self.results, columns=['user_id', 'sentiment', 'score'])
        
        # --- Step 8: NumPy Integration ---
        scores_array = np.array(results_df['score'])
        mean_score = np.mean(scores_array)
        std_score = np.std(scores_array)
        
        print(f"\nAnalysis Summary:")
        print(f"Total Processed: {len(results_df)}")
        print(f"Mean Sentiment Score: {mean_score:.2f}")
        print(f"Sentiment Standard Deviation: {std_score:.2f}")

        # --- Step 7: Store Output to File ---
        output_file = "sentiment_report.csv"
        results_df.to_csv(output_file, index=False)
        print(f"\nReport saved to: {output_file}")
        
        return results_df

    # --- Step 9: Data Visualization ---
    def visualize(self, results_df):
        """Generates visualizations (Step 9)"""
        sentiment_counts = results_df['sentiment'].value_counts()
        
        plt.figure(figsize=(12, 5))
        
        # Color palette
        colors = ['#4CAF50', '#F44336', '#2196F3']
        
        # Plot 1: Pie Chart (Distribution)
        plt.subplot(1, 2, 1)
        plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', colors=colors, startangle=140)
        plt.title('Sentiment Distribution')
        
        # Plot 2: Bar Chart (Score Frequency)
        plt.subplot(1, 2, 2)
        results_df['score'].value_counts().sort_index().plot(kind='bar', color='skyblue')
        plt.title('Score Frequency')
        plt.xlabel('Sentiment Score')
        plt.ylabel('Count')
        
        plt.tight_layout()
        plt.savefig('sentiment_visualization.png')
        print("Visualization saved as 'sentiment_visualization.png'")

# --- Main Interaction Logic (Step 4 & 11) ---
def main():
    analyzer = SentimentAnalyzer()
    analyzer.display_welcome()
    
    input_file = "comments.csv"
    
    try:
        results = analyzer.analyze(input_file)
        analyzer.visualize(results)
        
        # --- Step 3: Sets (Remove duplicates if any - though here used contextually) ---
        sentiments_found = set(results['sentiment'])
        print(f"Unique sentiments detected: {sentiments_found}")
        
    except Exception as e:
        print(f"A fatal error occurred: {e}")

if __name__ == "__main__":
    main()
