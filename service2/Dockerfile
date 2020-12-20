FROM ubuntu:latest
# install sqlite3
RUN apt update
RUN apt install -y sqlite3 libsqlite3-dev 

# install python3-pip			
RUN apt install python3-pip -y


COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt						
EXPOSE 3001
ENTRYPOINT ["python3"]
CMD [ "app.py"]
