# FStartBench
FStartBench is a benchmark suite with serverless workload.

Our project uses five commonly used application programs on a serverless computing platform as benchmark test programs to represent typical cloud server workloads. Deploying these 13 functions on a serverless platform allows for testing of their cold start time, execution time, memory usage, and other related information. This benchmark can help researchers improve their applications or optimize platform performance.

## Test Cases
### 1. Hello App
Functions 1-4 are respectively written in Java, Node.js, Go, and Python and serve as Hello programs to test the difference in startup time of different programming languages on a serverless platform.

### 2. Data Analyze
Functions 6-8 are three functions related to data analysis. Their images consist of the same operating system (Debian) and programming language (Python). In order to test the impact of adding dependency packages on startup time, the dependencies of these three functions in the runtime layer are incrementally increased (adding Numpy, Pandas, and Matplotlib on top of Flask).

### 3. Data Transfer
Function 9 is a C++ function used to test the communication overhead between serverless functions and other cloud services.

### 4. CPU-intensive
Function 10 is an ALU application used to test the resource requirements of serverless functions. It implements ten million arithmetic operations.

### 5. Real World App
To cover various real-world serverless workloads in popular cloud scenarios, three applications were provided: a web application (Function 11), an image processing application (Function 12), and a machine learning application (Function 13).
