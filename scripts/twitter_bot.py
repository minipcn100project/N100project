# scripts/twitter_bot.py
"""
Twitter  
"""
import tweepy
import os
from dotenv import load_dotenv
from PIL import Image
import io

load_dotenv()

class TwitterNFTBot:
    def __init__(self):
        # Twitter API v2 
        self.client = tweepy.Client(
            bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
        )

        # API v1.1 ( )
        auth = tweepy.OAuth1UserHandler(
            os.getenv("TWITTER_API_KEY"),
            os.getenv("TWITTER_API_SECRET"),
            os.getenv("TWITTER_ACCESS_TOKEN"),
            os.getenv("TWITTER_ACCESS_SECRET")
        )
        self.api = tweepy.API(auth)

    def optimize_image(self, image_path, max_size_mb=5):
        """
            
        """
        img = Image.open(image_path)

        if img.size[0] > 1200 or img.size[1] > 1200:
            img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)

        output = io.BytesIO()
        img.save(output, format='PNG', optimize=True)
        output.seek(0)

        size_mb = len(output.getvalue()) / (1024 * 1024)

        if size_mb > 5:
            output = io.BytesIO()
            img.convert('RGB').save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)

        return output

    def post_nft(self, image_path, nft_data):
        """
        NFT   

        Args:
            image_path:   
            nft_data: {
                "index": 1,
                "title": "",
                "description": "",
                "mint_url": " ",
                "price": 0.5,
                "style": "realistic"
            }
        """
        try:
            #  
            print(" Uploading image to Twitter...")
            optimized_img = self.optimize_image(image_path)
            media = self.api.media_upload(filename="nft.png", file=optimized_img)

            #   
            tweet_text = self.create_tweet_text(nft_data)

            #  
            print(" Posting to Twitter...")
            tweet = self.client.create_tweet(
                text=tweet_text,
                media_ids=[media.media_id]
            )

            tweet_url = f"https://twitter.com/user/status/{tweet.data['id']}"
            print(f" Tweet posted: {tweet_url}")

            return {
                "success": True,
                "tweet_id": tweet.data['id'],
                "tweet_url": tweet_url
            }

        except Exception as e:
            print(f" Twitter posting failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def create_tweet_text(self, nft_data):
        """
           (280 )
        """
        title = nft_data.get("title", "Untitled")
        index = nft_data.get("index", 0)
        description = nft_data.get("description", "")
        mint_url = nft_data.get("mint_url", "")
        price = nft_data.get("price", 0.5)
        style = nft_data.get("style", "AI Art")

        #   
        max_desc_length = 120
        if len(description) > max_desc_length:
            description = description[:max_desc_length-3] + "..."

        #  
        tweet = f""" {title} #{index:03d}

{description}

 Mint: {mint_url}
 {price} SOL
 Lazy Mint (  )

#{self.get_style_hashtag(style)} #NFT #SolanaNFT #AIArt #N100"""

        # 280   
        if len(tweet) > 280:
            excess = len(tweet) - 280
            description = description[:-(excess + 3)] + "..."
            tweet = f""" {title} #{index:03d}

{description}

 {mint_url}
 {price} SOL

#{self.get_style_hashtag(style)} #NFT #SolanaNFT"""

        return tweet

    def get_style_hashtag(self, style):
        """
         
        """
        hashtags = {
            "realistic": "Photorealistic",
            "ghibli": "StudioGhibli",
            "pixelart": "PixelArt",
            "flat2d_anime": "AnimeArt"
        }
        return hashtags.get(style.lower(), "DigitalArt")

    def post_collection_update(self, total_minted, total_available):
        """
          
        """
        tweet = f""" N100 NFT Collection Update

 Total Generated: {total_available}
 Total Minted: {total_minted}
 Available: {total_available - total_minted}

 Powered by Intel N100 Mini PC
 No GPU, Pure CPU Magic

#NFT #SolanaNFT #N100Project"""

        self.client.create_tweet(text=tweet)


if __name__ == "__main__":
    # 
    bot = TwitterNFTBot()
    test_data = {
        "index": 999,
        "title": "Test NFT",
        "description": "This is a test description for the NFT.",
        "mint_url": "https://example.com/mint/999",
        "price": 0.5,
        "style": "realistic"
    }
    # result = bot.post_nft("test_image.png", test_data)
    print("Twitter bot ready!")
