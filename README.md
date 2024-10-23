luego de que los servicios se hayan levantado, ejecuta estos comandos dentro del contenedor DB con postgres.

psql -U postgres -d postgres -f tables.sql
psql -U postgres -d postgres -f import_data.sql
