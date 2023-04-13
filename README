# Plugin for manage LoadBalancer with Netbox

## How to install plugin

### 1. Incase Netbox Manual Install

This plugin require installed netbox first, if you don't have netbox please refer this document to install it (https://docs.netbox.dev/en/stable/installation/)

Install Plugin with `pip`

```
source /opt/netbox/venv/bin/activate
```

```
cd /opt/netbox/netbox
pip3 install netbox-loadbalancer
```

```
sudo sh -c "echo 'django-auth-ldap' >> /opt/netbox/local_requirements.txt"
```

Enable plugin in `/opt/netbox/netbox/netbox/configuration.py`

```
PLUGINS = [
    'netbox_loadbalancer'
]
```

Migrate Database for newly Plugin

```
cd /opt/netbox/netbox
python3 manage.py migrate
```

Restart Netbox service

```
sudo systemctl restart netbox netbox-rq
```

### 2. Incase Netbox Install with Docker compose

To install netbox with docker-compose use this repository (https://github.com/netbox-community/netbox-docker)

Suppose you use `/opt` for netbox docker working directory

First, Re-build base image for netbox

```
mkdir /tmp/netbox-docker-rebuild && cd /tmp/netbox-docker-rebuild
```

```
cat << EOF > plugin_requirements.txt
gunicorn
netbox-loadbalancer
EOF
```

```
cat << EOF > Dockerfile
FROM netboxcommunity/netbox:v3.4-2.4.0

COPY plugin_requirements.txt /
RUN /opt/netbox/venv/bin/pip install  --no-warn-script-location -r /plugin_requirements.txt
EOF
```

```
docker build -t netbox-custom:latest .
```

Then Change config for netbox docker

```
cd /opt/netbox-docker/
```

Change image from `docker-compose.yml`

```
version: '3.4'
services:
  netbox: &netbox
    image: netbox-custom:latest <-- Change this line to your custom image name
    depends_on:
    - postgres
    - redis
...
```

Add plugin to `/opt/netbox-docker/configuration/configuration.py`

```
PLUGINS = [
    'netbox_loadbalancer'
]
```

Finally Run Netbox with docker-compose

```
cd /opt/netbox-docker/
docker-compose up
```