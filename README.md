# FStartBench
FStartBench is a benchmark suite with serverless workload.

Our project uses eight commonly used application programs on a serverless computing platform as benchmark test programs to represent typical cloud server workloads. Deploying these 72 functions on a serverless platform allows for testing of their cold start time, execution time, memory usage, and other related information. This benchmark can help researchers improve their applications or optimize platform performance.

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

### 6. Libraries-Numpy 
Libraries-Numpy contains 20 functions from Numpy libraries based on Python, aimed at facilitating mathematical operations on images. All functions are built on the same operating system and Python language, utilizing the same versions of dependencies. 

### 7. Libraries-Torch
Libraries-Torch comprises 20 functions from Torch libraries, which provide functionalities related to machine learning on images. Similar to Libraries-Numpy, these functions are also developed using a consistent operating system and Python language, as well as the same versions of dependencies. Notably, Libraries-Numpy is built on Alpine, while Libraries-Torch is based on Debian.
The details are provided in the table below.

|Libraries-Numpy | Libraries-Torch|
|------------------|----------|
| arccos           | cifar    | 
| ceil             | eye      | 
| cos              | folder   | 
| det              | fromnp   |  
| exp              | linspace |
| fabs             | minst    |
| floor            | randn    |
| intersect        | randperm |
| inv              | alex     |
| load             | center   | 
| log              | dense121 |
| max              | dense169 |
| min              | flip     |
| save             | pad      |  
| shuffle          | res18    | 
| solve            | res50    |
| sort             | res152   |
| sqrt             | save     |
| square           | squeeze1 |
| svd              | vgg13    |

### 8. Applications
Applications includes a total of 20 applications in three different programming languages. Among them, Java has 5 applications designed for processing input .csv data, while Node.js and Python have 6 and 8 applications, respectively, each covering different content. 

The details are provided in the table below.

| Application Name        | Language | Description                                                        |
|-------------------------|----------|--------------------------------------------------------------------|
|java_data_group          | Java     | Processes .csv data                                                |
|java_data_load           | Java     | Processes .csv data                                                |
|java_data_query          | Java     | Processes .csv data                                                |
|java_data_scan           | Java     | Processes .csv data                                                |
|java_data_upload         | Java     | Processes .csv data                                                |
|nodejs_auto_complete     | Node.js  | Processes file                                                     |
|nodejs_dynamic_html      | Node.js  | Processes file                                                     |
|nodejs_image_sizing      | Node.js  | Sizes input image(.png)                                            |
|nodejs_ocr_image         | Node.js  | Using LSTM to recognize characters in images into base64 code      |
|nodejs_thumbnailer       | Node.js  | Downloads images(.png)                                             |
|nodejs_uploader          | Node.js  | Uploads images(.png)                                               |
|python_dna_visualization | Python   | Visualizes the input DNA code                                      |
|python_file_compression  | Python   | Compresses fileholder into a .zip file                             |
|python_file_pagerank     | Python   | Generates a graph using pagerank function                          |
|python_graph_bfs         | Python   | Performs bfs algorithm                                             |
|python_graph_markdown    | Python   | Transforms base64-string into a markdown file                      |
|python_graph_mst         | Python   | Performs mst algorithm                                             |
|python_image_recognition | Python   | Using Res50 to recognize images                                    |
|python_sentiment_analysis| Python   | Using TextBlob to recognize emotions in files                      |
