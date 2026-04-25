from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader(searchpath='./src/templates/'))

def render_template(template_name: str, params: dict):
    template = env.get_template(template_name)
    return template.render(params)