# ddapp

Execute these after running the .sql file for setting up the database:
```
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO devuser;
GRANT ALL PRIVILEGES ON ALL sequences IN SCHEMA public TO devuser;
```