import streamlit as st
import requests
import subprocess
import webbrowser
import os
import time
import zipfile

# Set page configuration
st.set_page_config(page_title="Artifacts Ai", layout="wide")

# Custom Styling
st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap');

        html, body {{
            font-family: 'Outfit', sans-serif;
            background: linear-gradient(135deg, #e0f7fa, #e1bee7);
            color: #1a1a1a;
            margin: 0;
            padding: 0;
            animation: fadeInBackground 1.5s ease-in-out;
        }}

        @keyframes fadeInBackground {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        @keyframes slideFadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .main-title {{
            text-align: center;
            font-size: 3em;
            font-weight: 700;
            background: linear-gradient(90deg, #7b1fa2, #00acc1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: slideFadeIn 1.8s ease-out;
            margin-bottom: 2rem;
        }}

        .glass-box {{
            background: rgba(255, 255, 255, 0.4);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.2);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            animation: slideFadeIn 2s ease;
        }}

        .stTextArea > div > div > textarea {{
            height: 100px !important;
            border-radius: 10px !important;
            padding: 14px !important;
            font-size: 1rem !important;
            font-family: 'Outfit', sans-serif !important;
            border: 1px solid #cccccc;
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
        }}

        .stTextArea > div > div > textarea:focus {{
            border-color: #7b1fa2 !important;
            box-shadow: 0 0 0 3px rgba(123, 31, 162, 0.2) !important;
            outline: none !important;
        }}

        .stButton > button {{
            background: linear-gradient(90deg, #7b1fa2, #00acc1);
            color: white !important;
            font-weight: 600;
            border: none;
            border-radius: 10px;
            padding: 0.7rem 1.5rem;
            font-size: 1rem;
            transition: background 0.3s ease, transform 0.2s ease;
            box-shadow: 0 4px 14px rgba(0,0,0,0.1);
        }}

        .stButton > button:hover {{
            transform: translateY(-2px);
            background: linear-gradient(90deg, #8e24aa, #26c6da);
            color: white !important;
        }}


        .stButton > button:active {{
            transform: translateY(0px);
        }}

        .fade-in {{
            animation: slideFadeIn 1.2s ease-in-out;
        }}
    
        
""", unsafe_allow_html=True)

API_KEY = "fbc41e2b2c5eb3ae16060b4dce94e1f5e557734e0c92f0dc528fdad99d717a8d"




# Title
st.markdown('<div class="main-title">Artifact-AI</div>', unsafe_allow_html=True)

# User input for generating new component
st.markdown("<div class='input-box fade-in'>", unsafe_allow_html=True)
user_input = st.text_area("Enter component description:", placeholder="Describe the React component...", height=80)
st.markdown("</div>", unsafe_allow_html=True)

# Generate Button
st.markdown("<div class='submit-btn fade-in'>", unsafe_allow_html=True)
if st.button("Generate"):
    if not user_input.strip():
        st.error("Please enter a description!")
    else:

        st.info("⏳ Thinking... Please wait.")
        try:
            response = requests.post(
                "https://artifacts-ai-backend.onrender.com/generate-react",
                json={"userInput": user_input},
                headers={"Content-Type": "application/json"},
            )
            if response.status_code == 200:
                data = response.json()
                if "code" in data:
                    st.success("✅ Component Generated Successfully!")

                    # Clean the code by removing triple backticks if they exist
                    full_code = data["code"].strip()  # Remove leading/trailing spaces
                    if full_code.startswith("```") and full_code.endswith("```"):
                        full_code = full_code[3:-3].strip()  # Remove the first & last 3 characters

                    # Display code with a typing effect
                    code_container = st.empty()
                    displayed_code = ""

                    for line in full_code.split("\n"):
                        displayed_code += line + "\n"
                        code_container.code(displayed_code, language="tsx")
                        time.sleep(0.1)  # Typing speed (adjustable)

                else:
                    st.error("❌ Error: No code returned.")
            else:
                st.error("❌ Error: Failed to generate component.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


# Modify React Component
st.markdown("<div class='input-box fade-in'>", unsafe_allow_html=True)
modification_input = st.text_area("Enter modification instructions:", placeholder="Describe the changes...", height=80)
st.markdown("</div>", unsafe_allow_html=True)

if st.button("Modify"):
    if not modification_input.strip():
        st.error("Please enter modification instructions!")
    else:
        st.info("⏳ Modifying... Please wait.")
        try:
            response = requests.post(
                "http://localhost:5000/modify-react",
                json={"userInput": modification_input},
                headers={"Content-Type": "application/json"},
            )
            if response.status_code == 200:
                data = response.json()
                if "code" in data:
                    st.success("✅ Component Modified Successfully!")

                    # Clean the modified code by removing triple backticks if present
                    full_code = data["code"].strip()
                    if full_code.startswith("```") and full_code.endswith("```"):
                        full_code = full_code[3:-3].strip()

                    # Typing effect for displaying modified code
                    code_container = st.empty()
                    displayed_code = ""

                    for line in full_code.split("\n"):
                        displayed_code += line + "\n"
                        code_container.code(displayed_code, language="tsx")
                        time.sleep(0.1)  # Adjust typing speed as needed

                else:
                    st.error("❌ Error: No modified code returned.")
            else:
                st.error("❌ Error: Failed to modify component.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


# Download Button
st.markdown("<div class='submit-btn fade-in'>", unsafe_allow_html=True)
if st.sidebar.button("Download"):
    # Copy content from add.tsx to files/App.tsx
    add_file_path = "D:\\artifacts-ai\\add.tsx"
    app_file_path = "D:\\artifacts-ai\\files\\App.tsx"
    
    with open(add_file_path, 'r', encoding='utf-8') as add_file:
        add_content = add_file.read()
    
    with open(app_file_path, 'w', encoding='utf-8') as app_file:
        app_file.write(add_content)
    
    # Create a zip file of the files/ directory
    zip_file_path = "D:\\artifacts-ai\\files.zip"
    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        for foldername, subfolders, filenames in os.walk("D:\\artifacts-ai\\files"):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                zip_file.write(file_path, os.path.relpath(file_path, "D:\\artifacts-ai\\files"))
    
    # Provide download link for the zip file
    with open(zip_file_path, "rb") as f:
        st.sidebar.download_button("Confirm Download", f, file_name="files.zip")

if st.sidebar.button("View Latest Component"):
    try:
        response = requests.get("http://localhost:5000/view-latest")
        if response.status_code == 200:
            data = response.json()
            if "code" in data:
                st.code(data["code"], language="tsx")
            else:
                st.error("❌ No code found.")
        else:
            st.error("❌ Error: Could not retrieve the latest component.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

if st.sidebar.button("Website Preview"):
    # Trigger the overlay using JS
    st.components.v1.html("<script>showOverlay();</script>", height=0)

    def run_script():
        try:
            result = subprocess.run(
                ["node","D:\\artifacts-ai\\sandbox_creator.js"],
                capture_output=True, text=True, shell=True, encoding="utf-8"
            )
            return result.stdout
        except Exception as e:
            return e
    
    def remove_first_and_last_line(file_path: str) -> None:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            if len(lines) <= 2:
                return
            
            start = 1 if ('```' in lines[0] or '"""' in lines[0]) else 0
            end = -1 if ('```' in lines[-1] or '"""' in lines[-1]) else None
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(lines[start:end])
        except Exception as e:
            print(f"Error processing file: {e}")

    file_path = os.path.abspath("D:\\artifacts-ai\\add.tsx")
    remove_first_and_last_line(file_path)

    # Simulate execution with overlay
    st.write("Executing script...")
    stdout = run_script()

    # Hide overlay
    st.components.v1.html("<script>hideOverlay();</script>", height=0)

    if stdout:
        filtered_output = "\n".join(
            line for line in stdout.split("\n") if "Creating sandbox..." not in line and "✅ Sandbox Created Successfully!" not in line
        )
        st.text_area("Output:", filtered_output, height=200)
        for line in filtered_output.split("\n"):
            if "Preview URL:" in line:
                url = line.split("Preview URL:")[1].strip()
                webbrowser.open(url)
