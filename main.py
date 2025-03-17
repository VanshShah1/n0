import Neutron
from g4f.client import Client
import re
import pyperclip
from markupsafe import Markup

client = Client()

SYSTEM_PROMPT = """
You are a professional UI/UX designer and frontend developer. Generate clean, modern, responsive HTML/CSS/JS code based on user's description.

Rules:
1. Respond ONLY with code inside <result> tags
2. Combine in single HTML file
3. Use modern CSS features
4. No markdown or backticks
5. Ensure valid HTML syntax
6. Escape special characters
7. Include proper meta tags

Wrap final code in <result></result>
"""

chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]

def sanitize_code(code):
    """Clean and validate generated code"""
    code = re.sub(r'```html|```', '', code)
    code = re.sub(r'<think>.*?</think>', '', code, flags=re.DOTALL)
    return Markup(code.strip())

def extract_code(response):
    match = re.search(r'<result>(.*?)</result>', response, re.DOTALL)
    return sanitize_code(match.group(1)) if match else None

def generate_component(prompt):
    global chat_history
    chat_history.append({"role": "user", "content": prompt})
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=chat_history
        )
        ai_message = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": ai_message})
        return extract_code(ai_message)
    except Exception as e:
        print(f"AI Error: {str(e)}")
        return None

win = Neutron.Window("UI Craft AI", size=(1200, 800), css="def.css")
win.display(file="render.html")

def update_ui(code):
    if not code:
        return
    
    # Create safe iframe content
    iframe_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <base target="_blank">
        <style>
            body {{ 
                margin: 0;
                padding: 1rem;
                font-family: inherit;
            }}
            {code.split('<style>')[-1].split('</style>')[0] if '<style>' in code else ''}
        </style>
    </head>
    <body>
        {code.split('<body>')[-1].split('</body>')[0] if '<body>' in code else code}
    </body>
    </html>
    """
    
    preview_frame = win.getElementById("previewFrame")
    preview_frame.srcdoc = iframe_content
    
    code_content = win.getElementById("codeContent")
    code_content.textContent = iframe_content
    
    win.getElementById("followUpSection").classList.remove("hidden")

def handle_submit():
    prompt = win.getElementById("promptInput").value
    if prompt:
        code = generate_component(prompt)
        if code:
            update_ui(code)
        win.getElementById("promptInput").value = ""

def handle_follow_up():
    prompt = win.getElementById("followUpInput").value
    if prompt:
        code = generate_component(prompt)
        if code:
            update_ui(code)
        win.getElementById("followUpInput").value = ""

# Fixed event listeners
win.getElementById("submitBtn").addEventListener("click", Neutron.event(handle_submit))
win.getElementById("promptInput").addEventListener("keypress", 
    Neutron.event(lambda: handle_submit() if win.getElementById("promptInput").value else None))

win.getElementById("followUpBtn").addEventListener("click", Neutron.event(handle_follow_up))
win.getElementById("followUpInput").addEventListener("keypress", 
    Neutron.event(lambda: handle_follow_up() if win.getElementById("followUpInput").value else None))

def copy_code():
    code = win.getElementById("codeContent").textContent
    pyperclip.copy(code)
    print("Code copied to clipboard!")

win.getElementById("copyBtn").addEventListener("click", Neutron.event(copy_code))

win.show()