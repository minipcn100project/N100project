# scripts/workflow_converter.py
"""
Convert ComfyUI UI workflow format to API format
"""
import json

def convert_ui_to_api(ui_workflow):
    """
    Convert ComfyUI UI format workflow to API format

    UI format has 'nodes' and 'links'
    API format is a dict of node_id -> node_config
    """
    if "nodes" not in ui_workflow:
        # Already in API format
        return ui_workflow

    api_workflow = {}

    # Create a map of link IDs to their source/target
    link_map = {}
    for link in ui_workflow.get("links", []):
        # link format: [link_id, source_node, source_slot, target_node, target_slot, type]
        link_id = link[0]
        link_map[link_id] = {
            "source_node": link[1],
            "source_slot": link[2],
            "target_node": link[3],
            "target_slot": link[4],
            "type": link[5]
        }

    # Process each node
    for node in ui_workflow["nodes"]:
        node_id = str(node["id"])
        node_type = node["type"]

        # Skip Note and other non-functional nodes
        if node_type in ["Note", "Reroute"]:
            continue

        # Create API node structure
        api_node = {
            "class_type": node_type,
            "inputs": {}
        }

        # Add widget values as inputs
        if "widgets_values" in node and node["widgets_values"]:
            widget_values = node["widgets_values"]

            # Map widget values to input names based on node type
            if node_type == "CheckpointLoaderSimple":
                if len(widget_values) > 0:
                    api_node["inputs"]["ckpt_name"] = widget_values[0]

            elif node_type == "LoraLoader":
                if len(widget_values) >= 3:
                    api_node["inputs"]["lora_name"] = widget_values[0]
                    api_node["inputs"]["strength_model"] = widget_values[1]
                    api_node["inputs"]["strength_clip"] = widget_values[2]

            elif node_type == "CLIPTextEncode":
                if len(widget_values) > 0:
                    api_node["inputs"]["text"] = widget_values[0]

            elif node_type == "KSampler":
                if len(widget_values) >= 7:
                    api_node["inputs"]["seed"] = widget_values[0]
                    api_node["inputs"]["control_after_generate"] = widget_values[1]
                    api_node["inputs"]["steps"] = widget_values[2]
                    api_node["inputs"]["cfg"] = widget_values[3]
                    api_node["inputs"]["sampler_name"] = widget_values[4]
                    api_node["inputs"]["scheduler"] = widget_values[5]
                    api_node["inputs"]["denoise"] = widget_values[6]

            elif node_type == "EmptyLatentImage":
                if len(widget_values) >= 3:
                    api_node["inputs"]["width"] = widget_values[0]
                    api_node["inputs"]["height"] = widget_values[1]
                    api_node["inputs"]["batch_size"] = widget_values[2]

            elif node_type == "SaveImage":
                if len(widget_values) > 0:
                    api_node["inputs"]["filename_prefix"] = widget_values[0]

        # Add input connections from links
        if "inputs" in node:
            for input_def in node["inputs"]:
                if "link" in input_def and input_def["link"] is not None:
                    link_id = input_def["link"]
                    if link_id in link_map:
                        link_info = link_map[link_id]
                        source_node_id = str(link_info["source_node"])
                        source_slot = link_info["source_slot"]
                        input_name = input_def["name"]

                        # Create connection reference
                        api_node["inputs"][input_name] = [source_node_id, source_slot]

        api_workflow[node_id] = api_node

    return api_workflow


if __name__ == "__main__":
    # Test conversion
    import sys
    from pathlib import Path

    if len(sys.argv) > 1:
        workflow_path = Path(sys.argv[1])
    else:
        workflow_path = Path("config/workflows/sd15_pixelart_lcm.json")

    print(f"Converting {workflow_path}...")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        ui_workflow = json.load(f)

    api_workflow = convert_ui_to_api(ui_workflow)

    # Save converted workflow
    output_path = workflow_path.parent / f"{workflow_path.stem}_api.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(api_workflow, f, indent=2)

    print(f"Converted workflow saved to: {output_path}")
    print(f"Nodes: {len(api_workflow)}")
