#!/bin/bash

# Run docker-compose in detached mode
docker-compose up -d
gnome-terminal --tab --title="Kinderneutron_API_Server" -- bash -c "docker exec -it kinderneutronapicontainer bash"

# Open a new tab and run the first Docker image
gnome-terminal --tab --title="Kinderneutron_Webapp" -- bash -c "docker exec -it kinderneutroncontainer bash"

# Open another new tab and run the second Docker image
gnome-terminal --tab --title="Postgres DB" -- bash -c "docker exec -it psql-db sh"

