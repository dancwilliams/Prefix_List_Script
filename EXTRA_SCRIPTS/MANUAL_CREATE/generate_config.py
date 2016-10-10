from jinja2 import Environment, FileSystemLoader
import yaml
import os.path

ENV = Environment(loader=FileSystemLoader('./'))
script_path = 'SCRIPTS/'
allowed_script = os.path.join(script_path, 'allowed.txt')
remediation_script = os.path.join(script_path, 'remediation.txt')

with open("config.yaml") as _:
    yaml_dict =  yaml.load(_)

allowed_dict = yaml_dict['allowed']

remediation_dict = yaml_dict['remediation']

# Render template and print generated config to console
template = ENV.get_template("allowed_template.text")
print(template.render(config=allowed_dict))

with open(allowed_script, 'w') as outfile:
    temp = template.render(config=allowed_dict)
    outfile.write(temp)

template = ENV.get_template("remediation_template.text")
print(template.render(config=remediation_dict))

with open(remediation_script, 'w') as outfile:
    temp = template.render(config=remediation_dict)
    outfile.write(temp)
