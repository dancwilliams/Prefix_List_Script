from jinja2 import Environment, FileSystemLoader
import yaml
import os.path

ENV = Environment(loader=FileSystemLoader('./'))
script_path = 'SCRIPTS/'

script = os.path.join(script_path, 'script.txt')


with open("config.yaml") as _:
    yaml_dict =  yaml.load(_)

template = ENV.get_template("template.text")

with open(script, 'w') as outfile:
    temp = template.render(config=yaml_dict)
    outfile.write(temp)

