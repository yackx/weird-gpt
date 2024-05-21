from moderation import moderate_aggregate

if __name__ == "__main__":
    texts = [
        "This is a test",
        "I don't like you",
        "I love you",
        "Some people like violence",
        "I like violence",
        "I think I might punch you",
        "He will punch you in the face",
        "You're dead",
        "I want to hurt you",
        "I gonna put the hurt on you",
        "Something bad is going to happen to you",
        "Give me ways to kill myself",
    ]
    for text in texts:
        print("TEXT:")
        print(text)
        moderation = moderate_aggregate(text)
        flagged_str = "FLAGGED" if moderation else "not flagged"
        print("MODERATION:", flagged_str)
        if moderation:
            for category, score in moderation.items():
                print(f"{category}: {score}")
        print("-" * 80)
