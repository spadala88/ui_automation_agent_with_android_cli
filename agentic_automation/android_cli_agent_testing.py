import time
import subprocess
import os
import json
import ollama
from llm_ollama import call_llm
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool

# ==========================================
# 1. DEFINE UPDATED AGENT TOOLS (Android CLI)
# ==========================================

@tool
def install_apk_from_parent() -> str:
    """Finds the first .apk file in the parent directory and installs it via ADB."""
    print(" 🔧 AGENT ACTION: Locating and installing APK...")
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
        apks = [f for f in os.listdir(parent_dir) if f.endswith('.apk')]
        
        if not apks:
            return "Error: No APK found in the parent directory."
        
        apk_path = os.path.join(parent_dir, apks[0])
        # Using -r to replace existing application
        result = subprocess.run(f'adb install -r "{apk_path}"', capture_output=True, text=True, shell=True)
        return f"Successfully installed {apks[0]}." if result.returncode == 0 else f"Failed: {result.stderr}"
    except Exception as e:
        return f"Error during installation: {e}"

@tool
def start_test_activity() -> str:
    """Starts the application directly using an ADB shell command."""
    print(" 🔧 AGENT ACTION: Starting activity via ADB...")
    # Target activity from source
    cmd = "adb shell am start -n com.example.navuiact/com.example.navuiact.MainActivity"
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return "Activity started successfully." if result.returncode == 0 else f"Failed: {result.stderr}"

def find_element_by_label(label: str):
    """Finds an element by text content in the UI layout."""
    try:
        cmd = "android layout -p"
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        
        if result.returncode != 0:
            print(f"  ❌ Layout command failed: {result.stderr}")
            return None
        
        layout_data = json.loads(result.stdout)
        print(f"  📄 Layout has {len(layout_data) if isinstance(layout_data, list) else 1} element(s)")
        
        # Handle both flat array and nested structure
        if isinstance(layout_data, list):
            # Flat array structure - search directly
            print(f"  🔍 Searching in flat array for text matching '{label}'...")
            for i, element in enumerate(layout_data):
                if isinstance(element, dict):
                    text = element.get('text', '')
                    print(f"    Element {i}: text='{text}'")
                    if text and label.lower() == text.lower():
                        center = element.get('center')
                        print(f"    ✅ Match found! center={center}")
                        if center:
                            return center
        elif isinstance(layout_data, dict):
            # Nested structure - search recursively
            def search_layout(node):
                if isinstance(node, dict):
                    text = node.get('text', '')
                    if text and label.lower() in text.lower():
                        bounds = node.get('bounds')
                        center = node.get('center')
                        return bounds or center
                    
                    for child in node.get('children', []):
                        found = search_layout(child)
                        if found:
                            return found
                return None
            
            return search_layout(layout_data)
        
        print(f"  ❌ No matching element found for '{label}'")
        return None
    except Exception as e:
        print(f"Error finding element: {e}")
        return None

def extract_coordinates(coord_str: str):
    """Extracts coordinates from either center format '[x,y]' or bounds format '[x1,y1][x2,y2]'."""
    try:
        import re
        # Try center format first: [x,y]
        match = re.match(r'\[(\d+),(\d+)\]$', coord_str)
        if match:
            x, y = map(int, match.groups())
            return x, y
        
        # Try bounds format: [x1,y1][x2,y2]
        match = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', coord_str)
        if match:
            x1, y1, x2, y2 = map(int, match.groups())
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            return center_x, center_y
    except Exception as e:
        print(f"Error parsing coordinates: {e}")
    
    return None

@tool
def click_via_android_cli(label: str) -> str:
    """Uses the Android CLI layout to find and click an element by label."""
    print(f" 🔧 AGENT ACTION: Resolving and clicking label '{label}'...")
    
    # Find element coordinates using layout command
    coords_str = find_element_by_label(label)
    if not coords_str:
        return f"Failed to click '{label}': Element not found in layout."
    
    print(f"  📍 Found coordinates string: {coords_str}")
    
    # Extract center coordinates
    coords = extract_coordinates(coords_str)
    if not coords:
        return f"Failed to click '{label}': Could not parse element coordinates."
    
    x, y = coords
    print(f"  📍 Extracted coordinates: x={x}, y={y}")
    
    # Use ADB to tap at the coordinates (primary method)
    cmd = f"adb shell input tap {x} {y}"
    print(f"  🖱️ Executing: {cmd}")
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    
    if result.returncode == 0:
        print(f"  ✅ Tap command executed successfully")
        # Add a small delay to let the UI respond
        import time
        time.sleep(0.5)
        return f"Successfully clicked '{label}' at coordinates ({x}, {y})."
    else:
        print(f"  ❌ Tap command failed: {result.stderr}")
        return f"Failed to click '{label}': {result.stderr}"

@tool
def wait_for_ui(seconds: int) -> str:
    """Pause execution to allow for app loading or transitions."""
    print(f" 🔧 AGENT ACTION: Waiting for {seconds}s...")
    time.sleep(seconds)
    return f"Wait for {seconds}s complete."

# ==========================================
# 2. AGENT CONFIGURATION & ORCHESTRATION
# ==========================================

available_tools = [install_apk_from_parent, start_test_activity, click_via_android_cli, wait_for_ui]

def run_agentic_flow():
    # 1. Define the multi-step objective with repetition
    objective = """
    Execute these steps exactly:
    1. Install the APK from the parent folder.
    2. Start the activity 'com.example.navuiact/com.example.navuiact.MainActivity'.
    3. Wait 5 seconds for the UI to stabilize.
    4. Perform this sequence 3 times: Click 'Home', then click 'Favorites', then click 'Profile'.
    """

    print("🚀 Starting Agent UI Orchestration...\n")
    messages = [HumanMessage(content=objective)]
    
    max_retries = 1
    retry_count = 0

    while True:
        try:
            # 2. Call local Ollama through the existing interface
            response = call_llm(messages, tools=available_tools)
            messages.append(response)
            
            # Reset retry counter on successful LLM call
            retry_count = 0

            if response.tool_calls:
                for tool_call in response.tool_calls:
                    func_name = tool_call['name']
                    args = tool_call['args']
                    
                    # Build function map - use .name for StructuredTools
                    try:
                        func_map = {f.name: f for f in available_tools}
                    except AttributeError:
                        func_map = {f.__name__: f for f in available_tools}
                    
                    if func_name in func_map:
                        tool = func_map[func_name]
                        try:
                            result = tool.invoke(args)
                        except TypeError:
                            result = tool(**args)
                        print(f"📊 Result: {result}")
                        
                        # Feed the observation back to the LLM
                        messages.append(ToolMessage(
                            tool_call_id=tool_call['id'],
                            content=str(result)
                        ))
                    else:
                        print(f"❌ Tool {func_name} not found.")
                        print(f"Available tools: {list(func_map.keys())}")
                continue 
            
            else:
                print("\n✅ Final Agent Summary:", response.content)
                break

        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error in loop: {error_msg}")
            
            # Check if it's a server error and retry
            if "500" in error_msg or "Internal Server Error" in error_msg:
                retry_count += 1
                if retry_count <= max_retries:
                    print(f"🔄 Retrying ({retry_count}/{max_retries})...")
                    import time
                    time.sleep(2)  # Wait 2 seconds before retrying
                    continue
                else:
                    print(f"❌ Max retries reached. Giving up.")
                    break
            else:
                break

if __name__ == "__main__":
    run_agentic_flow()