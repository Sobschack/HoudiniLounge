import os
import json

my_path = os.environ["HIP"]
my_file = "my_file.json"
database = os.path.join(my_path, my_file)
selection = hou.selectedNodes()

json_data = []
for nodes in selection:
    kids = nodes.children()
    for node in kids:
        json_data.append(node.name())
with open(database, "w") as link:
    json.dump(json_data, link, indent=4)
print("OK")