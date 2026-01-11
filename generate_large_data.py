import pandas as pd
import random
from datetime import datetime, timedelta

def generate_data(num_records=1000):
    positive_phrases = [
        "I love this product!", "Amazing experience today.", "Highly recommend this to everyone.",
        "The best service I've ever had.", "So happy with the results!", "Fantastic community and support.",
        "Great job on the new update.", "This is absolutely perfect.", "Excellent quality and design.",
        "not bad at all, actually good.", "never better, simply amazing.", "no crash so far, very stable."
    ]
    negative_phrases = [
        "I hate the new layout.", "This is the worst experience ever.", "It keeps crashing all the time.",
        "So confusing and hard to use.", "I want a refund immediately.", "Very slow performance on mobile.",
        "not great, very disappointing.", "never happy with their support.", "no good features found."
    ]
    neutral_phrases = [
        "The app is okay, I guess.", "Average performance, nothing special.", "It's a balanced update.",
        "Neutral opinion on the new feature.", "It does what it says it should do.", "Just another social media post.",
        "Checking in for the day.", "Interested to see what's next.", "Could be better, could be worse.",
        "Looking forward to more details.", "Wait and see approach.", "Standard functionality."
    ]
    
    data = []
    base_time = datetime(2025, 12, 15, 12, 0, 0)
    
    for i in range(1, num_records + 1):
        cat = random.choice(['pos', 'neg', 'neu'])
        if cat == 'pos':
            text = random.choice(positive_phrases)
        elif cat == 'neg':
            text = random.choice(negative_phrases)
        else:
            text = random.choice(neutral_phrases)
            
        user_id = f"user_{random.randint(100, 9999):04d}"
        timestamp = (base_time + timedelta(minutes=random.randint(1, 10000))).strftime("%Y-%m-%d %H:%M:%S")
        
        data.append([user_id, text, timestamp])
    
    df = pd.DataFrame(data, columns=['user_id', 'comment_text', 'timestamp'])
    df.to_csv('comments.csv', index=False)
    print(f"Generated {len(df)} records in comments.csv")

if __name__ == "__main__":
    generate_data(1000)
