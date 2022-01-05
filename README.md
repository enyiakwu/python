## python
python scripts - mostly automation scripts


You can set your environment in various ways

#### bash
```
#!/bin/bash
```

#### python - locally on remote host
```
#!/bin/python
```

#### python3 - on remote host
```
#!/bin/python3
```

#### python - virtual env
```
#!/bin/bash
set -e
source ~/docker-lib/virtualenv.sh
pip3.6 install requests
pip3.6 install "python-slugify"
# <install other dependencies>
```

#### python - virtual env_2
```
#!/bin/bash
set -e
source ~/docker-lib/virtualenv.sh

pip3.6 install PyGithub
pip3.6 install requests
```
