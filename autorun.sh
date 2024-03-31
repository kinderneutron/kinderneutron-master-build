#!/bin/bash

# Run docker-compose in detached mode
docker-compose up -d

# Open a new tab and run the first Docker image
gnome-terminal --tab --title="kinderneutron_image" -- bash -c "docker exec -it kinderneutron_container sh"

# Open another new tab and run the second Docker image
gnome-terminal --tab --title="Postgres DB" -- bash -c "docker exec -it psql-db sh"
