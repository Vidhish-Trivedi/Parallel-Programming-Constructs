# Task Construct
The OpenMP `TASK` directive is used to explicitly create tasks that can be executed asynchronously by the OpenMP runtime. Tasks allow for finer-grained parallelism compared to parallel regions and can be particularly useful for irregular or dynamic workloads.

These may be executed by the encountering thread, or deferred for execution by any other thread in the team.
The data environment of the task is determined by the data sharing attribute clauses.
## Format
```c++
#pragma omp task [clause ...] 
                   if (scalar expression)_
                   final (scalar expression) 
                   untied
                   default (shared | none)
                   mergeable
                   private (list)
                   firstprivate (list) 
                   shared (list) 

structured_block
```
Usually, the `TASK` directive is enclosed within a `SINGLE` directive to ensure that a task is executed by a single thread.
## Example
```c++
#include <stdio.h>
#include <omp.h>
int fib(int n) {
    int i, j;
    if (n<2) {
        return n;
    }
    else {
        #pragma omp task shared(i) firstprivate(n)
        {
                printf("n-1: thread number: %d\n", omp_get_thread_num());
                i=fib(n-1);
        }

        #pragma omp task shared(j) firstprivate(n)
        {
                printf("n-2: thread number: %d\n", omp_get_thread_num());
                j=fib(n-2);
        }

        #pragma omp taskwait
        return i+j;  // Waits for the calls/tasks to fib(n-1) and fib(n-2) to finish
    }
}

int main() {
    int n = 4;

    omp_set_dynamic(0);
    omp_set_num_threads(4);

    #pragma omp parallel shared(n)
    {
        #pragma omp single
        printf("fib(%d) = %d\n", n, fib(n));
    }
}
```

Output:
```shell
n-1: thread number: 0
n-2: thread number: 0
n-1: thread number: 2
n-2: thread number: 3
n-2: thread number: 2
n-1: thread number: 2
n-1: thread number: 2
n-2: thread number: 3
fib(4) = 3
```
(Credit: Oracle Docs - OpenMP API User's Guide)

In the example, the **parallel** directive denotes a parallel region which will be executed by four threads. In the parallel construct, the **single** directive is used to indicate that only one of the threads will execute the **print** statement that calls fib(n).

The call to fib(n) generates two tasks, indicated by the **task** directive. One of the tasks computes fib(n-1) and the other computes fib(n-2), and the return values are added together to produce the value returned by fib(n). Each of the calls to fib(n-1) and fib(n-2) will in turn generate two tasks. Tasks will be recursively generated until the argument passed to fib() is less than 2.

The **taskwait** directive ensures that the two tasks generated in an invocation of fib() are completed (that is. the tasks compute i and j) before that invocation of fib() returns.

Note that although only one thread executes the **single** directive and hence the call to fib(n), all four threads will participate in executing the tasks generated.

## Aditional Notes
### taskwait
The taskwait directive is used to synchronize tasks in OpenMP.
When encountering a taskwait, the current thread waits until all tasks generated by the current task region are complete before proceeding.
It ensures that the execution of the code following the taskwait directive will not start until all tasks spawned before it have completed execution.
It's often used after a group of tasks where subsequent computation depends on the completion of those tasks.
### taskyield
The taskyield directive instructs the runtime system to yield the execution of the current task and allows other tasks to run.
When a thread encounters taskyield, it suspends execution of the current task and returns control to the OpenMP runtime system.
Other tasks may then be executed before the suspended task is resumed, potentially improving task scheduling and load balancing.
It's typically used to improve concurrency and reduce the likelihood of thread starvation or deadlock in scenarios with a large number of tasks.
