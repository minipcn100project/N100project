# scripts/image_generator.py
"""
ComfyUI API를 통한 이미지 생성
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

        # 워크플로우 파일 경로
        self.workflow_dir = Path("config/workflows")
        self.output_dir = Path("output/images")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_workflow(self, style):
        """
        스타일에 맞는 워크플로우 로드
        """
        workflow_files = {
            "realistic": "sd15_realistic_lcm.json",
            "ghibli": "sd15_ghibli_lcm.json",
            "pixelart": "sd15_pixelart_lcm.json",
            "flat2d_anime": "sd15_flat2d_anime_lcm.json"
        }

        workflow_path = self.workflow_dir / workflow_files.get(style, workflow_files["realistic"])

        if not workflow_path.exists():
            # 워크플로우가 없으면 ComfyUI 설치 경로에서 복사
            comfyui_workflow = Path(f"C:/StabilityMatrix/Data/Packages/ComfyUI/user/default/workflows/{workflow_files[style]}")
            if comfyui_workflow.exists():
                import shutil
                shutil.copy(comfyui_workflow, workflow_path)

        with open(workflow_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def queue_prompt(self, prompt):
        """
        ComfyUI에 프롬프트 전송
        """
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{self.server_address}/prompt", data=data)
        response = urllib.request.urlopen(req).read()
        return json.loads(response)

    def get_image(self, filename, subfolder, folder_type):
        """
        생성된 이미지 다운로드
        """
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)

        with urllib.request.urlopen(f"http://{self.server_address}/view?{url_values}") as response:
            return response.read()

    def get_history(self, prompt_id):
        """
        생성 히스토리 조회
        """
        with urllib.request.urlopen(f"http://{self.server_address}/history/{prompt_id}") as response:
            return json.loads(response.read())

    def track_progress(self, prompt_id):
        """
        WebSocket으로 진행상황 추적
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
                        break  # 완료
                    else:
                        print(f"⏳ Executing node: {data['node']}")

        ws.close()

    def generate(self, style, custom_prompt=None, index=1):
        """
        이미지 생성 메인 함수

        Args:
            style: "realistic", "ghibli", "pixelart", "flat2d_anime"
            custom_prompt: 사용자 정의 프롬프트 (선택)
            index: NFT 번호

        Returns:
            생성된 이미지 파일 경로
        """
        print(f"🎨 Loading {style} workflow...")
        workflow = self.load_workflow(style)

        # 프롬프트 커스터마이즈 (선택)
        if custom_prompt:
            # positive prompt를 찾아서 교체
            for node_id, node_data in workflow.items():
                if node_data.get("class_type") == "CLIPTextEncode":
                    if "inputs" in node_data and "text" in node_data["inputs"]:
                        # 첫 번째 CLIPTextEncode가 positive prompt
                        node_data["inputs"]["text"] = custom_prompt
                        break

        # Seed 랜덤화 (매번 다른 이미지 생성)
        import random
        for node_id, node_data in workflow.items():
            if node_data.get("class_type") == "KSampler":
                node_data["inputs"]["seed"] = random.randint(1, 2**32 - 1)

        print("📤 Sending prompt to ComfyUI...")
        prompt_response = self.queue_prompt(workflow)
        prompt_id = prompt_response['prompt_id']

        print(f"⏳ Generating image (Prompt ID: {prompt_id})...")
        self.track_progress(prompt_id)

        print("✅ Generation complete! Downloading image...")
        history = self.get_history(prompt_id)[prompt_id]

        # 생성된 이미지 찾기
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                for image in node_output['images']:
                    image_data = self.get_image(
                        image['filename'],
                        image['subfolder'],
                        image['type']
                    )

                    # 파일 저장
                    output_filename = f"nft_{index:03d}.png"
                    output_path = self.output_dir / output_filename

                    with open(output_path, 'wb') as f:
                        f.write(image_data)

                    print(f"💾 Saved: {output_path}")
                    return str(output_path)

        raise Exception("Failed to generate image")


def generate_image(style, custom_prompt=None, index=1):
    """
    간편 사용 함수
    """
    generator = ComfyUIImageGenerator()
    return generator.generate(style, custom_prompt, index)


if __name__ == "__main__":
    # 테스트
    print("Testing image generation...")
    result = generate_image("realistic", index=999)
    print(f"Test image saved: {result}")
