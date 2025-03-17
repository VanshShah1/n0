import flet as ft
from g4f.client import Client
import re

client = Client()

class UIComponentGenerator:
    def __init__(self):
        self.chat_history = [
            {"role": "system", "content": """You are a professional UI/UX designer. 
            Generate clean, modern HTML/CSS/JS code for UI components based on user prompts. 
            Follow these rules:
            1. Use semantic HTML5
            2. CSS variables for theming
            3. Mobile-first responsive design
            4. Smooth CSS animations
            5. Modern styling with shadows and gradients
            6. Combine all code in one HTML file
            7. Include interactive elements where appropriate
            8. Use Flexbox or Grid for layouts
            9. Add comments for key sections"""}
        ]

    async def generate_component(self, prompt):
        self.chat_history.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=self.chat_history
        )
        
        content = response.choices[0].message.content
        self.chat_history.append({"role": "assistant", "content": content})
        
        html_content = re.sub(r'``````', '', content).strip()
        return html_content

async def main(page: ft.Page):
    page.title = "AI Component Studio"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.fonts = {"primary": "Roboto"}
    page.padding = 20
    
    generator = UIComponentGenerator()
    current_html = ft.Text()
    has_generated = False
    
    # UI Components
    title = ft.Text("AI Component Studio", size=24, weight="bold", text_align="center")
    
    prompt_field = ft.TextField(
        label="Describe your UI component",
        hint_text="e.g., 'A modern login form with gradient background and hover effects'",
        multiline=True,
        min_lines=1,
        max_lines=3,
        expand=True,
        filled=True,
        border_radius=15,
        border_color=ft.colors.GREY_300,
        on_submit=lambda e: submit_prompt(e)
    )
    
    submit_btn = ft.ElevatedButton(
        "Generate",
        icon=ft.icons.SEND,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor=ft.colors.BLACK,
            color=ft.colors.WHITE
        )
    )
    
    preview_tab = ft.Tab(
        text="Preview",
        content=ft.Container(
            content=ft.Html("", expand=True),
            border_radius=15,
            bgcolor=ft.colors.GREY_50,
            padding=10
        )
    )
    
    code_tab = ft.Tab(
        text="Code",
        content=ft.Column([
            ft.IconButton(
                icon=ft.icons.COPY,
                on_click=lambda e: page.set_clipboard(current_html.value),
                top=10,
                right=10,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.WHITE,
                    color=ft.colors.BLACK
                )
            ),
            ft.Container(
                content=current_html,
                expand=True,
                border_radius=15,
                bgcolor=ft.colors.GREY_50,
                padding=20,
                scroll=ft.ScrollMode.ALWAYS
            )
        ], spacing=0)
    )
    
    tabs = ft.Tabs(
        tabs=[preview_tab, code_tab],
        expand=True,
        animation_duration=300
    )
    
    async def submit_prompt(e):
        nonlocal has_generated
        html_code = await generator.generate_component(prompt_field.value)
        current_html.value = html_code
        preview_tab.content.content.value = html_code
        
        if not has_generated:
            page.add(followup_row)
            has_generated = True
            
        await page.update_async()
    
    submit_btn.on_click = submit_prompt
    
    followup_field = ft.TextField(
        label="Modify your component...",
        expand=True,
        border_radius=15,
        filled=True,
        border_color=ft.colors.GREY_300
    )
    
    followup_row = ft.ResponsiveRow([
        ft.Column([
            followup_field,
            ft.ElevatedButton("Apply Changes", on_click=submit_prompt)
        ], col={"sm": 12, "md": 10})
    ], visible=False)
    
    layout = ft.Column([
        title,
        ft.ResponsiveRow([
            ft.Column([prompt_field], col={"sm": 12, "md": 10}),
            ft.Column([submit_btn], col={"sm": 12, "md": 2})
        ], vertical_alignment="center"),
        ft.Divider(),
        tabs
    ], spacing=20)
    
    page.add(layout)

ft.app(target=main)
