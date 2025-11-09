# Refactor Ansible Roles from home Collection

I merged in the home collection at ./home/. Merge it into the mkhome collection at ./ and refactor the collection so we have one role for every functionality we are configuring. The grouping should come mostly from the files in home/roles/home/tasks/. Each role should be split into two task files called by the main.yaml, a home.yaml and a system.yaml. The system.yaml installs the necessary system packages and configures system wide configuration. The home.yaml configures the current users home directory with functions the user needs to use the apps. In the main.yaml there is a condition to see which mkhome_mode is activated, home, system or both.

See if this is finished completely and if so remove all ansible artifacts remaining.
