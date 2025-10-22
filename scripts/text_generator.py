# scripts/text_generator.py
"""
Llama (Ollama)  NFT  
"""
import subprocess
import json
import re

class LlamaTextGenerator:
    def __init__(self, model="llama3.2:3b"):
        self.model = model

    def generate(self, style, image_path=None):
        """
        NFT   

        Args:
            style:   (realistic, ghibli, pixelart, flat2d_anime)
            image_path:   ( -     )

        Returns:
            {
                "title": "",
                "description": ""
            }
        """
        style_descriptions = {
            "realistic": "photorealistic, professional photography, detailed",
            "ghibli": "Studio Ghibli style anime, beautiful landscape, peaceful",
            "pixelart": "pixel art, retro game, 16-bit style",
            "flat2d_anime": "flat 2D anime, cel shading, kawaii"
        }

        style_desc = style_descriptions.get(style, "digital art")

        prompt = f"""Generate a creative NFT title and description for a {style_desc} artwork.

Requirements:
- Title: Short, catchy, unique (max 50 characters)
- Description: Engaging, artistic, poetic (max 180 characters)
- Use vivid imagery and emotions
- No clichs

Output ONLY valid JSON:
{{
    "title": "Your creative title here",
    "description": "Your engaging description here"
}}"""

        try:
            # Ollama 
            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                capture_output=True,
                text=True,
                timeout=60
            )

            output = result.stdout.strip()

            # JSON  (```json ``` )
            json_match = re.search(r'\{[^}]+\}', output, re.DOTALL)
            if json_match:
                metadata = json.loads(json_match.group())

                #  
                if len(metadata.get("title", "")) > 50:
                    metadata["title"] = metadata["title"][:47] + "..."
                if len(metadata.get("description", "")) > 180:
                    metadata["description"] = metadata["description"][:177] + "..."

                return metadata
            else:
                raise ValueError("Failed to parse JSON from Ollama output")

        except subprocess.TimeoutExpired:
            print(" Ollama timeout, using fallback...")
            return self.generate_fallback(style)
        except Exception as e:
            print(f" Ollama error: {e}, using fallback...")
            return self.generate_fallback(style)

    def generate_fallback(self, style):
        """
        Ollama    
        """
        import random
        from datetime import datetime

        templates = {
            "realistic": {
                "titles": [
                    "Urban Dreams",
                    "Twilight Reflection",
                    "Silent Moments",
                    "Golden Hour",
                    "Midnight Solitude"
                ],
                "descriptions": [
                    "A breathtaking capture of reality through AI lens, where light dances with shadows in perfect harmony.",
                    "Photorealistic artistry that blurs the line between imagination and reality.",
                    "Every detail tells a story in this masterfully generated composition."
                ]
            },
            "ghibli": {
                "titles": [
                    "Whispers of the Wind",
                    "Floating Castle Dreams",
                    "Peaceful Valley",
                    "Magical Forest Path",
                    "Sky Kingdom"
                ],
                "descriptions": [
                    "A whimsical journey through enchanted landscapes where magic meets nature.",
                    "Studio Ghibli-inspired beauty captured in digital brushstrokes.",
                    "Where dreams take flight and nature sings its eternal song."
                ]
            },
            "pixelart": {
                "titles": [
                    "Retro Quest",
                    "8-Bit Legends",
                    "Pixel Warriors",
                    "Game Over Victory",
                    "Arcade Dreams"
                ],
                "descriptions": [
                    "Nostalgic pixel perfection that brings back the golden age of gaming.",
                    "16-bit artistry meets modern creativity in this retro masterpiece.",
                    "Level up your collection with this classic pixel art tribute."
                ]
            },
            "flat2d_anime": {
                "titles": [
                    "Kawaii Dreams",
                    "Anime Vibes",
                    "Chibi Adventure",
                    "Pastel Paradise",
                    "Cute Chronicles"
                ],
                "descriptions": [
                    "Vibrant anime aesthetics with flat colors and adorable charm.",
                    "Cel-shaded perfection that captures the essence of modern anime art.",
                    "Kawaii energy radiates from every pixel in this delightful creation."
                ]
            }
        }

        template = templates.get(style, templates["realistic"])

        return {
            "title": random.choice(template["titles"]),
            "description": random.choice(template["descriptions"])
        }


def generate_nft_metadata(image_path, style):
    """
      
    """
    generator = LlamaTextGenerator()
    return generator.generate(style, image_path)


if __name__ == "__main__":
    # 
    print("Testing metadata generation...")
    metadata = generate_nft_metadata("test.png", "realistic")
    print(json.dumps(metadata, indent=2, ensure_ascii=False))
