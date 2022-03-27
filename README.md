# Machinists Toolbox

Django based app to

* Manage milling tool
* Calculate feeds recipies based on
  * the tool parameters 
  * the material to cut
  * the machine capabilities
* Generate FreeCAD Job Templates based on the feeds and speeds recipies

## Import Fixture data

```bash
./manage.py createsuperuser --username admin --email admin@localhost

./manage.py loaddata --format json --app material default
./manage.py loaddata --format json --app tool_library default
./manage.py loaddata --format json --app milling machines cutting_data
```

## Recreate migrations

```bash
fd -p '.*/migrations/\d.*\.py' -X rm
```