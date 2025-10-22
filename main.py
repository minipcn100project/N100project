# main.py
"""
N100 NFT   
"""
import schedule
import time
import random
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

#  
from scripts.image_generator import generate_image
from scripts.text_generator import generate_nft_metadata
from scripts.solana_minter import mint_nft
from scripts.twitter_bot import TwitterNFTBot
from scripts.landing_page_generator import LandingPageGenerator
from scripts.git_sync import sync_to_github
from scripts.web_automation import post_to_twitter_web

#   
load_dotenv()

# 
use_web_automation = os.getenv("USE_WEB_AUTOMATION", "false").lower() == "true"
twitter_bot = TwitterNFTBot() if not use_web_automation else None
page_gen = LandingPageGenerator()

# NFT  ( )
counter_file = Path("output/nft_counter.txt")
if counter_file.exists():
    with open(counter_file, 'r') as f:
        nft_index = int(f.read().strip())
else:
    nft_index = 0


def save_counter():
    """NFT  """
    with open(counter_file, 'w') as f:
        f.write(str(nft_index))


def automated_workflow():
    """
       
    """
    global nft_index
    nft_index += 1

    print(f"\n{'='*70}")
    print(f"Starting NFT #{nft_index} generation")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")

    try:
        # 1.   
        styles = ["realistic", "ghibli", "pixelart", "flat2d_anime"]
        style = random.choice(styles)
        print(f"Selected style: {style}")

        # 2. ComfyUI  
        print("\n[1/6] Generating image with ComfyUI...")
        image_path = generate_image(style, index=nft_index)
        print(f"[OK] Image saved: {image_path}")

        # 3. Llama / 
        print("\n[2/6] Generating metadata with Llama...")
        metadata = generate_nft_metadata(image_path, style)
        print(f"[OK] Title: {metadata['title']}")
        print(f"[OK] Description: {metadata['description'][:60]}...")

        # 4. NFT   (Lazy Minting)
        print("\n[3/6] Preparing NFT metadata...")
        mint_result = mint_nft(
            image_path,
            metadata["title"],
            metadata["description"],
            nft_index
        )
        print(f"[OK] Metadata ready")

        # 5.  
        print("\n[4/6] Generating landing page...")
        nft_data = {
            "index": nft_index,
            "title": metadata["title"],
            "description": metadata["description"],
            "mint_url": mint_result["mint_url"],
            "price": float(os.getenv("NFT_PRICE_SOL", "0.5")),
            "style": style,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        landing_url = page_gen.generate_nft_page(nft_data)
        print(f"[OK] Landing page: {landing_url}")

        # 6.  
        print("\n[5/6] Posting to Twitter...")
        nft_data_for_twitter = nft_data.copy()
        nft_data_for_twitter["mint_url"] = landing_url  #   

        # Twitter API  Web Automation 
        if use_web_automation:
            print("Using Web Automation (Playwright)")
            #   
            tweet_text = f"""{nft_data['title']} #{nft_data['index']:03d}

{nft_data['description'][:120]}

{landing_url}
{nft_data['price']} SOL
Lazy Mint

#NFT #SolanaNFT #AIArt #N100"""

            tweet_result = post_to_twitter_web(tweet_text, image_path)
        else:
            print("Using Twitter API")
            tweet_result = twitter_bot.post_nft(image_path, nft_data_for_twitter)

        if tweet_result["success"]:
            print(f"[OK] Tweet posted: {tweet_result.get('tweet_url', 'Success')}")
        else:
            print(f"[WARN] Twitter posting failed: {tweet_result['error']}")

        # 7. GitHub 
        print("\n[6/6] Syncing to GitHub...")
        sync_to_github({
            "index": nft_index,
            "title": metadata["title"],
            "description": metadata["description"],
            "image_path": image_path,
            "mint_url": mint_result["mint_url"],
            "landing_url": landing_url,
            "tweet_url": tweet_result.get("tweet_url", ""),
            "style": style
        })
        print("[OK] Synced to GitHub")

        #  
        save_counter()

        print(f"\n{'='*70}")
        print(f"NFT #{nft_index} workflow completed successfully!")
        print(f"Total time: {(datetime.now() - start_time).seconds} seconds")
        print(f"{'='*70}\n")

    except Exception as e:
        print(f"\n{'='*70}")
        print(f"[ERROR] Workflow failed: {str(e)}")
        print(f"{'='*70}\n")

        #   
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        with open(log_dir / "errors.log", "a", encoding='utf-8') as f:
            f.write(f"{datetime.now()}: NFT #{nft_index} - {str(e)}\n")

        #    
        nft_index -= 1
        save_counter()


def post_weekly_stats():
    """
       ( )
    """
    try:
        total_generated = nft_index
        twitter_bot.post_collection_update(
            total_minted=0,  #    Candy Machine 
            total_available=total_generated
        )
        print("[OK] Posted weekly statistics to Twitter")
    except Exception as e:
        print(f"[WARN] Failed to post stats: {e}")


if __name__ == "__main__":
    import sys

    #   
    test_mode = "--test" in sys.argv

    if test_mode:
        #  :  1 
        print("=" * 60)
        print("")
        print("      N100 NFT Automation - TEST MODE")
        print("")
        print("=" * 60 + "\n")

        start_time = datetime.now()
        automated_workflow()

        print("\nTest completed!")
        sys.exit(0)

    #  : 
    interval_hours = int(os.getenv("MINT_INTERVAL_HOURS", "1"))
    schedule.every(interval_hours).hours.do(automated_workflow)

    #   (   8)
    # schedule.every().sunday.at("20:00").do(post_weekly_stats)

    twitter_mode = "Web Automation (Playwright)" if use_web_automation else "Twitter API"

    print("=" * 60)
    print("")
    print("      N100 NFT Automation Bot Started!")
    print("")
    print(f"  Schedule: Every {interval_hours} hour(s)")
    print("  Blockchain: Solana (Lazy Minting)")
    print(f"  Twitter: {twitter_mode}")
    print("  GitHub: Auto-Sync Enabled")
    print("  Styles: Realistic, Ghibli, Pixel Art, Anime")
    print("")
    print("  Powered by: Intel N100 Mini PC (CPU Only)")
    print("")
    print("=" * 60 + "\n")

    print(f"Current NFT count: {nft_index}")
    print(f"Next run scheduled in {interval_hours} hour(s)\n")

    #    ()
    user_input = input("Run immediately? (y/n): ").lower()
    if user_input == 'y':
        start_time = datetime.now()
        automated_workflow()

    #  
    print("\nWaiting for scheduled tasks...\n")
    while True:
        schedule.run_pending()
        time.sleep(60)  # 1 
