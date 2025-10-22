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
           
        """
        workflow_files = {
            "realistic": "sd15_realistic_lcm.json",
            "ghibli": "sd15_ghibli_lcm.json",
            "pixelart": "sd15_pixelart_lcm.json",
            "flat2d_anime": "sd15_flat2d_anime_lcm.json"
        }

        workflow_path = self.workflow_dir / workflow_files.get(style, workflow_files["realistic"])

        if not workflow_path.exists():
            #   ComfyUI   
            comfyui_workflow = Path(f"C:/StabilityMatrix/Data/Packages/ComfyUI/user/default/workflows/{workflow_files[style]}")
            if comfyui_workflow.exists():
                import shutil
                shutil.copy(comfyui_workflow, workflow_path)

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

        #   ()
        if custom_prompt:
            # positive prompt  
            for node_id, node_data in workflow.items():
                if node_data.get("class_type") == "CLIPTextEncode":
                    if "inputs" in node_data and "text" in node_data["inputs"]:
                        #   CLIPTextEncode positive prompt
                        node_data["inputs"]["text"] = custom_prompt
                        break

        # Seed  (   )
        import random
        for node_id, node_data in workflow.items():
            if node_data.get("class_type") == "KSampler":
                node_data["inputs"]["seed"] = random.randint(1, 2**32 - 1)

        print(" Sending prompt to ComfyUI...")
        prompt_response = self.queue_prompt(workflow)
        prompt_id = prompt_response['prompt_id']

        print(f" Generating image (Prompt ID: {prompt_id})...")
        self.track_progress(prompt_id)

        print(" Generation complete! Downloading image...")
        history = self.get_history(prompt_id)[prompt_id]

        #   
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
      
    """
    generator = ComfyUIImageGenerator()
    return generator.generate(style, custom_prompt, index)


if __name__ == "__main__":
    # 
    print("Testing image generation...")
    result = generate_image("realistic", index=999)
    print(f"Test image saved: {result}")
