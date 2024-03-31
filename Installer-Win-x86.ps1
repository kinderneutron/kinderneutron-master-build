# Run docker-compose in detached mode
docker-compose up -d

# Open a new PowerShell tab and run the first Docker image
Start-Process powershell -NoNewWindow -ArgumentList "docker exec -it kinderneutron_container sh"

# Open another new PowerShell tab and run the second Docker image
Start-Process powershell -NoNewWindow -ArgumentList "docker exec -it psql-db sh"
