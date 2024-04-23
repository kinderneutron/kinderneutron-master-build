@ECHO OFF


docker ps --filter name=psql-db --format "{{.ID}}" > container_id.txt

IF EXIST container_id.txt (
  SET /P container_id=<container_id.txt
  DEL container_id.txt

  rem Execute the psql command within the container
  docker exec psql-db psql -U postgres -f /docker-entrypoint-initdb.d/create-db.sql
  ECHO .
  ECHO .
  ECHO Kinderneutron Database is Setup Sucessfully!
) ELSE (
  ECHO Error: No container named "psql-db" is found.
  EXIT /B 1
)



EXIT /B 0
