from dotenv import load_dotenv
import tweepy
import os 
import logging

logging.basicConfig(level=logging.DEBUG)

def main():
    client = tweepy.Client(
        bearer_token=os.getenv("BEARER_TOKEN"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
        consumer_key=os.getenv("API_KEY"),
        consumer_secret=os.getenv("API_KEY_SECRET")
    )
    client.create_tweet(text="Hola desde Python :)")
 
if __name__ == "__main__":
    load_dotenv()
    main()