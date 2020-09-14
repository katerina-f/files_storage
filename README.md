# files_storage

### How to run
To install and run the code in the docker containers, make script

> >run.sh

executable

> chmod +x ./run.sh

This script will start building the application and run it in the project root

> ./run.sh

### Usage

#### POST (upload)

```
curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@/path/to/file/some_file.jpg" localhost:5000/file_manager
```

Returns name (hash view) of created file and 201 code if success

```
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 35
Server: Werkzeug/1.0.1 Python/3.7.4
Date: Mon, 14 Sep 2020 09:43:26 GMT

"609cdd2445c2b6bbf6517ab7398548b4"
```

Returns error message and 403 code if filename not allowed

```
HTTP/1.0 403 FORBIDDEN
Content-Type: application/json
Content-Length: 24
Server: Werkzeug/1.0.1 Python/3.7.4
Date: Mon, 14 Sep 2020 09:48:48 GMT

"Not allowed filename!"
```

Returns error message and 400 code if bad request

```
HTTP/1.0 400 BAD REQUEST
Content-Type: application/json
Content-Length: 17
Server: Werkzeug/1.0.1 Python/3.7.4
Date: Mon, 14 Sep 2020 09:52:12 GMT

"File is needed"
```

#### GET (download)

Be careful to save bad response to the file and check file exists before saving
```
curl -i  -X GET http://localhost:5000/file_manager/6b4ca457f7241c0ba2f2454b761bba34
```

If exists returns message and 200 code

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 14
Server: Werkzeug/1.0.1 Python/3.7.4
Date: Mon, 14 Sep 2020 10:42:33 GMT

"File exists"
```

if not returns error message and 404 code

```
HTTP/1.0 404 NOT FOUND
Content-Type: application/json
Content-Length: 21
Server: Werkzeug/1.0.1 Python/3.7.4
Date: Mon, 14 Sep 2020 10:45:24 GMT

"File was not found"
```

And then you can download file

```
curl http://localhost:5000/file_manager/6b4ca457f7241c0ba2f2454b761bba34/download --output "some_file.jpg"
```

`6b4ca457f7241c0ba2f2454b761bba34` -  hash name of file you are looking for
`download` - command to save
`some_file.jpg` - path to file that you want to save

Returns downloading log and 200 code if success
```
 % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                Dload  Upload   Total   Spent    Left  Speed
100  235k  100  235k    0     0  13.5M      0 --:--:-- --:--:-- --:--:-- 13.5M
```

#### DELETE

```
curl -i -X DELETE http://localhost:5000/file_manager/6b4ca457f7241c0ba2f2454b761bba34
```

Returns error message and 404 code if file was not found

```
HTTP/1.0 404 NOT FOUND
Content-Type: application/json
Content-Length: 21
Server: Werkzeug/1.0.1 Python/3.7.4
Date: Mon, 14 Sep 2020 10:49:15 GMT

"File was not found"
```

Return 204 code if success

```
HTTP/1.0 204 NO CONTENT
Content-Type: application/json
Content-Length: 32
Server: Werkzeug/1.0.1 Python/3.7.4
Date: Mon, 14 Sep 2020 10:52:12 GMT
```
