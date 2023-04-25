# Questions

## 1. How do you estimate the runtime behavior of your implementation in terms of CPU usage and memory consumption?

If the application is running in a container (docker), one possiblity is to use docker stats, where it shows the CPU and memory usage.

Other possible way is to use Prometheus. I developed once an integration between Prometheus and FastAPI application, where I could export some metrics under /metrics endpoint and consume it using Grafana to plot the charts.

This implementation in an example scope would be something like this:

from starlette_prometheus import metrics, PrometheusMiddleware

```
app = FastAPI() # Start the FastAPI application
app.add_middleware(PrometheusMiddleware) # Add the Prometheus middleware
app.add_route(“/metrics”, metrics) # Export the metrics under this route
```

The metrics endpoint would export some data as follow, but keep in mind that it is responsible to export startlette matric, if you want to access other metrics, there are other options available:

- https://github.com/trallnag/prometheus-fastapi-instrumentator
- https://github.com/stephenhillier/starlette_exporter

Note: The starlette metrics are: starlette_requests_total (total of requests by method and path), starlette_responses_total (histogram of requests processing time by path in seconds), starlette_requests_in_progress (gauge of requests by method and path currently being processed), and etc.

But the good part is that Prometheus provides some built-ins measures, for example:

- virtual_memory_bytes
- resident_memory_bytes

The integration between Prometheus and Grafana can be added inserting new data source and add the Prometheus and configuring it to consum the right por where your instance is running.

## 2. How do you approach designing and architecting large-scale Python applications, and what tools or techniques do you use to ensure scalability, maintainability, and performance?

* **Microservice**: A possibility is to split the aplications in small applications responsible only for a section of the code with an isolate database. It make easier to scale the application, since there is no need to scale the whole monolitich, but only the part where the clients are overloading.

* **Containerization**: Containerization can help the the scalability by enabling it to be deployed and scaled across multiple environments.

* **Load Balancer**: It is possible to use load balancer to distribute the incoming requests between the servers running, one possible tool that enables it and loadbalance the application which is running in the container is Traefik, however there are other solutions such as NGINX.

* **Caching**: Caching the response to reduce the timing of the retrieving data from DB.

* **Logging**: Use Prometheus for monitoring the application and making easier to identify the issue

* **Automated tests**: Automated tests helps a lot to identify the problem in the company stack, there it can point the exactly point where the issue is happening, if the applications are well covered by tests.


## 3. Can you describe your experience working with any Python web frameworks, such as Flask or Django, and how you have used third-party tools or libraries to enhance their functionality?

## 4. Can you discuss your experience with authentication and authorization in API design, and how you have implemented these features in Python?

## 5. What are the pros and cons of deploying applications as a container (e.g. Docker)?

## 6. Suppose you need to continuously roll out an application to several stations in multiple remote locations in different time zones and sometimes unstable/slow internet connections. Service continuity and stability are paramount. Each on-site location has a central server available. How would you make sure that you can roll out updated versions of the application in a timely fashion while interrupting the service as shortly as possible?

## 7. How do you optimize queries in a relational database, such as PostgreSQL or MySQL? Can you discuss techniques such as indexing, query planning, or query optimization?