# Python 3.6.7
FROM python:3.7.1-slim
# Packages that we need 
COPY requirements.txt /app/
WORKDIR /app


RUN pip   install -r requirements.txt
# Copy all the files from current source duirectory(from your system) to
# Docker container in /app directory 
COPY . /app

# Specifies a command that will always be executed when the  
# container starts.
# In this case we want to start the python interpreter
ENTRYPOINT ["python"]
# We want to start app.py file. (change it with your file name) 
# Argument to python command
CMD ["main.py"]