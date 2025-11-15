Get rid of the ansible and apt.txt. We go full on pure mkosi.
Put the package configuration into mkosi config files in mkosi.conf.d/. The new config files should have the same name as the old roles.
All config files go into /etc and are globally configured.
Create a clean-mkhome-after-d9-migration script in /usr/local/bin/ that gets installed automatically that cleans up all previously home directory configured config files that are now hanlded globally.
For templates with config options, install python jinja apt package in the buildroot environment and create a build script that renders them all from a central d9.yaml in the src directory. 
