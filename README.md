# TJADB
## What is TJADB?
TJADB is a community 

> dedicated to the preservation, creation, and overall discussion of TJA files and Taiko no Tatsujin (太鼓の達人) charting!

This resulted in this project, as a way of storing and hosting the custom TJA files created by the community, and making them searchable. This project has since grown, working together with the [OpenTaiko project](https://github.com/0auBSQ/OpenTaiko), and aligning its development cycle with OpenTaiko, to improve both projects.

## Installation
Installation is fairly straightforward.

### (Optionally) Setting up a virtual environment
``` shell
virtualenv -p python3 venv
source venv/bin/activate
```

### Installing the requirements
``` shell
pip install -r website/requirements.txt
```


### Localization
To allow the web server to serve pages in multiple languages, localization has to happen. We can do this by running the following code, from the root of the project folder. Make sure that - if you use a virtual environment, that it is loaded.
``` shell
python3 website/locale/localize.py generate
django-admin compilemessages
```

## License
This is free software released under the "GNU Affero General Public License v3.0"

````
Copyright (c) 2021  Pieter-Jan Moreels - https://github.com/pidgeyl/
Copyright (c) 2021  TJADB Community - https://discord.com/invite/XHcVYKW
````

## Shout-outs
This section is for people who helped out the project by sponsoring the server that runs the public TJADB website and Discord bot.

````
@Y2K-x
Hue#1629
And others
````
