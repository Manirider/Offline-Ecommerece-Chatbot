import os


class PromptLoader:
    def __init__(self, prompts_dir="prompts"):
        self.prompts_dir = prompts_dir

    def load(self, filename):
        path = os.path.join(self.prompts_dir, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Prompt template not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def render(self, template, context):
        rendered = template
        for key, value in context.items():
            rendered = rendered.replace(f"{{{{{key}}}}}", value)
        return rendered
