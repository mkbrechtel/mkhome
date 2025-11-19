#!/usr/bin/env python3
import os
import sys

# Read debian/control.stub
with open('debian/control.stub', 'r') as f:
    control_stub = f.read()

# Generate package entries from tasks/
packages = []
for task_file in sorted(os.listdir('tasks/')):
    task_path = os.path.join('tasks', task_file)
    if not os.path.isfile(task_path):
        continue

    with open(task_path, 'r') as f:
        lines = f.readlines()

    # Parse task file
    task_name = None
    description = ""
    depends = []
    recommends = []
    suggests = []

    in_description = False
    for line in lines:
        line = line.rstrip()
        if line.startswith('Task:'):
            task_name = line.split(':', 1)[1].strip()
        elif line.startswith('Description:'):
            description = line.split(':', 1)[1].strip()
            in_description = True
        elif line.startswith(' ') and in_description:
            description += " " + line.strip()
        elif line.startswith('Depends:'):
            in_description = False
            depends.append(line.split(':', 1)[1].strip())
        elif line.startswith('Recommends:'):
            in_description = False
            recommends.append(line.split(':', 1)[1].strip())
        elif line.startswith('Suggests:'):
            in_description = False
            suggests.append(line.split(':', 1)[1].strip())
        elif line and not line.startswith(' '):
            in_description = False

    if task_name:
        pkg_name = 'd9-' + task_name.lower().replace(' ', '-')
        pkg = f"\nPackage: {pkg_name}\n"
        pkg += "Architecture: all\n"
        if depends:
            pkg += f"Depends: ${{misc:Depends}}, {', '.join(depends)}\n"
        if recommends:
            pkg += f"Recommends: {', '.join(recommends)}\n"
        if suggests:
            pkg += f"Suggests: {', '.join(suggests)}\n"
        pkg += f"Description: {description}\n"
        packages.append(pkg)

# Write debian/control
with open('debian/control', 'w') as f:
    f.write(control_stub)
    f.write('\n')
    for pkg in packages:
        f.write(pkg)

print(f"Generated debian/control with {len(packages)} packages")
