import re

with open('twitter_thread.md', 'r') as f:
    content = f.read()

# Split by tweet headers
tweets = re.split(r'## Tweet \d+/10', content)[1:]

for i, tweet in enumerate(tweets, 1):
    # Remove image attachments and clean up
    lines = tweet.strip().split('\n')
    tweet_text = []
    for line in lines:
        if not line.startswith('[Attach:'):
            tweet_text.append(line)
    
    # Join and count characters
    full_text = '\n'.join(tweet_text).strip()
    char_count = len(full_text)
    
    print(f"Tweet {i}/10: {char_count} characters")
    if char_count > 280:
        print(f"  ⚠️  OVER LIMIT by {char_count - 280} characters")
    else:
        print(f"  ✓ Under limit ({280 - char_count} characters remaining)")
    print()