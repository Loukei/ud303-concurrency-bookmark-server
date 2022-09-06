# ud303-concurrency-bookmark-server

## What's the problem?

The bookmark server can't handle over 1 request. 

If user try to use bookmark server URI (ex: "https://ud303-loukei-bookmarksever.herokuapp.com/") as bookmark, server will try to make requests for himself.

![Demo](IMG/chrome_1IzclsC6jS.png)

``` python
def __check_longuri(self, longuri:str)->bool:
    "Check longuri, if uri exist, return true"
    try:
        res:requests.Response = requests.get(url=longuri)
        return res.status_code == 200
    except requests.RequestException:
        return False
    except:
        return False
```

Since our server can't handle over 1 request, the server will crash instantly.

## How to fix it?

#TODO
1. how to use thread to solve concurrency problem?
2. What is `ThreadingMixIn`? How does it work with `http.server.HTTPServer`?

``` python
import threading
from socketserver import ThreadingMixIn

class ThreadHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    "This is an HTTPServer that supports thread-based concurrency."
```

Use `ThreadHTTPServer` instead of `HTTPServer` 

``` python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    server_address = ('', port)
    httpd = ThreadHTTPServer(server_address, Shortener)
    httpd.serve_forever()
```

## The OS concepts

### The program

Program means a couple of files stored in computer disc. For example, if you installed Internet Explorer, but not using it now, then it's a program, an inactive data in disc.

### The process

The process is opposed to the program, which means the OS is running the program and distributing resources like memory and CPU for it, not data stored in the disc.

### The thread

The thread is a small unit that OS can schedule, each process can have more than one thread, every thread in same process share the resource of the process.

For example, in modern browser, each page use different thread, but they share the resource which OS distribute to our browser.

Another example is the process is like a news paper, the thread    is like a person who's reading it, when you reading the economic article, your wife can read the sports article. Each person use the different part of resource, but when they want to access the same article, it will cause **race condition**.

### Concurrency

Concurrency means we split our job into several different task, they share the same resource at a time. When CPU running a concurrency task, it picks one task, running it, then switch to another task, so it looks like those task are running parallel but not.

### Why we need concurrency in this case?

#TODO

## Reference

- [ud303 - HTTP in the Real World](https://learn.udacity.com/courses/ud303/lessons/f5e2f7c1-d0ce-4738-b985-1f70fb61817d/concepts/461f4efb-c3c9-463d-9057-37e63ac879e8)
- [socketserver --- 用于网络服务器的框架 — Python 3.10.6 說明文件](https://docs.python.org/zh-tw/3/library/socketserver.html)
- [Difference Between Process and Thread - Georgia Tech - Advanced Operating Systems - YouTube](https://www.youtube.com/watch?v=O3EyzlZxx3g)
- [程序(進程)、執行緒(線程)、協程，傻傻分得清楚！. 要成為一個優秀的軟體工程師，進程（process）、線程（thread）是一定要… | by 莫力全 Kyle Mo | Medium](https://oldmo860617.medium.com/%E9%80%B2%E7%A8%8B-%E7%B7%9A%E7%A8%8B-%E5%8D%94%E7%A8%8B-%E5%82%BB%E5%82%BB%E5%88%86%E5%BE%97%E6%B8%85%E6%A5%9A-a09b95bd68dd)
- [How web browsers use process & Threads | by Thiluxan | Medium](https://thiluxan.medium.com/how-web-browsers-use-process-threads-a5e560d42037)
- [翻译｜揭示现代浏览器原理(1) — Chrome官方 - 知乎](https://zhuanlan.zhihu.com/p/111560897)
- [multithreading - What is a race condition? - Stack Overflow](https://stackoverflow.com/questions/34510/what-is-a-race-condition)