# Concurrency and Parallelism Implementations in Common Languages 

*Disclaimer*: This is a work in progress, and represents what I've learned so far. I'm sure I'm wrong about some of this. PRs or Comments welcome (and encouraged!!).


Different languages handle concurrency and parallelism very differently. Although there are usually higher or lower level abstractions, or commonly used external dependencies, to mitigate a langague's weak points, some languages lend themselves more to certain types of operations.

Below, references to parallelism denote doing things at the exact same time (like breathing while running), while concurrency refers to rapidly switching between small chunks of work before the larger task is complete, but never truly doing more than one task at a time (like taking a step, then exhaling while not moving, and then taking another step while holding your breath). In the context of computers, true parallelism is when multiple processors or CPU cores are doing work at the same time, whereas concurrency takes place in one CPU core where programs may appear to do multiple things at once, but the in reality they're switching between tasks so rapidly it appears as though things are happening in parallel.

Rob Pike, the creator of Golang explains this concept wonderfully : https://www.youtube.com/watch?v=cN_DpYBzKso


It may also be worth understanding that an OS process is isolated from other processes and contains everything a program needs to run (including it's own memory). An OS thread, meanwhile, is meant to run within a process, and all threads share the memory of the process they are in. OS threads can utilize multiple CPU cores.

Native threads are what programming languages use to refer to OS threads. Green Threads are usually language specific higher level abstractions on top of OS threads.



## Ruby, Python

Python and Ruby are languages built on C and have a Global Interpreter Lock (GIL) that ensures no two operations are occuring simultaneously. When threads are created in these languages, the GIL ensures that no two threads are actually running in parallel, instead allowing them to rapidly switch between each other.

Part of the motivation for the GIL may be due to side effects of a Python program depending on C-level libraries without any knowledge of their internals. Jython and JRuby, Python and Ruby implementations built on top of Java instead of C, use OS threads that allow parallelism, but as a result break compatability with C extensions, and not all libraries are built with thread safety in mind (since the GIL ensures it in the implementations built on C).

Langauges like these perform work sequentially by default, and doing things in asynchronously or in parallel is done by leveraring included libraries that distribute work across system processes. In Python the `multiprocessing` library will fork a new OS process, which can utilize multiple system cores. However, system processes are very heavy weight (can have hundreds of MB of overhead) and each CPU core can only do work for once process at a time. Typically, the a number of processes forked closely matches the number of CPU cores. The equivalent mechanism in Ruby is just to call `fork` and pass a block of work.

Python and Ruby also have Threading libraries (`Thread` in Ruby and `Threading` in Python) that do work concurrently, but respect the GIL. 

Ruby 1.9 moved away from green threads towards OS threads, however the GIL doesn't take advantage of parallelism of the system. Ruby 3.0 has a proposal out for the concept of `guilds`, which would separate code into separate guilds, each of which have a GIL that blocks with respect to its internals, but can run in parallel with other guilds. This would keep backwards compatability will existing code (since it would just be considered to exist in one guild).


## Erlang, Elixir

Note that while theyr'e very different, I use the terms Elixir and Erlang somewhat interchangably. Elixir is a light wrapper on top of Erlang, a language created by Ericsson for their massively parallel telephone systems. Elixir can natively call Erlang modules and use its tools.

In Erlang, each function usually runs in a separate process (a higher level Erlang language implementation of processes, not an OS process). This is done by using `spawn` or Elixir's `Task` module. Each process has its own memory heap and is completely isolated from the rest of the program. The functional and immutable nature of Erlang lends itself well to this type of design.

Processes are extremely lightweight and hundreds of thousands can run on a single machine. Erlang processes are inherintly parallel, performing operations at the same time across multiple CPU cores. There are constructs in the langauge for controlling whether operations are done eagerly, lazily, or with a maximum concurrency limit.

Communication is done by passing messages between processes (a function `call` is somewhat literal in this language). This makes Erlang programs easy to distribute across different physical servers (as the mechanism for distributing and send to/receiving from these isolated processes is the same). 

It also allows for code to be how swappable (new processes will load the new code, and there is a mechansim for translating existing processes to the code).


See : http://elixir-lang.org/getting-started/processes.html


## PHP

PHP leverages OS processes in order to run. Each OS system process has a virtual address space that is completely isolated from other processes.

This is similar to Erlang, expect Erlang uses a higher level abstraction for processes that is much lighter on system resources. Maximum parallelism for PHP will be defined by the OS (`ulimit` is configurable settings for how many processes can run simultaneously on linux).

PHP is commonly used in a LAMP stack that relies on a database on the back end in order transfer information between processes (since after a process dies, the contents of its memory no longer persist).



## Golang

Golang has also reimplimented lightweight processes on top of OS processes (for which hundreds of thousands can be spawned) and is not bound by a GIL. Golang differs from Erlang, however, in its shared memory.

Golang functions can be made asynchronous by prepending the function call with the term `go`. Though concurrency can be handled several ways, it often uses a WaitGroup mechanism that increments and decrements a counter of running processes, and unblocks when all have completed (similar to the `join` syntax in Python or Ruby).

Golang has a concept called `channels`, which are a mechansim through which different processes can send and receive from each other.

In Golang all memory is stored in the same heap, so garbage collection must be performed periodically, which can be a costly operation. Golang 1.8, however, improves the performance of the garbage collector dramatically.



## Node JS

In JavaScript, code is run asynchronously by default. On the browser this was a useful mechanism to have many "listeners" for actions like users pressing a certain key, while still being able to perform other tasks while waiting.

By default, JavaScript is core bound, operating an event loop within a process. Not being truly parallel makes implementation of the language, as well as debugging, much easier (locking mechanisms are a frequent source of errors). When run on servers, however, making use of multiple cores is necessary, so it common to have Node with one main thread managing the sequence of events and several forked processes that will do more intensive actions.

JavaScript employs mechanisms like `callbacks` and `promises` to handle control flow since the syntax is not completely sequential (for the circumstances in which one does which to wait for an action to complete before starting another. Like waiting for an HTTP response from a server before attempting to parse the body).


### Java

TODO
