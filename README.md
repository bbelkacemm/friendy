# Friendy: a chatbot for autistic children!

## Introduction

Friendy is a platform that provides an intelligent **chatbot** for autistic children to prevent them from **depression**. Solving this problem is a bit tricky because of the data it requires. The data must be collected and verified by professionals. So we have created a portal where they can contribute to the dataset making the chatbot more robust.

## Prerequisites

* Anaconda.
* NPM.
* Docker (Optional).

## Development

1. Create a conda environment using the file **environment.yml** using the following commands:

```shell
cd server
conda env create environment.yml
```

2. Prepare and launch database container using the following commands:

```shell
docker pull postgres
docker container run --name pfe -d -p 5432:5432 -e POSTGRES_PASSWORD=1234 postgres
```

3. Download nltk data:

```python
import nltk

# uncomment 'nltk.download()' located in server/model/train.py, 
# after downloading the data comment it again
nltk.download()
```

4. Launch the server using the following command:

```shell
# if you are on macos replace set with export
# use python.exe located on your environment's bin
set FLASK_DEBUG=0 && set FLASK_APP=server/app.py && python -m flask run
```

5. Launch the client (web) using the following commands:

```shell
cd client
npm run serve
```

6. Train the model from the dashboard page.

## Notes

- Change the date style 
```sql
ALTER DATABASE postgres SET datestyle TO "ISO, DMY";
```
