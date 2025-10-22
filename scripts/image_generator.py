# scripts/image_generator.py
"""
ComfyUI API   
"""
import json
import urllib.request
import urllib.parse
import websocket
import uuid
import os
from pathlib import Path

class ComfyUIImageGenerator:
    def __init__(self, server_address="127.0.0.1:8188"):
        self.server_address = server_address
        self.client_id = str(uuid.uuid4())

        #   
        self.workflow_dir = Path("config/workflows")
        self.output_dir = Path("output/images")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_workflow(self, style):
        """
        Load workflow file and convert to API format
        """
        # Use pixelart workflow for all styles as requested
        workflow_file = "sd15_pixelart_lcm_api.json"

        workflow_path = self.workflow_dir / workflow_file

        # If API version doesn't exist, convert it
        if not workflow_path.exists():
            ui_workflow_path = self.workflow_dir / "sd15_pixelart_lcm.json"
            if ui_workflow_path.exists():
                from scripts.workflow_converter import convert_ui_to_api
                with open(ui_workflow_path, 'r', encoding='utf-8') as f:
                    ui_workflow = json.load(f)
                api_workflow = convert_ui_to_api(ui_workflow)
                with open(workflow_path, 'w', encoding='utf-8') as f:
                    json.dump(api_workflow, f, indent=2)
            else:
                raise Exception(f"Workflow file not found: {ui_workflow_path}")

        with open(workflow_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def queue_prompt(self, prompt):
        """
        ComfyUI  
        """
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{self.server_address}/prompt", data=data)
        response = urllib.request.urlopen(req).read()
        return json.loads(response)

    def get_image(self, filename, subfolder, folder_type):
        """
          
        """
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)

        with urllib.request.urlopen(f"http://{self.server_address}/view?{url_values}") as response:
            return response.read()

    def get_history(self, prompt_id):
        """
          
        """
        with urllib.request.urlopen(f"http://{self.server_address}/history/{prompt_id}") as response:
            return json.loads(response.read())

    def track_progress(self, prompt_id):
        """
        WebSocket  
        """
        ws = websocket.WebSocket()
        ws.connect(f"ws://{self.server_address}/ws?clientId={self.client_id}")

        while True:
            out = ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'executing':
                    data = message['data']
                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        break  # 
                    else:
                        print(f" Executing node: {data['node']}")

        ws.close()

    def generate(self, style, custom_prompt=None, index=1):
        """
           

        Args:
            style: "realistic", "ghibli", "pixelart", "flat2d_anime"
            custom_prompt:    ()
            index: NFT 

        Returns:
               
        """
        print(f" Loading {style} workflow...")
        workflow = self.load_workflow(style)

        # Update prompt if provided
        if custom_prompt:
            # Find positive prompt node (usually node 6)
            for node_id, node_data in workflow.items():
                if node_data.get("class_type") == "CLIPTextEncode":
                    if "text" in node_data.get("inputs", {}):
                        # First CLIPTextEncode is positive prompt
                        node_data["inputs"]["text"] = f"pixel art, {custom_prompt}, 16-bit style, retro game, vibrant colors, sharp pixels"
                        break

        # Randomize seed for variety
        import random
        for node_id, node_data in workflow.items():
            if node_data.get("class_type") == "KSampler":
                if "seed" in node_data.get("inputs", {}):
                    node_data["inputs"]["seed"] = random.randint(1, 2**32 - 1)
                    print(f" Random seed: {node_data['inputs']['seed']}")

        print(" Sending prompt to ComfyUI...")
        prompt_response = self.queue_prompt(workflow)
        prompt_id = prompt_response['prompt_id']

        print(f" Generating image (Prompt ID: {prompt_id})...")
        self.track_progress(prompt_id)

        print(" Generation complete! Downloading image...")
        history_response = self.get_history(prompt_id)

        # Check if prompt_id exists in history
        if prompt_id not in history_response:
            raise Exception(f"Prompt ID {prompt_id} not found in history")

        history = history_response[prompt_id]

        # Get output images
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                for image in node_output['images']:
                    image_data = self.get_image(
                        image['filename'],
                        image['subfolder'],
                        image['type']
                    )

                    #  
                    output_filename = f"nft_{index:03d}.png"
                    output_path = self.output_dir / output_filename

                    with open(output_path, 'wb') as f:
                        f.write(image_data)

                    print(f" Saved: {output_path}")
                    return str(output_path)

        raise Exception("Failed to generate image")


def generate_image(style, custom_prompt=None, index=1):
    """
    Generate image (with simulation fallback if ComfyUI unavailable)
    """
    try:
        generator = ComfyUIImageGenerator()
        return generator.generate(style, custom_prompt, index)
    except Exception as e:
        print(f" [WARN] ComfyUI generation failed: {str(e)}")
        print(" [INFO] Using simulation mode...")

        # Create simulation image
        from PIL import Image, ImageDraw, ImageFont
        import random

        img = Image.new('RGB', (512, 512), color=(random.randint(50, 150), random.randint(50, 150), random.randint(50, 150)))
        draw = ImageDraw.Draw(img)

        # Add text
        text_lines = [
            f"NFT #{index:03d}",
            f"Style: {style}",
            "SIMULATION MODE",
            "(Install ComfyUI for real generation)"
        ]

        y_position = 180
        for line in text_lines:
            # Simple text without font
            bbox = draw.textbbox((0, 0), line)
            text_width = bbox[2] - bbox[0]
            x_position = (512 - text_width) // 2
            draw.text((x_position, y_position), line, fill=(255, 255, 255))
            y_position += 40

        # Save
        output_dir = Path("output/images")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_filename = f"nft_{index:03d}.png"
        output_path = output_dir / output_filename

        img.save(output_path)
        print(f" [OK] Simulation image saved: {output_path}")
        return str(output_path)


if __name__ == "__main__":
    # 
    print("Testing image generation...")
    result = generate_image("realistic", index=999)
    print(f"Test image saved: {result}")
