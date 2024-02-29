#this file have all the steps necessary to create our own custom image

#This specifies the base image from Docker Hub to build upon
FROM python:3.10.13

#(optional)This sets the working directory inside the Docker container to /usr/src/app(stores all the application code)
#where all the command are going to run
WORKDIR /usr/src/app

# (./ or /usr/src/app) 
COPY requirements.txt ./ 

#The --no-cache-dir flag prevents caching of the package installation.
RUN pip install --no-cache-dir -r requirements.txt

#This copies all the files from the host into the current directory (/usr/src/app) in the Docker container
#(.. or . /usr/src/app)
COPY . .

#command to run the application get splitted into an array of elements
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

#when we build images from the docker file it actually treats each line as a layer of image 
#even if the code changes we does not change the base image and it tries each line of this file and will run accordingly
