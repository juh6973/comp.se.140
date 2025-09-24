# Exercise 1
Report for "Basics of containers and microservices" exercise.

## 1. Basic Information
I used my personal laptop as the development and run environment for the application. Here are the specifications:
- HW: Apple M2 Pro, RAM 16 GB
- OS: macOS Sequioa v15.7
- Docker: v24.0.7
- Docker Compose: v2.23.3-desktop.2

## 2. Application Architecture
TODO

## 3. Content Analysis
The services measure the disk space and uptime from within a docker container. The disk space is obtained from the container's root filesystem. This is not the same as host machine's disk space as docker utilizes overlay storage drives that limits the view into the disk space. Uptime is based on a measures of time since the container started. These measurements are relevant for monitoring the container runtime but doesn't assess host-level uptime. To reflect the total disk space of the host, the container should be mounted to the host's filesystem and highlight that the uptime refers to container lifecycle.

## 4. Comparison of Persistent Storage Solutions
There were two persistent storage solutions: A named volume and a bind mounted log file. The bind mounted file is easy to read by the host, but violates the container isolation principle. The file doesn't exists as part of the docker build and has to be added manually. Also, the file write permissions can cause problems in some cases. This setup is okay for debugging purposes but should not be taken into production. The named volume approach is more inline with docker design patterns. The volume is portable via docker and doesn't require any extra actions from the user. However, accessing the volume manually is more tricky as the file isn't readable outside the docker network. All-in-all, the latter approach is still better as it provides a self-contained and portable storage solution that avoids host dependecies.

## 5. Teacher's Instructions
***How to run the application:**
- `docker-compose up –-build -d`
To inspect the status:
- `curl localhost:8199/status`
To inspect the logs:
- `curl localhost:8199/log`

***How to shut down the application:**
- `docker-compose down`

**To remove the persistent storage**
- `curl -X DELETE localhost:8199/log`

**To read the vstorage**
- `cat ./vstorage/log.txt`

## 6. Reflections
The main challenge in this exercise was understanding what was actually expected and gathering all the necessary requirements. In other words, the instructions weren’t entirely clear. From a technical perspective, the most difficult part was grasping the purpose of vstorage and implementing it correctly (initially, I implemented it as just another Docker volume). That said, I think the exercise was a good introduction to the course and the kinds of tasks we’ll be tackling later on.