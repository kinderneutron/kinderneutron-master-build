#!/bin/sh

# Turn off echoing commands
set +x

# Get the ID of the container named "psql-db"
container_id=$(docker ps -qf "name=psql-db")

if [ -n "$container_id" ]; then
  # Execute the psql command within the container
  docker exec psql-db psql -U postgres -f /docker-entrypoint-initdb.d/create-db.sql 2> /tmp/error.log
  
  if grep -q "already exists, skipping" /tmp/error.log; then
    echo "Error: Relations already exist in the database."
    exit 1
  else
    echo
    echo "Kinderneutron Database is Setup Successfully!"
    exit 0
fi
else
  echo "Error: No container named \"psql-db\" is found."
  exit 1
fi


