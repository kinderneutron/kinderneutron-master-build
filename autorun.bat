@echo off
echo Hello From Team,Kinderneutron .......
echo.                                     

echo Created By Team, Kinderneutron

echo.    

echo Setting Up Docker containers...
timeout /t 3 /nobreak > nul
REM Run docker-compose in detached mode without displaying output
echo Running Docker containers...
docker-compose up -d > nul

REM Display custom message in the Command Prompt


REM Wait for 5 seconds (adjust the number as needed)
echo Executing kinderneutron_image and psql Docker containers...
timeout /t 5 /nobreak > nul

REM Open a new Command Prompt window and run the first Docker image without displaying output
start cmd /k "docker exec -it kinderneutron_container sh" & title kinderneutron_image

REM Wait for 3 seconds (adjust the number as needed)


REM Open another new Command Prompt window and run the second Docker image without displaying output
start cmd /k "docker exec -it psql-db sh" & title psql-db
