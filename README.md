## python
python scripts - mostly automation scripts


You can set your environment in various ways

#### BASH
```
#!/bin/bash
```

#### PYTHON - locally on remote host
```
#!/bin/python
```

#### PYTHON3 - on remote host
```
#!/bin/python3
```

#### PYTHON - virtual env
```
#!/bin/bash
set -e
source ~/docker-lib/virtualenv.sh
pip3.6 install requests
pip3.6 install "python-slugify"
# <install other dependables>
```

#### PYTHON - virtual env_2
```
#!/bin/bash
set -e
source ~/docker-lib/virtualenv.sh

pip3.6 install PyGithub
pip3.6 install requests
```
