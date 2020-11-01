### Requirements
 - Python 3.7
 - PostgreSQL


### Prepare project and run services
```bash
for service in "routes" "users" "web_front" "web_routes" ; \
do python3 -m venv "$service" && source "${service}/bin/activate" && pip install -r "${service}/requirements.txt"; \
done

for db in "sso" "routes" "web_routes"; \
do createdb -U postgres "$db"; \ 
done

for service in "routes" "users" "web_routes"; \
do cd "$service" && alembic upgrade head && cd ..; \
done

for service in "routes" "users" "web_front" "web_routes"; \
do cd "$service" && python server.py & && cd ..

```


### Files
 - /etc/systemd/system/web_routes_front.service
 - /etc/systemd/system/web_routes.service
 - /etc/systemd/system/users.service
 - /etc/systemd/system/routes.service
 
 - /etc/nginx/conf.d/server_oneway.conf 
