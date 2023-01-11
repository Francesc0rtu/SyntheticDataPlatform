# Synthetic Data Platform

[![Docker Image Size](https://badgen.net/docker/size/francescortu/sdp?icon=docker&label=image%20size)](https://hub.docker.com/r/francescortu/sdp)
![License MIT](https://img.shields.io/github/license/Francesc0rtu/SyntheticDataPlatform)
## Usage
To run the application you need a MongoDB ATLAS database. You can create a free cluster [here](https://www.mongodb.com/cloud/atlas). Then, you need to create a `config/.env` file in the root directory of the project. The file should contain the following variables:
```bash
MONGO_URI=<your-mongo-uri>
```
The database is structurated as follow:
```
collection ---> SDP
                |
                |--> User(Username, Email, Password)
                |--> InputDataset <--- GridFS with (filename, username)
                |--> OutputDataset <--- GridFS with (filename, username, base_dataset)
```
### Docker
Build the image
```bash
$ docker build -t sdp .
```
Run the container
```bash
$ docker run  --env-file config/.env sdp
```


### Clone the repo
The application require `Python 3.9.15`.
Fristly, clone the repo
```bash
$ git clone https://github.com/Francesc0rtu/SyntheticDataPlatform
```
Then install the requirements
```bash
$ pip install -r requirements.txt
```
Finally, run the application
```bash
$ python main.py
```



[contributors-shield]: https://img.shields.io/github/contributors/Francesc0rtu/SyntheticDataPlatform.svg?style=for-the-badge

[contributors-url]: https://github.com/Francesc0rtu/SyntheticDataPlatform/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/Francesc0rtu/SyntheticDataPlatform.svg?style=for-the-badge

[forks-url]: https://github.com/Francesc0rtu/SyntheticDataPlatform/network/members

[stars-shield]: https://img.shields.io/github/stars/Francesc0rtu/SyntheticDataPlatform.svg?style=for-the-badge

[stars-url]: https://github.com/Francesc0rtu/SyntheticDataPlatform/stargazers

[issues-shield]: https://img.shields.io/github/issues/Francesc0rtu/SyntheticDataPlatform.svg?style=for-the-badge

[issues-url]: https://github.com/Francesc0rtu/SyntheticDataPlatform/issues

[license-shield]: https://img.shields.io/github/license/Francesc0rtu/SyntheticDataPlatform.svg?style=for-the-badge

[license-url]: https://github.com/Francesc0rtu/SyntheticDataPlatform/blob/main/LICENSE


