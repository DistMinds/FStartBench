## 开发准备

### 相关资源
依赖静态库: jsoncpp boost_system boost_thread Poco (在lib文件夹下)
依赖动态库: ssl crypto rt z (需要安装)

1. 安装boost的库和头文件 [http://www.boost.org/](http://www.boost.org/)
2. 安装cmake工具 [http://www.cmake.org/download/](http://www.cmake.org/download/)
3. 安装openssl的库和头文件 http://www.openssl.org/source/
4. 安装Poco的库和头文件 [https://pocoproject.org/download/index.html](https://pocoproject.org/download/index.html)
5. 从控制台获取APP ID、SecretID、SecretKey。

sdk中提供了Poco、jsoncpp的库以及头文件，以上库编译好后替换掉sdk中相应的库和头文件即可，如果以上库已经安装到系统里，也可删除sdk中相应的库和头文件。
可以修改CMakeList.txt文件中，指定本地boost头文件路径，修改如下语句： SET(BOOST_HEADER_DIR "/root/boost_1_61_0")

### SDK 配置

直接下载github上提供的源代码，集成到您的开发环境。

执行下面的命令 ：
``` bash
cd ${cos-cpp-sdk}
mkdir -p build
cd build
cmake ..
make
```

cos_demo.cpp里面有常见API的例子。生成的cos_demo可以直接运行，生成的静态库名称为：libcossdk.a。生成的 libcossdk.a 放到你自己的工程里lib路径下，include 目录拷贝到自己的工程的include路径下。

## 初始化操作
### 初始化
接口说明：在使用COS操作之前，需要首先进行COS系统参数的设置，然后分别创建CosConfig以及CosAPI对象，COS的操作都是基于CosAPI对象进行的。

### 配置文件
```
"SecretId":"*********************************", // V5.4.3之前的版本请使用AccessKey替换SecretId
"SecretKey":"********************************",
"Region":"cn-north",                // COS区域, 一定要保证正确
"SignExpiredTime":360,              // 签名超时时间, 单位s
"ConnectTimeoutInms":6000,          // connect超时时间, 单位ms
"ReceiveTimeoutInms":60000,         // recv超时时间, 单位ms
"UploadPartSize":10485760,          // 上传文件分片大小，1M~5G, 默认为10M
"UploadCopyPartSize":20971520,      // 上传复制文件分片大小，5M~5G, 默认为20M
"UploadThreadPoolSize":5,           // 单文件分块上传线程池大小
"DownloadSliceSize":4194304,        // 下载文件分片大小
"DownloadThreadPoolSize":5,         // 单文件下载线程池大小
"AsynThreadPoolSize":2,             // 异步上传下载线程池大小
"LogoutType":1,                     // 日志输出类型,0:不输出,1:输出到屏幕,2输出到syslog
"LogLevel":3                        // 日志级别:1: ERR, 2: WARN, 3:INFO, 4:DBG
"IsCheckMd5":false                  // 下载文件时是否校验MD5, 默认不校验
```

### COS API对象构造原型

```
CosConfig(const string& config_file); // config_file是配置文件所在路径
CosAPI(CosConfig& config);
```

如果使用临时密钥，可以调用`CosConfig::SetTmpToken()`来设置临时密钥：
``` cpp
CosConfig config("path/to/config"); // config_file是配置文件所在路径
config.SetTmpToken("input_tmp_token");
```

## 生成签名

### Sign
#### 功能说明
 生成签名

#### 方法原型1
```
static std::string Sign(const std::string& secret_id,
                        const std::string& secret_key,
                        const std::string& http_method,
                        const std::string& in_uri,
                        const std::map<std::string, std::string>& headers,
                        const std::map<std::string, std::string>& params);
```

#### 参数说明

- secret_id   —— String             开发者拥有的项目身份识别 ID，用以身份认证
- secret_key  —— String             开发者拥有的项目身份密钥
- http_method —— String             http方法,如POST/GET/HEAD/PUT等, 传入大小写不敏感
- in_uri      —— String             http uri
- headers     —— map<string,string> http header的键值对
- params      —— map<string,string> http params的键值对

#### 返回结果说明

- 返回签名，可以在指定的有效期内(通过CosSysConfig设置, 默认60s)使用, 返回空串表示签名失败

#### 方法原型2
``` cpp
static std::string Sign(const std::string& secret_id,
                        const std::string& secret_key,
                        const std::string& http_method,
                        const std::string& in_uri,
                        const std::map<std::string, std::string>& headers,
                        const std::map<std::string, std::string>& params,
                        uint64_t start_time_in_s,
                        uint64_t end_time_in_s);
```
#### 参数说明

- secret_id   —— String             开发者拥有的项目身份识别 ID，用以身份认证
- secret_key  —— String             开发者拥有的项目身份密钥
- http_method —— String             http方法,如POST/GET/HEAD/PUT等, 传入大小写不敏感
- in_uri      —— String             http uri
- headers     —— map<string,string> http header的键值对
- params      —— map<string,string> http params的键值对
- start_time_in_s —— uint64_t       签名生效的开始时间
- end_time_in_s —— uint64_t         签名生效的截止时间

#### 返回结果说明
- String, 返回签名，可以在指定的有效期内使用, 返回空串表示签名失败


## Service/Bucket/Object 操作
所有与Service/Bucket/Object相关的方法原型，均是如下形式`CosResult Operator(BaseReq, BaseResp)`。

### CosResult
 封装了请求出错时返回的错误码和对应错误信息，详见[官网链接](https://www.qcloud.com/document/product/436/773 "错误码")。
**sdk内部封装的请求均会返回CosResult对象，每次调用完成后，均要使用IsSucc()成员函数判断本次调用是否成功。**

#### 成员函数：
`bool isSucc()`, 返回本次调用成功或失败，当返回false时， 后续的CosResult成员函数才有意义。当返回True时，可以从OperatorResp中获取具体返回内容。

`string GetErrorCode()`， 获取cos返回的错误码，用来确定错误场景。

`string GetErrorMsg()`， 包含具体的错误信息。

`string GetResourceAddr()`， 资源地址：Bucket地址或者Object地址。

`string GetXCosRequestId()`， 当请求发送时，服务端将会自动为请求生成一个唯一的 ID。使用遇到问题时，request-id能更快地协助 COS 定位问题。

`string GetXCosTraceId()`， 当请求出错时，服务端将会自动为这个错误生成一个唯一的 ID。使用遇到问题时，trace-id能更快地协助 COS 定位问题。当请求出错时，trace-id与request-id一一对应。

`string GetErrorInfo()`, 获取sdk内部错误信息。

`int GetHttpStatus()`， 获取http状态码。

#### BaseReq/BaseResp
BaseReq、BaseResp 封装了请求和返回， 调用者只需要根据不同的操作类型生成不同的OperatorReq（比如后文介绍的GetBucketReq), 并填充OperatorReq的内容即可。
函数返回后，调用对应BaseResp的成员函数获取请求结果。

对于Request，如无特殊说明，仅需要关注request的构造函数。
对于Response，所有方法的response均有获取公共返回头部的成员函数。
Response的公共成员函数如下， 具体字段含义见[公共返回头部](https://www.qcloud.com/document/product/436/7729 "公共返回头部")， 此处不再赘述：
```
uint64_t GetContentLength();
std::string GetContentType();
std::string GetEtag();
std::string GetConnection();
std::string GetDate();
std::string GetServer();
std::string GetXCosRequestId();
std::string GetXCosTraceId();
```


## Bucket操作

###  Get Bucket

#### 功能说明

Get Bucket请求等同于List Object请求，可以列出该Bucekt下部分或者所有Object，发起该请求需要拥有Read权限。详见:https://www.qcloud.com/document/product/436/773

#### 方法原型

``` cpp
CosResult GetBucket(const GetBucketReq& req, GetBucketResp* resp);
```

#### 参数说明

- req   —— GetBucketReq GetBucket操作的请求

``` cpp
/// 设置前缀，用来规定返回的文件前缀地址
void SetPrefix(const std::string& prefix);

/// 设置定界符，如果有 Prefix，则将 Prefix 到 delimiter 之间的相同路径归为一类，
/// 定义为 Common Prefix，然后列出所有 Common Prefix。如果没有 Prefix，则从路径起点开始
void SetDelimiter(const std::string& delimiter);

/// 规定返回值的编码方式，可选值：url
void SetEncodingType(const std::string& encoding_type);

/// 默认以 UTF-8 二进制顺序列出条目，所有列出条目从marker开始
void SetMarker(const std::string& marker);

/// 单次返回最大的条目数量，默认1000
void SetMaxKeys(uint64_t max_keys);
```

- resp   —— GetBucketResp GetBucket操作的返回

GetBucketResp提供以下成员函数，用于获取GetBucket返回的xml格式中的具体内容。
``` cpp
std::vector<Content> GetContents();
std::string GetName();
std::string GetPrefix();
std::string GetMarker();
uint64_t GetMaxKeys();
bool IsTruncated();
std::vector<std::string> GetCommonPrefixes();
```

其中Content的定义如下：
```
struct Content {
    std::string m_key; // Object 的 Key
    std::string m_last_modified; // Object 最后被修改时间
    std::string m_etag; // 文件的 MD-5 算法校验值
    std::string m_size; // 文件大小，单位是 Byte
    std::vector<std::string> m_owner_ids; // Bucket 持有者信息
    std::string m_storage_class; // Object 的存储级别，枚举值：STANDARD，STANDARD_IA
}
```
#### 示例

```cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";

// GetBucketReq的构造函数需要传入bucket_name
qcloud_cos::GetBucketReq req(bucket_name);
qcloud_cos::GetBucketResp resp;
qcloud_cos::CosResult result = cos.GetBucket(req, &resp);

// 调用成功，调用resp的成员函数获取返回内容
if (result.IsSucc()) {
    std::cout << "Name=" << resp.GetName() << std::endl;
    std::cout << "Prefix=" << resp.GetPrefix() << std::endl;
    std::cout << "Marker=" << resp.GetMarker() << std::endl;
    std::cout << "MaxKeys=" << resp.GetMaxKeys() << std::endl;
} else {
    std::cout << "ErrorInfo=" << result.GetErrorInfo() << std::endl;
    std::cout << "HttpStatus=" << result.GetHttpStatus() << std::endl;
    std::cout << "ErrorCode=" << result.GetErrorCode() << std::endl;
    std::cout << "ErrorMsg=" << result.GetErrorMsg() << std::endl;
    std::cout << "ResourceAddr=" << result.GetResourceAddr() << std::endl;
    std::cout << "XCosRequestId=" << result.GetXCosRequestId() << std::endl;
    std::cout << "XCosTraceId=" << result.GetXCosTraceId() << std::endl;
}
```

###  Put Bucket

#### 功能说明

Put Bucket 接口请求可以在指定账号下创建一个 Bucket。该 API 接口不支持匿名请求，您需要使用帯 Authorization 签名认证的请求才能创建新的 Bucket 。创建 Bucket 的用户默认成为 Bucket 的持有者。详见:https://cloud.tencent.com/document/product/436/7738

#### 方法原型

```cpp
CosResult PutBucket(const PutBucketReq& req, PutBucketResp* resp);
```

#### 参数说明

- req   —— PutBucketReq PutBucket操作的请求

PutBucketReq提供以下成员函数，
``` cpp
/// 定义Bucket的ACL属性,有效值：private,public-read-write,public-read
/// 默认值：private
void SetXCosAcl(const std::string& str);

/// 赋予被授权者读的权限.格式：x-cos-grant-read: id=" ",id=" ".
/// 当需要给子账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>"
/// 当需要给根账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>"
void SetXCosGrantRead(const std::string& str);

/// 赋予被授权者写的权限,格式：x-cos-grant-write: id=" ",id=" "./
/// 当需要给子账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>",
/// 当需要给根账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>"
void SetXCosGrantWrite(const std::string& str);

/// 赋予被授权者读写权限.格式：x-cos-grant-full-control: id=" ",id=" ".
/// 当需要给子账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>",
/// 当需要给根账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>"
void SetXCosGrantFullControl(const std::string& str);
```
- resp   —— PutBucketResp PutBucket操作的返回

#### 示例

```cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";

qcloud_cos::PutBucketReq req(bucket_name);
qcloud_cos::PutBucketResp resp;
qcloud_cos::CosResult result = cos.PutBucket(req, &resp);

// 调用成功，调用resp的成员函数获取返回内容
if (result.IsSucc()) {
    // ...
} else {
    // 创建Bucket失败，可以调用CosResult的成员函数输出错误信息，比如requestID等
}
```

###  Delete Bucket

#### 功能说明

Delete Bucket 接口请求可以在指定账号下删除 Bucket，删除之前要求 Bucket 内的内容为空，只有删除了 Bucket 内的信息，才能删除 Bucket 本身。详见:https://cloud.tencent.com/document/product/436/7732

#### 方法原型

```cpp
CosResult DeleteBucket(const DeleteBucketReq& req, DeleteBucketResp* resp);
```

#### 参数说明

- req   —— DeleteBucketReq DeleteBucket操作的请求

- resp   —— DeletBucketResp DeletBucket操作的返回

#### 示例

``` cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";

// DeleteBucketReq的构造函数需要传入bucket_name
qcloud_cos::DeleteBucketReq req(bucket_name);
qcloud_cos::DeleteBucketResp resp;
qcloud_cos::CosResult result = cos.DeleteBucket(req, &resp);

// 调用成功，调用resp的成员函数获取返回内容
if (result.IsSucc()) {
    // ...
} else {
    // 删除Bucket失败，可以调用CosResult的成员函数输出错误信息，比如requestID等
}
```

###  Put Bucket Replication

#### 功能说明

Put Bucket Replication 请求用于向开启版本管理的存储桶添加 replication 配置。如果存储桶已经拥有 replication 配置，那么该请求会替换现有配置。详见:https://cloud.tencent.com/document/product/436/11738

#### 方法原型

```cpp
CosResult PutBucketReplication(const PutBucketReplicationReq& req, PutBucketReplicationResp* resp);
```

#### 参数说明

- req   —— PutBucketReplicationReq PutBucketReplication操作的请求

``` cpp
// 设置Replication的发起者身份标示，role格式： qcs::cam::uin/[UIN]:uin/[Subaccount]
void SetRole(const std::string& role);

// 增加ReplicationRule
void AddReplicationRule(const ReplicationRule& rule);

// 设置ReplicationRules
void SetReplicationRule(const std::vector<ReplicationRule>& rules);
```

其中ReplicationRule的定义如下：
``` cpp
struct ReplicationRule {
    bool m_is_enable; // 该Rule是否生效
    std::string m_id; // 非必选字段，用来标注具体 Rule 的名称
    std::string m_prefix; // 前缀匹配策略，不可重叠，重叠返回错误。前缀匹配根目录为空
    std::string m_dest_bucket; // 标识目标Bucket，资源标识符：qcs:id/0:cos:[region]:appid/[AppId]:[bucketname]
    std::string m_dest_storage_class; // 非必选字段，存储级别，枚举值：Standard, Standard_IA；为空表示保持原存储桶级别

    ReplicationRule();
    ReplicationRule(const std::string& prefix,
                    const std::string& dest_bucket,
                    const std::string& storage_class = "",
                    const std::string& id = "",
                    bool is_enable = true);
};
```
- resp   —— PutBucketReplicationResp PutBucketReplication操作的返回

#### 示例

```cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";

// PutBucketReplicationReq的构造函数需要传入bucket_name
qcloud_cos::PutBucketReplicationReq req(bucket_name);
req.SetRole("qcs::cam::uin/***:uin/****");
qcloud_cos::ReplicationRule rule("sevenyou_10m", "qcs:id/0:cos:cn-south:appid/***:sevenyousouthtest", "", "RuleId_01", true);
req.AddReplicationRule(rule)

qcloud_cos::PutBucketReplicationResp resp;
qcloud_cos::CosResult result = cos.PutBucketReplication(req, &resp);

// 调用成功，调用resp的成员函数获取返回内容
if (result.IsSucc()) {
    // ...
} else {
    // 设置跨区域复制失败，可以调用CosResult的成员函数输出错误信息，比如requestID等
}
```

###  Get Bucket Replication

#### 功能说明

Get Bucket Replication 接口请求实现读取存储桶中用户跨区域复制配置信息。
详见:https://cloud.tencent.com/document/product/436/11736

#### 方法原型

```cpp
CosResult GetBucketReplication(const GetBucketReplicationReq& req, GetBucketReplicationResp* resp);
```

#### 参数说明

- req   —— GetBucketReplicationReq GetBucketReplication操作的请求

- resp   —— GetBucketReplicationResp GetBucketReplication操作的返回

``` cpp
// 获取Replication的发起者身份
std::string GetRole();

// 获取ReplicationRules, ReplicationRule定义参见Put Bucket Replication
std::vector<ReplicationRule> GetRules();
```

#### 示例

```cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";

// GetBucketReplicationReq的构造函数需要传入bucket_name
qcloud_cos::GetBucketReplicationReq req(bucket_name);
qcloud_cos::GetBucketReplicationResp resp;
qcloud_cos::CosResult result = cos.GetBucketReplication(req, &resp);

// 调用成功，调用resp的成员函数获取返回内容
if (result.IsSucc()) {
    // ...
} else {
    // 获取跨区域复制配置失败，可以调用CosResult的成员函数输出错误信息，比如requestID等
}
```

###  Delete Bucket Replication

#### 功能说明

Delete Bucket Replication 接口请求实现删除存储桶中用户跨区域复制配置。
详见: https://cloud.tencent.com/document/product/436/11737

#### 方法原型

```cpp
CosResult DeleteBucketReplication(const DDeleteBucketReplicationReq& req, DeleteBucketReplicationResp* resp);
```

#### 参数说明

- req   —— DeleteBucketReplicationReq DeleteBucketReplication操作的请求

- resp   —— DeleteBucketReplicationResp DeleteBucketReplication操作的返回

#### 示例

```cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";

// DeleteBucketReplicationReq的构造函数需要传入bucket_name
qcloud_cos::DeleteBucketReplicationReq req(bucket_name);
qcloud_cos::DeleteBucketReplicationResp resp;
qcloud_cos::CosResult result = cos.DeleteBucketReplication(req, &resp);

// 调用成功，调用resp的成员函数获取返回内容
if (result.IsSucc()) {
    // ...
} else {
    // 删除跨区域复制配置失败，可以调用CosResult的成员函数输出错误信息，比如requestID等
}
```

###  Put Bucket Versioning

#### 功能说明

Put Bucket Versioning 接口实现启用或者暂停存储桶的版本控制功能。详见:https://cloud.tencent.com/document/product/436/8591

#### 方法原型

```cpp
CosResult PutBucketVersioning(const PutBucketVersioningReq& req, PutBucketVersioningResp* resp);
```

#### 参数说明

- req   —— PutBucketVersioningReq PutBucketVersioning操作的请求

```
// 设置版本控制的状态, 开启或暂停
void SetStatus(bool is_enable);
```

- resp   —— PutBucketVersioningResp PutBucketVersioning操作的返回

#### 示例

``` cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";

// PutBucketVersioningReq的构造函数需要传入bucket_name
qcloud_cos::PutBucketVersioningReq req(bucket_name);
req.SetStatus(true);
qcloud_cos::PutBucketVersioningResp resp;
qcloud_cos::CosResult result = cos.PutBucketVersioning(req, &resp);

// 调用成功，调用resp的成员函数获取返回内容
if (result.IsSucc()) {
    // ...
} else {
    // 开启/暂停版本控制失败，可以调用CosResult的成员函数输出错误信息，比如requestID等
}
```

###  Get Bucket Versioning

#### 功能说明

Get Bucket Versioning 接口实现获得存储桶的版本控制信息。
详见: https://cloud.tencent.com/document/product/436/8597

#### 方法原型

```cpp
CosResult GetBucketVersioning(const GetBucketVersioningReq& req, GetBucketVersioningResp* resp);
```

#### 参数说明

- req   —— GetBucketVersioningReq GetBucketVersioning操作的请求

- resp   —— GetBucketVersioningResp GetBucketVersioning操作的返回

``` cpp
/// 返回bucket的版本状态,0: 从未开启版本管理, 1: 版本管理生效中, 2: 暂停
/// 区别于PutBucketVersioning, 一个Bucket可能处于三种状态
int GetStatus() const;
```

#### 示例

```cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";

// GetBucketVersioningReq的构造函数需要传入bucket_name
qcloud_cos::GetBucketVersioningReq req(bucket_name);
qcloud_cos::GetBucketVersioningnResp resp;
qcloud_cos::CosResult result = cos.GetBucketVersioning(req, &resp);

// 调用成功，调用resp的成员函数获取返回内容
if (result.IsSucc()) {
    int status = resp.GetStatus();
    if (0 == status) {
        // ...
    } else if (1 == status) {
        // ...
    } else {
        // ...
    }
} else {
    // 获取Versioning失败，可以调用CosResult的成员函数输出错误信息，比如requestID等
}
```

###  Put Bucket Lifecycle

#### 功能说明

COS 支持用户以生命周期配置的方式来管理 Bucket 中 Object 的生命周期。生命周期配置包含一个或多个将应用于一组对象规则的规则集 (其中每个规则为 COS 定义一个操作)。
这些操作分为以下两种：

转换操作：定义对象转换为另一个存储类的时间。例如，您可以选择在对象创建 30 天后将其转换为 STANDARD_IA (IA，适用于不常访问) 存储类别。
过期操作：指定 Object 的过期时间。COS 将会自动为用户删除过期的 Object。
Put Bucket Lifecycle 用于为 Bucket 创建一个新的生命周期配置。如果该 Bucket 已配置生命周期，使用该接口创建新的配置的同时则会覆盖原有的配置。

详见: https://cloud.tencent.com/document/product/436/8280

#### 方法原型

```cpp
CosResult PutBucketLifecycle(const DPutBucketLifecycleReq& req, PutBucketLifecycleResp* resp);
```

#### 参数说明

- req   —— PutBucketLifecycleReq PutBucketLifecycle操作的请求

``` cpp
// 新增LifecycleRule
void AddRule(const LifecycleRule& rule)

// 设置LifecycleRule
void SetRule(const std::vector<LifecycleRule>& rules)

```

LifecycleRule的定义比较复杂，具体如下：
``` cpp
struct LifecycleTag {
    std::string key;
    std::string value;
};

class LifecycleFilter {
public:
    LifecycleFilter();

    std::string GetPrefix();
    std::vector<LifecycleTag> GetTags();

    void SetPrefix(const std::string& prefix);
    void SetTags(const std::vector<LifecycleTag>& tags);
    void AddTag(const LifecycleTag& tag);

    bool HasPrefix();
    bool HasTags();

private:
    std::string m_prefix; // 指定规则所适用的前缀。匹配前缀的对象受该规则影响，Prefix 最多只能有一个
    std::vector<LifecycleTag> m_tags; // 标签，Tag 可以有零个或者多个
};

class LifecycleTransition {
public:
    LifecycleTransition();

    uint64_t GetDays();
    std::string GetDate();
    std::string GetStorageClass();

    void SetDays(uint64_t days);
    void SetDate(const std::string& date);
    void SetStorageClass(const std::string& storage_class);

    bool HasDays();
    bool HasDate();
    bool HasStorageClass();

private:
    // 不能在同一规则中同时使用Days和Date
    uint64_t m_days; // 指明规则对应的动作在对象最后的修改日期过后多少天操作, 有效值是非负整数
    std::string m_date; // 指明规则对应的动作在何时操作
    std::string m_storage_class; // 指定 Object 转储到的目标存储类型，枚举值： Standard_IA
};

class LifecycleExpiration {
public:
    LifecycleExpiration();

    uint64_t GetDays();
    std::string GetDate();
    bool IsExpiredObjDelMarker();

    void SetDays(uint64_t days);
    void SetDate(const std::string& date);
    void SetExpiredObjDelMarker(bool marker);

    bool HasDays();
    bool HasDate();
    bool HasExpiredObjDelMarker();

private:
    // 不能在同一规则中同时使用Days和Date
    uint64_t m_days; // 指明规则对应的动作在对象最后的修改日期过后多少天操作, 有效值为正整数
    std::string m_date; // 指明规则对应的动作在何时操作
    bool m_expired_obj_del_marker; // 删除过期对象删除标记，枚举值 true，false
};

class LifecycleNonCurrTransition {
public:
    LifecycleNonCurrTransition();

    uint64_t GetDays();
    std::string GetStorageClass();

    void SetDays(uint64_t days);
    void SetStorageClass(const std::string& storage_class);

    bool HasDays();
    bool HasStorageClass();

private:
    uint64_t m_days; // 指明规则对应的动作在对象最后的修改日期过后多少天操作, 有效值是非负整数
    std::string m_storage_class; // 指定 Object 转储到的目标存储类型，枚举值： Standard_IA
};

class LifecycleNonCurrExpiration {
public:
    LifecycleNonCurrExpiration();

    uint64_t GetDays();

    void SetDays(uint64_t days);

    bool HasDays();

private:
    uint64_t m_days; // 指明规则对应的动作在对象最后的修改日期过后多少天操作, 有效值为正整数
};

struct AbortIncompleteMultipartUpload {
    uint64_t m_days_after_init; // 指明分片上传开始后多少天内必须完成上传
};

class LifecycleRule {
public:
    LifecycleRule();

    void SetIsEnable(bool is_enable);
    void SetId(const std::string& id);
    void SetFilter(const LifecycleFilter& filter);
    void SetTransition(const LifecycleTransition& rh);
    void SetExpiration(const LifecycleExpiration& rh);
    void SetNonCurrTransition(const LifecycleNonCurrTransition& rh);
    void SetNonCurrExpiration(const LifecycleNonCurrExpiration& rh);
	void SetAbortIncompleteMultiUpload(const AbortIncompleteMultipartUpload& rh);

    bool IsEnable();
    std::string GetId();
    LifecycleFilter GetFilter();
    LifecycleTransition GetTransition();
    LifecycleExpiration GetExpiration();
    LifecycleNonCurrTransition GetNonCurrTransition();
    LifecycleNonCurrExpiration GetNonCurrExpiration();
    AbortIncompleteMultipartUpload GetAbortIncompleteMultiUpload();

    bool HasIsEnable();
    bool HasId();
    bool HasFilter();
    bool HasExpiration();
    bool HasNonCurrTransition();
    bool HasNonCurrExpiration();
    bool HasAbortIncomMultiUpload();

private:
    bool m_is_enable; // 规则是否生效
    std::string m_id; // 规则ID
    LifecycleFilter m_filter; // 过滤器，用来指定规则生效的Object范围
    LifecycleTransition m_transition; // 转换操作
    LifecycleExpiration m_expiration; // 过期操作
    LifecycleNonCurrTransition m_non_curr_transition; // 非当前版本转换操作
    LifecycleNonCurrExpiration m_non_curr_expiration; // 非当前版本过期操作
    AbortIncompleteMultipartUpload m_abort_multi_upload; // 设置允许分片上传保持运行的最长时间
}
```

- resp   —— PutBucketLifecycleResp PutBucketLifecycle操作的返回

#### 示例

```cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";

// PutBucketLifecycleReq的构造函数需要传入bucket_name
qcloud_cos::PutBucketLifecycleReq req(bucket_name);
// 设置规则1
{
    qcloud_cos::LifecycleRule rule;
    rule.SetIsEnable(true);
    rule.SetId("lifecycle_rule00");
    qcloud_cos::LifecycleFilter filter;
    filter.SetPrefix("sevenyou_e1");
    rule.SetFilter(filter);
    qcloud_cos::LifecycleExpiration expiration;
    expiration.SetDays(1);
    rule.SetExpiration(expiration);
    req.AddRule(rule);
}

// 设置规则2
{
    qcloud_cos::LifecycleRule rule;
    rule.SetIsEnable(true);
    rule.SetId("lifecycle_rule01");
    qcloud_cos::LifecycleFilter filter;
    filter.SetPrefix("sevenyou_e2");
    rule.SetFilter(filter);
    qcloud_cos::LifecycleExpiration expiration;
    expiration.SetDays(3);
    rule.SetExpiration(expiration);
    req.AddRule(rule);
}

qcloud_cos::PutBucketLifecycleResp resp;
qcloud_cos::CosResult result = cos.PutBucketLifecycle(req, &resp);

// 调用成功，调用resp的成员函数获取返回内容
if (result.IsSucc()) {
    // ...
} else {
    // 设置生命周期失败，可以调用CosResult的成员函数输出错误信息，比如requestID等
}
```

###  Get Bucket Lifecycle

#### 功能说明

Get Bucket Lifecycle 用来查询 Bucket 的生命周期配置。如果该 Bucket 没有配置生命周期规则会返回 NoSuchLifecycleConfiguration。
详见: https://cloud.tencent.com/document/product/436/8278

#### 方法原型

```cpp
CosResult GetBucketLifecycle(const DGetBucketLifecycleReq& req, GetBucketLifecycleResp* resp);
```

#### 参数说明

- req   —— GetBucketLifecycleReq GetBucketLifecycle操作的请求

- resp   —— GetBucketLifecycleResp GetBucketLifecycle操作的返回

``` cpp
// 获取LifecycleRules, LifecycleRule定义参见Put Bucket Lifecycle
std::vector<LifecycleRule> GetRules()
```

#### 示例

```cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";

// GetBucketLifecycleReq的构造函数需要传入bucket_name
qcloud_cos::GetBucketLifecycleReq req(bucket_name);
qcloud_cos::GetBucketLifecycleResp resp;
qcloud_cos::CosResult result = cos.GetBucketLifecycle(req, &resp);

// 调用成功，调用resp的成员函数获取返回内容
if (result.IsSucc()) {
    // ...
} else {
    // 获取生命周期配置失败，可以调用CosResult的成员函数输出错误信息，比如requestID等
}
```

###  Delete Bucket Lifecycle

#### 功能说明

Delete Bucket Lifecycle 用来删除 Bucket 的生命周期配置。如果该 Bucket 没有配置生命周期规则会返回 NoSuchLifecycleConfiguration。
详见: https://cloud.tencent.com/document/product/436/8284

#### 方法原型

```cpp
CosResult DeleteBucketLifecycle(const DDeleteBucketLifecycleReq& req, DeleteBucketLifecycleResp* resp);
```

#### 参数说明

- req   —— DeleteBucketLifecycleReq DeleteBucketLifecycle操作的请求

- resp   —— DeleteBucketLifecycleResp DeleteBucketLifecycle操作的返回


#### 示例

```cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";

// DeleteBucketLifecycleReq的构造函数需要传入bucket_name
qcloud_cos::DeleteBucketLifecycleReq req(bucket_name);
qcloud_cos::DeleteBucketLifecycleResp resp;
qcloud_cos::CosResult result = cos.DeleteBucketLifecycle(req, &resp);

// 调用成功，调用resp的成员函数获取返回内容
if (result.IsSucc()) {
    // ...
} else {
    // 删除生命周期配置失败，可以调用CosResult的成员函数输出错误信息，比如requestID等
}
```

###  Put Bucket CORS

#### 功能说明

CPut Bucket CORS 接口用来请求设置 Bucket 的跨域资源共享权限，您可以通过传入 XML 格式的配置文件来实现配置，文件大小限制为64 KB。默认情况下，Bucket 的持有者直接有权限使用该 API 接口，Bucket 持有者也可以将权限授予其他用户。

详见: https://cloud.tencent.com/document/product/436/8279

#### 方法原型

```cpp
CosResult PutBucketCORS(const DPutBucketCORSReq& req, PutBucketCORSResp* resp);
```

#### 参数说明

- req   —— PutBucketCORSReq PutBucketCORS操作的请求

``` cpp
// 新增CORSRule
void AddRule(const CORSRule& rule);

// 设置CORSRule
void SetRules(const std::vector<CORSRule>& rules)

```

CORSRule定义如下：
``` cpp
struct CORSRule {
    std::string m_id; // 配置规则的 ID，可选填
    std::string m_max_age_secs; // 设置 OPTIONS 请求得到结果的有效期
    std::vector<std::string> m_allowed_headers; // 在发送 OPTIONS 请求时告知服务端，接下来的请求可以使用哪些自定义的 HTTP 请求头部，支持通配符 *
    std::vector<std::string> m_allowed_methods; // 允许的 HTTP 操作，枚举值：GET，PUT，HEAD，POST，DELETE
    std::vector<std::string> m_allowed_origins; // 允许的访问来源，支持通配符 * ，格式为：协议://域名[:端口]如：http://www.qq.com
    std::vector<std::string> m_expose_headers;  // 设置浏览器可以接收到的来自服务器端的自定义头部信息
};

```

- resp   —— PutBucketCORSResp PutBucketCORS操作的返回

#### 示例

```cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";

// PutBucketCORSReq的构造函数需要传入bucket_name
qcloud_cos::PutBucketCORSReq req(bucket_name);
qcloud_cos::CORSRule rule;
rule.m_id = "123";
rule.m_allowed_headers.push_back("x-cos-meta-test");
rule.m_allowed_origins.push_back("http://www.qq.com");
rule.m_allowed_origins.push_back("http://www.qcloud.com");
rule.m_allowed_methods.push_back("PUT");
rule.m_allowed_methods.push_back("GET");
rule.m_max_age_secs = "600";
rule.m_expose_headers.push_back("x-cos-expose");
req.AddRule(rule);

qcloud_cos::PutBucketCORSResp resp;
qcloud_cos::CosResult result = cos.PutBucketCORS(req, &resp);

// 调用成功，调用resp的成员函数获取返回内容
if (result.IsSucc()) {
    // ...
} else {
    // 设置生命周期失败，可以调用CosResult的成员函数输出错误信息，比如requestID等
}
```

###  Get Bucket CORS

#### 功能说明

Get Bucket CORS 接口实现 Bucket 持有者在 Bucket 上进行跨域资源共享的信息配置。（CORS 是一个 W3C 标准，全称是"跨域资源共享"（Cross-origin resource sharing））。默认情况下，Bucket 的持有者直接有权限使用该 API 接口，Bucket 持有者也可以将权限授予其他用户。
详见: https://cloud.tencent.com/document/product/436/8274

#### 方法原型

```cpp
CosResult GetBucketCORS(const DGetBucketCORSReq& req, GetBucketCORSResp* resp);
```

#### 参数说明

- req   —— GetBucketCORSReq GetBucketCORS操作的请求

- resp   —— GetBucketCORSResp GetBucketCORS操作的返回

``` cpp
// 获取CORSRules, CORSRule定义参见Put Bucket CORS
std::vector<CORSRule> GetCORSRules();
```

#### 示例

```cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";

// GetBucketCORSReq的构造函数需要传入bucket_name
qcloud_cos::GetBucketCORSReq req(bucket_name);
qcloud_cos::GetBucketCORSResp resp;
qcloud_cos::CosResult result = cos.GetBucketCORS(req, &resp);

// 调用成功，调用resp的成员函数获取返回内容
if (result.IsSucc()) {
    // ...
} else {
    // 获取生命周期配置失败，可以调用CosResult的成员函数输出错误信息，比如requestID等
}
```

###  Delete Bucket CORS

#### 功能说明

Delete Bucket CORS 用来删除 Bucket 的生命周期配置。如果该 Bucket 没有配置生命周期规则会返回 NoSuchCORSConfiguration。
详见: https://cloud.tencent.com/document/product/436/8283

#### 方法原型

```cpp
CosResult DeleteBucketCORS(const DDeleteBucketCORSReq& req, DeleteBucketCORSResp* resp);
```

#### 参数说明

- req   —— DeleteBucketCORSReq DeleteBucketCORS操作的请求

- resp   —— DeleteBucketCORSResp DeleteBucketCORS操作的返回


#### 示例

```cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";

// DeleteBucketCORSReq的构造函数需要传入bucket_name
qcloud_cos::DeleteBucketCORSReq req(bucket_name);
qcloud_cos::DeleteBucketCORSResp resp;
qcloud_cos::CosResult result = cos.DeleteBucketCORS(req, &resp);

// 调用成功，调用resp的成员函数获取返回内容
if (result.IsSucc()) {
    // ...
} else {
    // 删除生命周期配置失败，可以调用CosResult的成员函数输出错误信息，比如requestID等
}
```

###  Put Bucket ACL

#### 功能说明

Put Bucket ACL 接口用来写入 Bucket 的 ACL 表，您可以通过 Header："x-cos-acl"，"x-cos-grant-read"，"x-cos-grant-write"，"x-cos-grant-full-control" 传入 ACL 信息，或者通过 Body 以 XML 格式传入 ACL 信息。

详见: https://cloud.tencent.com/document/product/436/7737

#### 方法原型

```cpp
CosResult PutBucketACL(const DPutBucketACLReq& req, PutBucketACLResp* resp);
```

#### 参数说明

- req   —— PutBucketACLReq PutBucketACL操作的请求

``` cpp
/// 定义Bucket的ACL属性,有效值：private,public-read-write,public-read
/// 默认值：private
void SetXCosAcl(const std::string& str);

/// 赋予被授权者读的权限.格式：x-cos-grant-read: id=" ",id=" ".
/// 当需要给子账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>"
/// 当需要给根账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>"
void SetXCosGrantRead(const std::string& str);

/// 赋予被授权者写的权限,格式：x-cos-grant-write: id=" ",id=" "./
/// 当需要给子账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>",
/// 当需要给根账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>"
void SetXCosGrantWrite(const std::string& str);

/// 赋予被授权者读写权限.格式：x-cos-grant-full-control: id=" ",id=" ".
/// 当需要给子账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>",
/// 当需要给根账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>"
void SetXCosGrantFullControl(const std::string& str);

/// Bucket 持有者 ID
void SetOwner(const Owner& owner);

/// 设置被授权者信息与权限信息
void SetAccessControlList(const std::vector<Grant>& grants);

/// 添加单个 Bucket 的授权信息
void AddAccessControlList(const Grant& grant);

```

> ** SetXCosAcl/SetXCosGrantRead/SetXCosGrantWrite/SetXCosGrantFullControl这类接口与SetAccessControlList/AddAccessControlList不可同时使用。因为前者实际是通过设置http header实现，而后者是在body中添加了xml格式的内容，二者只能二选一。 SDK内部优先使用第一类。 **

ACLRule定义如下：
``` cpp
struct Grantee {
    // type 类型可以为 RootAccount， SubAccount
	// 当 type 类型为 RootAccount 时，可以在 id 中 uin 中填写 QQ，可以在 id 中 uin 填写 QQ，也可以用 anyone（指代所有类型用户）代替 uin/<OwnerUin> 和 uin/<SubUin>
	// 当 type 类型为 RootAccount 时，uin 代表根账户账号，Subaccount 代表子账户账号
    std::string m_type;
    std::string m_id; // qcs::cam::uin/<OwnerUin>:uin/<SubUin>
    std::string m_display_name; // 非必选
    std::string m_uri;
};

struct Grant {
    Grantee m_grantee; // 被授权者资源信息
    std::string m_perm; // 指明授予被授权者的权限信息，枚举值：READ，WRITE，FULL_CONTROL
};

```

- resp   —— PutBucketACLResp PutBucketACL操作的返回

#### 示例

```cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";

// PutBucketACLReq的构造函数需要传入bucket_name
qcloud_cos::PutBucketACLReq req(bucket_name);
qcloud_cos::ACLRule rule;
rule.m_id = "123";
rule.m_allowed_headers.push_back("x-cos-meta-test");
rule.m_allowed_origins.push_back("http://www.qq.com");
rule.m_allowed_origins.push_back("http://www.qcloud.com");
rule.m_allowed_methods.push_back("PUT");
rule.m_allowed_methods.push_back("GET");
rule.m_max_age_secs = "600";
rule.m_expose_headers.push_back("x-cos-expose");
req.AddRule(rule);

qcloud_cos::PutBucketACLResp resp;
qcloud_cos::CosResult result = cos.PutBucketACL(req, &resp);

// 调用成功，调用resp的成员函数获取返回内容
if (result.IsSucc()) {
    // ...
} else {
    // 设置ACL，可以调用CosResult的成员函数输出错误信息，比如requestID等
}
```

###  Get Bucket ACL

#### 功能说明

Get Bucket ACL 接口用来获取 Bucket 的 ACL(access control list)， 即用户空间（Bucket）的访问权限控制列表。 此 API 接口只有 Bucket 的持有者有权限操作。
详见: https://cloud.tencent.com/document/product/436/7733

#### 方法原型

```cpp
CosResult GetBucketACL(const DGetBucketACLReq& req, GetBucketACLResp* resp);
```

#### 参数说明

- req   —— GetBucketACLReq GetBucketACL操作的请求

- resp   —— GetBucketACLResp GetBucketACL操作的返回

``` cpp
std::string GetOwnerID();
std::string GetOwnerDisplayName();
std::vector<Grant> GetAccessControlList();
```

#### 示例

```cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";

// GetBucketACLReq的构造函数需要传入bucket_name
qcloud_cos::GetBucketACLReq req(bucket_name);
qcloud_cos::GetBucketACLResp resp;
qcloud_cos::CosResult result = cos.GetBucketACL(req, &resp);

// 调用成功，调用resp的成员函数获取返回内容
if (result.IsSucc()) {
    // ...
} else {
    // 获取ACL失败，可以调用CosResult的成员函数输出错误信息，比如requestID等
}
```

## Object操作

###  Get Object

#### 功能说明

Get Object 请求可以将一个文件（Object）下载至本地或指定流中。该操作需要对目标 Object 具有读权限或目标 Object 对所有人都开放了读权限（公有读）。

#### 方法原型

```cpp
// 将Object下载到本地文件中
CosResult GetObject(const GetObjectByFileReq& req, GetObjectByFileResp* resp);

// 将Object下载到流中
CosResult GetObject(const GetObjectByStreamReq& req, GetObjectByStreamResp* resp);

// 将Object下载到本地文件中（多线程）
CosResult GetObject(const MultiGetObjectReq& req, MultiGetObjectResp* resp);
```

#### 参数说明

- req   —— GetObjectByFileReq/GetObjectByStreamReq/MultiGetObjectReq GetObject操作的请求

成员函数如下：
``` cpp
// 设置响应头部中的 Content-Type 参数
void SetResponseContentType(const std::string& str);

// 设置响应头部中的 Content-Language 参数
void SetResponseContentLang(const std::string& str);

// 设置响应头部中的 Content-Expires 参数
void SetResponseExpires(const std::string& str);

// 设置响应头部中的 Cache-Control 参数
void SetResponseCacheControl(const std::string& str);

// 设置响应头部中的 Content-Disposition 参数
void SetResponseContentDisposition(const std::string& str);

// 设置响应头部中的 Content-Encoding 参数
void SetResponseContentEncoding(const std::string& str);

/// \brief 请求参数中设置单链接限速,通过请求参数和请求头都可以设置,效果是一样的,
//  参考: https://cloud.tencent.com/document/product/436/40140
void SetTrafficLimitByParam(const std::string& str);

/// \brief 请求头中参数中设置单链接限速
void SetTrafficLimitByHeader(const std::string& str);
```

- resp   —— GetObjectByFileResp/GetObjectByStreamResp/MultiGetObjectResp GetObject操作的返回

GetObjectResp除了读取公共头部的成员函数外，还提供以下成员函数:

``` cpp
// 获取object最后被修改的时间, 字符串格式Date, 类似"Wed, 28 Oct 2014 20:30:00 GMT"
std::string GetLastModified();

// 获取object type, 表示object是否可以被追加上传，枚举值：normal 或者 appendable
std::string GetXCosObjectType();

// 获取Object 的存储级别，枚举值：STANDARD，STANDARD_IA
std::string GetXCosStorageClass();

// 以map形式返回所有自定义的meta, map的key均不包含"x-cos-meta-"前缀
std::map<std::string, std::string> GetXCosMetas();

// 获取自定义的meta, 参数可以为x-cos-meta-*中的*
std::string GetXCosMeta(const std::string& key);
```

#### 示例

```cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";
std::string object_name = "object_name";
std::string local_path = "/tmp/object_name";

// 下载到本地文件
{
    // request需要提供appid、bucketname、object,以及本地的路径（包含文件名）
    qcloud_cos::GetObjectByFileReq req(bucket_name, object_name, local_path);
    qcloud_cos::GetObjectByFileResp resp;
    qcloud_cos::CosResult result = cos.GetObject(req, &resp);
    if (result.IsSucc()) {
        // 下载成功，可以调用GetObjectByFileResp的成员函数
    } else {
        // 下载失败，可以调用CosResult的成员函数输出错误信息，比如requestID等
    }
}

// 下载到流中
{
    // request需要提供appid、bucketname、object, 以及输出流
    std::ostringstream os;
    qcloud_cos::GetObjectByStreamReq req(bucket_name, object_name, os);
    qcloud_cos::GetObjectByStreamResp resp;
    qcloud_cos::CosResult result = cos.GetObject(req, &resp);
    if (result.IsSucc()) {
        // 下载成功，可以调用GetObjectByStreamResp的成员函数
    } else {
        // 下载失败，可以调用CosResult的成员函数输出错误信息，比如requestID等
    }
}

// 多线程下载文件到本地
{
    // request需要提供appid、bucketname、object,以及本地的路径（包含文件名）
    qcloud_cos::MultiGetObjectReq req(bucket_name, object_name, local_path);
    qcloud_cos::MultiGetObjectResp resp;
    qcloud_cos::CosResult result = cos.GetObject(req, &resp);
    if (result.IsSucc()) {
        // 下载成功，可以调用MultiGetObjectResp的成员函数
    } else {
        // 下载失败，可以调用CosResult的成员函数输出错误信息，比如requestID等
    }
}
```

###  Head Object

#### 功能说明

Head Object 请求可以取回对应 Object 的元数据，Head的权限与 Get 的权限一致。

#### 方法原型

``` cpp
CosResult HeadObject(const HeadObjectReq& req, HeadObjectResp* resp);
```

#### 参数说明
- req   —— HeadObjectReq HeadObject操作的请求

- resp   —— HeadObjectResp HeadObject操作的返回

HeadObjectResp除了读取公共头部的成员函数外，还提供以下成员函数，
``` cpp
std::string GetXCosObjectType();

std::string GetXCosStorageClass();

// 获取自定义的meta, 参数可以为x-cos-meta-*中的*
std::string GetXCosMeta(const std::string& key);

// 以map形式返回所有自定义的meta, map的key均不包含"x-cos-meta-"前缀
std::map<std::string, std::string> GetXCosMetas()
```
#### 示例

```cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";
std::string object_name = "object_name";
qcloud_cos::HeadObjectReq req(bucket_name, object_name);
qcloud_cos::HeadObjectResp resp;
qcloud_cos::CosResult result = cos.HeadObject(req, &resp);
if (result.IsSucc()) {
    // 下载成功，可以调用HeadObjectResp的成员函数
} else {
    // 下载失败，可以调用CosResult的成员函数输出错误信息，比如requestID等
}
```

###  Put Object

#### 功能说明

Put Object请求可以将一个文件（Oject）上传至指定Bucket。

#### 方法原型

```cpp
/// 通过Stream进行上传
CosResult PutObject(const PutObjectByStreamReq& req, PutObjectByStreamResp* resp);

/// 上传本地文件
CosResult PutObject(const PutObjectByFileReq& req, PutObjectByFileResp* resp);
```

#### 参数说明
- req   ——PutObjectByStreamReq/PutObjectByFileReq PutObject操作的请求

``` cpp
/// Cache-Control RFC 2616 中定义的缓存策略，将作为 Object 元数据保存
void SetCacheControl(const std::string& str);

/// Content-Disposition RFC 2616 中定义的文件名称，将作为 Object 元数据保存
void SetContentDisposition(const std::string& str);

/// Content-Encoding    RFC 2616 中定义的编码格式，将作为 Object 元数据保存-
void SetContentEncoding(const std::string& str);

/// Content-Type    RFC 2616 中定义的内容类型（MIME），将作为 Object 元数据保存
void SetContentType(const std::string& str);

/// Expect  当使用 Expect: 100-continue 时，在收到服务端确认后，才会发送请求内容
void SetExpect(const std::string& str);

/// Expires RFC 2616 中定义的过期时间，将作为 Object 元数据保存
void SetExpires(const std::string& str);

/// 允许用户自定义的头部信息,将作为 Object 元数据返回.大小限制2K
void SetXCosMeta(const std::string& key, const std::string& value);

/// x-cos-storage-class 设置 Object 的存储级别，枚举值：STANDARD,STANDARD_IA，
/// 默认值：STANDARD（目前仅支持华南园区）
void SetXCosStorageClass(const std::string& storage_class);

/// 定义Object的ACL属性,有效值：private,public-read-write,public-read
/// 默认值：private
void SetXcosAcl(const std::string& str);

/// 赋予被授权者读的权限.格式：x-cos-grant-read: id=" ",id=" ".
/// 当需要给子账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>"
/// 当需要给根账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>"
void SetXcosGrantRead(const std::string& str);

/// 赋予被授权者写的权限,格式：x-cos-grant-write: id=" ",id=" "./
/// 当需要给子账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>",
/// 当需要给根账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>"
void SetXcosGrantWrite(const std::string& str);

/// 赋予被授权者读写权限.格式：x-cos-grant-full-control: id=" ",id=" ".
/// 当需要给子账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>",
/// 当需要给根账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>"
void SetXcosGrantFullControl(const std::string& str);
    
/// 设置Server端加密使用的算法, 目前支持AES256
void SetXCosServerSideEncryption(const std::string& str);

/// \brief 请求参数中设置单链接限速, 参考https://cloud.tencent.com/document/product/436/40140
void SetTrafficLimitByParam(const std::string& str);

/// \brief 请求头中参数中设置单链接限速
void SetTrafficLimitByHeader(const std::string& str);



- resp   ——PutObjectByStreamResp/PutObjectByFileResp PutObject操作的返回

#### 示例

```cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";
std::string object_name = "object_name";

// 简单上传(流)
{
    std::istringstream iss("put object");
    // request的构造函数中需要传入istream
    qcloud_cos::PutObjectByStreamReq req(bucket_name, object_name, iss);
    // 调用Set方法设置元数据或者ACL等
    req.SetXCosStorageClass("STANDARD_IA");
    qcloud_cos::PutObjectByStreamResp resp;
    qcloud_cos::CosResult result = cos.PutObject(req, &resp);

    if (result.IsSucc()) {
        // 调用成功，调用resp的成员函数获取返回内容
        do sth
    } else {
        // 调用失败，调用result的成员函数获取错误信息
        std::cout << "ErrorInfo=" << result.GetErrorInfo() << std::endl;
        std::cout << "HttpStatus=" << result.GetHttpStatus() << std::endl;
        std::cout << "ErrorCode=" << result.GetErrorCode() << std::endl;
        std::cout << "ErrorMsg=" << result.GetErrorMsg() << std::endl;
        std::cout << "ResourceAddr=" << result.GetResourceAddr() << std::endl;
        std::cout << "XCosRequestId=" << result.GetXCosRequestId() << std::endl;
        std::cout << "XCosTraceId=" << result.GetXCosTraceId() << std::endl;
     }
}

// 简单上传(文件)
{
    // request的构造函数中需要传入本地文件路径
    qcloud_cos::PutObjectByFileReq req(bucket_name, object_name, "/path/to/local/file");
    // 调用Set方法设置元数据或者ACL等
    req.SetXCosStorageClass("STANDARD_IA");
    qcloud_cos::PutObjectByFileResp resp;
    qcloud_cos::CosResult result = cos.PutObject(req, &resp);
        if (result.IsSucc()) {
        // 调用成功，调用resp的成员函数获取返回内容
        do sth
    } else {
        // 调用失败，调用result的成员函数获取错误信息
        std::cout << "ErrorInfo=" << result.GetErrorInfo() << std::endl;
        std::cout << "HttpStatus=" << result.GetHttpStatus() << std::endl;
        std::cout << "ErrorCode=" << result.GetErrorCode() << std::endl;
        std::cout << "ErrorMsg=" << result.GetErrorMsg() << std::endl;
        std::cout << "ResourceAddr=" << result.GetResourceAddr() << std::endl;
        std::cout << "XCosRequestId=" << result.GetXCosRequestId() << std::endl;
        std::cout << "XCosTraceId=" << result.GetXCosTraceId() << std::endl;
     }
}
```

###  Delete Object

#### 功能说明

Delete Object 接口请求可以在 COS 的 Bucket 中将一个文件（Object）删除。该操作需要请求者对 Bucket 有 WRITE 权限。
详见: https://cloud.tencent.com/document/product/436/7743

#### 方法原型

```cpp
CosResult DeleteObject(const DeleteObjectReq& req, DeleteObjectResp* resp);
```

#### 参数说明

- req   —— DeleteObjectReq DeleteObject操作的请求

``` cpp
/// 删除指定版本号的对象
void SetXCosVersionId(const std::string& version_id);
```

- resp   —— DeletObjectResp DeletObject操作的返回

#### 示例

``` cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";
std::string object_name = "test_object";

qcloud_cos::DeleteObjectReq req(bucket_name, object_name);
qcloud_cos::DeleteObjectResp resp;
qcloud_cos::CosResult result = cos.DeleteObject(req, &resp);

// 调用成功，调用resp的成员函数获取返回内容
if (result.IsSucc()) {
    // ...
} else {
    // 删除Object失败，可以调用CosResult的成员函数输出错误信息，比如requestID等
}
```

## 分块上传操作

###  Initiate Multipart Upload

#### 功能说明

Initiate Multipart Upload请求实现初始化分片上传，成功执行此请求以后会返回Upload ID用于后续的Upload Part请求。

#### 方法原型

```cpp
CosResult InitMultiUpload(const InitMultiUploadReq& req, InitMultiUploadResp* resp);
```

#### 参数说明
- req   —— InitMultiUploadReq InitMultiUpload操作的请求

``` cpp
/// Cache-Control RFC 2616 中定义的缓存策略，将作为 Object 元数据保存
void SetCacheControl(const std::string& str);

/// Content-Disposition RFC 2616 中定义的文件名称，将作为 Object 元数据保存
void SetContentDisposition(const std::string& str);

/// Content-Encoding    RFC 2616 中定义的编码格式，将作为 Object 元数据保存-
void SetContentEncoding(const std::string& str);

/// Content-Type    RFC 2616 中定义的内容类型（MIME），将作为 Object 元数据保存
void SetContentType(const std::string& str);

/// Expires RFC 2616 中定义的过期时间，将作为 Object 元数据保存
void SetExpires(const std::string& str);

/// 允许用户自定义的头部信息,将作为 Object 元数据返回.大小限制2K
void SetXCosMeta(const std::string& key, const std::string& value);

/// x-cos-storage-class 设置 Object 的存储级别，枚举值：STANDARD,STANDARD_IA，
/// 默认值：STANDARD
void SetXCosStorageClass(const std::string& storage_class);

/// 定义Object的ACL属性,有效值：private,public-read-write,public-read
/// 默认值：private
void SetXcosAcl(const std::string& str);

/// 赋予被授权者读的权限.格式：x-cos-grant-read: id=" ",id=" ".
/// 当需要给子账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>"
/// 当需要给根账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>"
void SetXcosGrantRead(const std::string& str);

/// 赋予被授权者写的权限,格式：x-cos-grant-write: id=" ",id=" "./
/// 当需要给子账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>",
/// 当需要给根账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>"
void SetXcosGrantWrite(const std::string& str);

/// 赋予被授权者读写权限.格式：x-cos-grant-full-control: id=" ",id=" ".
/// 当需要给子账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>",
/// 当需要给根账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>"
void SetXcosGrantFullControl(const std::string& str);
```

- resp   —— InitMultiUploadResp InitMultiUpload操作的返回

如果成功执行此请求后，返回的response中会包含bucket、key、uploadId， 分别表示分片上传的目标 Bucket、object名称以及后续分片上传所需的编号。

``` cpp
std::string GetBucket();
std::string GetKey();
std::string GetUploadId();
```

#### 示例

```cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);
std::string bucket_name = "cpp_sdk_v5-12345";
std::string object_name = "object_name";

qcloud_cos::InitMultiUploadReq req(bucket_name, object_name);
qcloud_cos::InitMultiUploadResp resp;
qcloud_cos::CosResult result = cos.InitMultiUpload(req, &resp);

std::string upload_id = "";
if (result.IsSucc()) {
    upload_id = resp.GetUploadId();
}
```

###  Upload Part

#### 功能说明

Upload Part请求实现在初始化以后的分块上传，支持的块的数量为1到10000，块的大小为1 MB 到5 GB。在每次请求Upload Part时候，需要携带partNumber和uploadID，partNumber为块的编号，支持乱序上传。

#### 方法原型

```cpp
CosResult UploadPartData(const UploadPartDataReq& request, UploadPartDataResp* response);
```

#### 参数说明
- req   —— UploadPartDataReq UploadPartData操作的请求

UploadPartDataReq在构造时，需要指明请求的appid、bucket、object、初始化成功后获取的uploadId, 以及上传的数据流(*调用完成后，流由调用方自己负责关闭*)。
``` cpp
UploadPartDataReq(const std::string& bucket_name,
                  const std::string& object_name, const std::string& upload_id,
                  std::istream& in_stream);
```
此外，请求还需要设置分片编号, 这个分片在完成分片上传时也会用到。
``` cpp
void SetPartNumber(uint64_t part_number);
```

- resp   —— UploadPartDataResp UploadPartData操作的返回


#### 示例

```cpp
// 上传第一个分片
{
    std::fstream is("demo_5M.part1");
    qcloud_cos::UploadPartDataReq req(bucket_name, object_name,
                                      upload_id, is);
    req.SetPartNumber(1);
    qcloud_cos::UploadPartDataResp resp;
    qcloud_cos::CosResult result = cos.UploadPartData(req, &resp);

    // 上传成功需要记录分片编号以及返回的etag
    if (result.IsSucc()) {
        etags.push_back(resp.GetEtag());
        part_numbers.push_back(1);
    }
    is.close();
}

// 上传第二个分片
{
    std::fstream is("demo_5M.part2");
    qcloud_cos::UploadPartDataReq req(bucket_name, object_name,
                                      upload_id, is);
    req.SetPartNumber(2);
    qcloud_cos::UploadPartDataResp resp;
    qcloud_cos::CosResult result = cos.UploadPartData(req, &resp);

    // 上传成功需要记录分片编号以及返回的etag
    if (result.IsSucc()) {
        etags.push_back(resp.GetEtag());
        part_numbers.push_back(2);
    }
    is.close();
}
```

###  Complete Multipart Upload

#### 功能说明

Complete Multipart Upload用来实现完成整个分块上传。当您已经使用Upload Parts上传所有块以后，你可以用该API完成上传。在使用该API时，您必须在Body中给出每一个块的PartNumber和ETag，用来校验块的准确性。

#### 方法原型

```cpp
CosResult CompleteMultiUpload(const CompleteMultiUploadReq& request, CompleteMultiUploadResp* response);
```

#### 参数说明
- req   —— CompleteMultiUploadReq CompleteMultiUploadReq操作的请求

CompleteMultiUploadReq在构造时，需要指明请求的appid、bucket、object、初始化成功后获取的uploadId。
```
CompleteMultiUploadReq(const std::string& bucket_name,
                       const std::string& object_name, const std::string& upload_id)
```
此外，request还需要设置所有上传的分片编号和Etag。

``` cpp
// 调用下列方法时，应注意编号和etag的顺序必须一一对应
void SetPartNumbers(const std::vector<uint64_t>& part_numbers);
void SetEtags(const std::vector<std::string>& etags) ;

// 添加part_number和etag对
void AddPartEtagPair(uint64_t part_number, const std::string& etag);
```

- resp   —— CompleteMultiUploadResp CompleteMultiUpload操作的请求

CompleteMultiUploadResp 的返回内容中包括Location、Bucket、Key、ETag，分别表示创建的Object的外网访问域名、分块上传的目标Bucket、Object的名称、合并后文件的 MD5 算法校验值。可以调用下列成员函数对response中的内容进行访问。

``` cpp
std::string GetLocation();
std::string GetKey();
std::string GetBucket();
std::string GetEtag();
```
#### 示例

```cpp
qcloud_cos::CompleteMultiUploadReq req(bucket_name, object_name, upload_id);
qcloud_cos::CompleteMultiUploadResp resp;
req.SetEtags(etags);
req.SetPartNumbers(part_numbers);

qcloud_cos::CosResult result = cos.CompleteMultiUpload(req, &resp);
```

###  Multipart Upload

#### 功能说明

Multipart Upload封装了初始化分块上传、分块上传、完成分块上传三步, 只需要在请求中指明上传的文件。

#### 方法原型

```cpp
CosResult MultiUploadObject(const MultiUploadObjectReq& request,        MultiUploadObjectResp* response);
```

#### 参数说明

- req   —— MultiUploadObjectReq MultiUploadObject操作的请求

MultiUploadObjectReq需要在构造的时候指明bucket、object以及待上传文件的本地路径， 如果不指明本地路径，则默认是当前工作路径下与object同名的文件。

``` cpp
MultiUploadObjectReq(const std::string& bucket_name,
                     const std::string& object_name, const std::string& local_file_path = "");
```

- resp —— MultiUploadObjectResp MultiUploadObject操作的返回

分块上传成功的情况下，该Response的返回内容与CompleteMultiUploadResp一致。
分块上传失败的情况下，该Response根据不同的失败情况，返回内容与InitMultiUploadResp、UploadPartDataResp、CompleteMultiUploadResp一致。可调用`GetRespTag()`来获取具体失败在哪一步。

``` cpp
// 返回Init、Upload、Complete
std::string GetRespTag();
```

#### 示例

``` cpp
qcloud_cos::MultiUploadObjectReq req( bucket_name, object_name, "/temp/demo_6G.tmp");
qcloud_cos::MultiUploadObjectResp resp;
qcloud_cos::CosResult result = cos.MultiUploadObject(req, &resp);

if (result.IsSucc()) {
    std::cout << resp.GetLocation() << std::endl;
    std::cout << resp.GetKey() << std::endl;
    std::cout << resp.GetBucket() << std::endl;
    std::cout << resp.GetEtag() << std::endl;
} else {
    // 获取具体失败在哪一步
    std::string resp_tag = resp.GetRespTag();
    if ("Init" == resp_tag) {
        // print result
    } else if ("Upload" == resp_tag) {
        // print result
    } else if ("Complete" == resp_tag) {
        // print result
    }
}
```

###  Abort Multipart Upload

#### 功能说明

Abort Multipart Upload用来实现舍弃一个分块上传并删除已上传的块。当您调用Abort Multipart Upload时，如果有正在使用这个Upload Parts上传块的请求，则Upload Parts会返回失败。

#### 方法原型

```cpp
CosResult AbortMultiUpload(const AbortMultiUploadReq& request, AbortMultiUploadResp* response);
```

#### 参数说明
- req    —— AbortMultiUploadReq AbortMultiUpload操作的请求

AbortMultiUploadReq需要在构造的时候指明bucket、object以及upload_id。
``` cpp
AbortMultiUploadReq(const std::string& bucket_name,
                    const std::string& object_name, const std::string& upload_id);
```

- resp —— AbortMultiUploadResp AbortMultiUpload操作的返回
无特殊方法，可调用BaseResp的成员函数来获取公共头部内容。

#### 示例

```cpp
qcloud_cos::AbortMultiUploadReq req(bucket_name, object_name,
                                                    upload_id);
qcloud_cos::AbortMultiUploadResp resp;
qcloud_cos::CosResult result = cos.AbortMultiUpload(req, &resp);
```

###  List Parts

#### 功能说明

List Parts 用来查询特定分块上传中的已上传的块，即罗列出指定 UploadId 所属的所有已上传成功的分块。
详见: https://cloud.tencent.com/document/product/436/7747

#### 方法原型

```cpp
CosResult ListParts(const ListPartsReq& req, ListPartsResp* resp);
```

#### 参数说明

- req   —— ListPartsReq ListParts操作的请求

``` cpp
// 构造函数，bucket名、object名、分块上传的 ID
ListPartsReq(const std::string& bucket_name,
             const std::string& object_name,
             const std::string& upload_id);

/// \brief 规定返回值的编码方式
void SetEncodingType(const std::string& encoding_type);

/// \brief 单次返回最大的条目数量，若不设置，默认 1000
void SetMaxParts(uint64_t max_parts);

/// \brief 默认以 UTF-8 二进制顺序列出条目，所有列出条目从 marker 开始
void SetPartNumberMarker(const std::string& part_number_marker);
```

- resp   —— ListPartsResp ListParts操作的返回

``` cpp
// 分块上传的目标 Bucket
std::string GetBucket();

// 规定返回值的编码方式
std::string GetEncodingType();

// Object 的名称
std::string GetKey();

// 标识本次分块上传的 ID
std::string GetUploadId();

// 用来表示本次上传发起者的信息
Initiator GetInitiator();

// 用来表示这些分块所有者的信息
Owner GetOwner();

// 默认以 UTF-8 二进制顺序列出条目，所有列出条目从 marker 开始
uint64_t GetPartNumberMarker();

// 返回每一个块的信息
std::vector<Part> GetParts();

// 假如返回条目被截断，则返回 NextMarker 就是下一个条目的起点
uint64_t GetNextPartNumberMarker();

// 用来表示这些分块的存储级别，枚举值：Standard，Standard_IA
std::string GetStorageClass();

// 单次返回最大的条目数量
uint64_t GetMaxParts();

// 返回条目是否被截断，布尔值：TRUE，FALSE
bool IsTruncated();
```

其中Part、Owner、Initiator的定义如下:

``` cpp
struct Initiator {
    std::string m_id; // 创建者的一个唯一标识
    std::string m_display_name; // 创建者的用户名描述
};

struct Owner {
    std::string m_id; // 用户的一个唯一标识
    std::string m_display_name; // 用户名描述
};

struct Part {
    uint64_t m_part_num; // 块的编号
    uint64_t m_size; // 块大小，单位 Byte
    std::string m_etag; // Object 块的 MD5 算法校验值
    std::string m_last_modified; // 块最后修改时间
};
```

#### 示例

```cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";
std::string object_name = "test_object";

// uploadId 是调用 InitMultiUpload 后获取的
qcloud_cos::ListPartsReq req(bucket_name, object_name, upload_id);
req.SetMaxParts(1);
req.SetPartNumberMarker("1");
qcloud_cos::ListPartsResp resp;
qcloud_cos::CosResult result = cos.ListParts(req, &resp);

// 调用成功，调用resp的成员函数获取返回内容
if (result.IsSucc()) {
    // ...
} else {
    // 删除Object失败，可以调用CosResult的成员函数输出错误信息，比如requestID等
}
```

###  Put Object ACL

#### 功能说明

Put Object ACL 接口用来写入 Object 的 ACL 表，您可以通过 Header："x-cos-acl"，"x-cos-grant-read"，"x-cos-grant-write"，"x-cos-grant-full-control" 传入 ACL 信息，或者通过 Body 以 XML 格式传入 ACL 信息。

详见: https://cloud.tencent.com/document/product/436/7748

#### 方法原型

```cpp
CosResult PutObjectACL(const PutObjectACLReq& req, PutObjectACLResp* resp);
```

#### 参数说明

- req   —— PutObjectACLReq PutObjectACL操作的请求

``` cpp
/// 定义Object的ACL属性,有效值：private,public-read-write,public-read
/// 默认值：private
void SetXCosAcl(const std::string& str);

/// 赋予被授权者读的权限.格式：x-cos-grant-read: id=" ",id=" ".
/// 当需要给子账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>"
/// 当需要给根账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>"
void SetXCosGrantRead(const std::string& str);

/// 赋予被授权者写的权限,格式：x-cos-grant-write: id=" ",id=" "./
/// 当需要给子账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>",
/// 当需要给根账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>"
void SetXCosGrantWrite(const std::string& str);

/// 赋予被授权者读写权限.格式：x-cos-grant-full-control: id=" ",id=" ".
/// 当需要给子账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>",
/// 当需要给根账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>"
void SetXCosGrantFullControl(const std::string& str);

/// Object 持有者 ID
void SetOwner(const Owner& owner);

/// 设置被授权者信息与权限信息
void SetAccessControlList(const std::vector<Grant>& grants);

/// 添加单个 Object 的授权信息
void AddAccessControlList(const Grant& grant);

```

> ** SetXCosAcl/SetXCosGrantRead/SetXCosGrantWrite/SetXCosGrantFullControl这类接口与SetAccessControlList/AddAccessControlList不可同时使用。因为前者实际是通过设置http header实现，而后者是在body中添加了xml格式的内容，二者只能二选一。 SDK内部优先使用第一类。 **

ACLRule定义如下：
``` cpp
struct Grantee {
    // type 类型可以为 RootAccount， SubAccount
	// 当 type 类型为 RootAccount 时，可以在 id 中 uin 中填写 QQ，可以在 id 中 uin 填写 QQ，也可以用 anyone（指代所有类型用户）代替 uin/<OwnerUin> 和 uin/<SubUin>
	// 当 type 类型为 RootAccount 时，uin 代表根账户账号，Subaccount 代表子账户账号
    std::string m_type;
    std::string m_id; // qcs::cam::uin/<OwnerUin>:uin/<SubUin>
    std::string m_display_name; // 非必选
    std::string m_uri;
};

struct Grant {
    Grantee m_grantee; // 被授权者资源信息
    std::string m_perm; // 指明授予被授权者的权限信息，枚举值：READ，WRITE，FULL_CONTROL
};

```

- resp   —— PutObjectACLResp PutObjectACL操作的返回

#### 示例

```cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";
std::string object_name = "sevenyou";

// 1 设置ACL配置(通过Body, 设置ACL可以通过Body、Header两种方式，但只能二选一，否则会有冲突)
{
    qcloud_cos::PutObjectACLReq req(bucket_name, object_name);
    qcloud_cos::Owner owner = {"qcs::cam::uin/xxxxx:uin/xxx", "qcs::cam::uin/xxxxxx:uin/xxxxx" };
    qcloud_cos::Grant grant;
    req.SetOwner(owner);
    grant.m_grantee.m_type = "Group";
    grant.m_grantee.m_uri = "http://cam.qcloud.com/groups/global/AllUsers";
    grant.m_perm = "READ";
    req.AddAccessControlList(grant);

    qcloud_cos::PutObjectACLResp resp;
    qcloud_cos::CosResult result = cos.PutObjectACL(req, &resp);
	// 调用成功，调用resp的成员函数获取返回内容
    if (result.IsSucc()) {
        // ...
    } else {
        // 设置ACL，可以调用CosResult的成员函数输出错误信息，比如requestID等
    }
}

// 2 设置ACL配置(通过Header, 设置ACL可以通过Body、Header两种方式，但只能二选一，否则会有冲突)
{
    qcloud_cos::PutObjectACLReq req(bucket_name, object_name);
    req.SetXCosAcl("public-read-write");

    qcloud_cos::PutObjectACLResp resp;
    qcloud_cos::CosResult result = cos.PutObjectACL(req, &resp);
    // 调用成功，调用resp的成员函数获取返回内容
    if (result.IsSucc()) {
        // ...
    } else {
        // 设置ACL，可以调用CosResult的成员函数输出错误信息，比如requestID等
    }
}

```

###  Get Object ACL

#### 功能说明

Get Object ACL 接口用来获取 Object 的 ACL(access control list)， 即用户空间（Object）的访问权限控制列表。 此 API 接口只有 Object 的持有者有权限操作。
详见: https://cloud.tencent.com/document/product/436/7744

#### 方法原型

``` cpp
CosResult GetObjectACL(const DGetObjectACLReq& req, GetObjectACLResp* resp);
```

#### 参数说明

- req   —— GetObjectACLReq GetObjectACL操作的请求

- resp   —— GetObjectACLResp GetObjectACL操作的返回

``` cpp
std::string GetOwnerID();
std::string GetOwnerDisplayName();
std::vector<Grant> GetAccessControlList();
```

#### 示例

```cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string Object_name = "cpp_sdk_v5-12345";

// GetObjectACLReq的构造函数需要传入Object_name
qcloud_cos::GetObjectACLReq req(Object_name);
qcloud_cos::GetObjectACLResp resp;
qcloud_cos::CosResult result = cos.GetObjectACL(req, &resp);

// 调用成功，调用resp的成员函数获取返回内容
if (result.IsSucc()) {
    // ...
} else {
    // 获取ACL失败，可以调用CosResult的成员函数输出错误信息，比如requestID等
}
```

###  Put Object Copy

#### 功能说明

Put Object Copy 请求实现将一个文件从源路径复制到目标路径。建议文件大小 1M 到 5G，超过 5G 的文件请使用分块上传 Upload - Copy。在拷贝的过程中，文件元属性和 ACL 可以被修改。
用户可以通过该接口实现文件移动，文件重命名，修改文件属性和创建副本。

详见: https://cloud.tencent.com/document/product/436/10881

#### 方法原型

```cpp
CosResult PutObjectCopy(const PutObjectCopyReq& req, PutObjectCopyResp* resp);
```

#### 参数说明

- req   —— PutObjectCopyReq PutObjectCopy操作的请求

``` cpp
/// 源文件 URL 路径，可以通过 versionid 子资源指定历史版本
void SetXCosCopySource(const std::string& str);

/// 是否拷贝元数据，枚举值：Copy, Replaced，默认值 Copy。
/// 假如标记为 Copy，忽略 Header 中的用户元数据信息直接复制；
/// 假如标记为 Replaced，按 Header 信息修改元数据。
/// 当目标路径和原路径一致，即用户试图修改元数据时，必须为 Replaced
void SetXCosMetadataDirective(const std::string& str);

/// 当 Object 在指定时间后被修改，则执行操作，否则返回 412。
/// 可与 x-cos-copy-source-If-None-Match 一起使用，与其他条件联合使用返回冲突。
void SetXCosCopySourceIfModifiedSince(const std::string& str);

/// 当 Object 在指定时间后未被修改，则执行操作，否则返回 412。
/// 可与 x-cos-copy-source-If-Match 一起使用，与其他条件联合使用返回冲突。
void SetXCosCopySourceIfUnmodifiedSince(const std::string& str);

/// 当 Object 的 Etag 和给定一致时，则执行操作，否则返回 412。
/// 可与x-cos-copy-source-If-Unmodified-Since 一起使用，与其他条件联合使用返回冲突
void SetXCosCopySourceIfMatch(const std::string& str);

/// 当 Object 的 Etag 和给定不一致时，则执行操作，否则返回 412。
/// 可与 x-cos-copy-source-If-Modified-Since 一起使用，与其他条件联合使用返回冲突。
void SetXCosCopySourceIfNoneMatch(const std::string& str);

/// x-cos-storage-class 设置 Object 的存储级别，枚举值：STANDARD,STANDARD_IA，
/// 默认值：STANDARD（目前仅支持华南园区）
void SetXCosStorageClass(const std::string& storage_class);

/// 定义Object的ACL属性,有效值：private,public-read-write,public-read
/// 默认值：private
void SetXCosAcl(const std::string& str);

    /// 赋予被授权者读的权限.格式：x-cos-grant-read: id=" ",id=" ".
/// 当需要给子账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>"
/// 当需要给根账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>"
void SetXCosGrantRead(const std::string& str);

/// 赋予被授权者写的权限,格式：x-cos-grant-write: id=" ",id=" "./
/// 当需要给子账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>",
/// 当需要给根账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>"
void SetXCosGrantWrite(const std::string& str);

/// 赋予被授权者读写权限.格式：x-cos-grant-full-control: id=" ",id=" ".
/// 当需要给子账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>",
/// 当需要给根账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>"
void SetXCosGrantFullControl(const std::string& str);

/// 允许用户自定义的头部信息,将作为 Object 元数据返回.大小限制2K
void SetXCosMeta(const std::string& key, const std::string& value);
```

- resp   —— PutObjectCopyResp PutObjectCopy操作的返回

``` cpp
// 返回文件的 MD5 算法校验值。ETag 的值可以用于检查 Object 的内容是否发生变化。
std::string GetEtag();

// 返回文件最后修改时间，GMT 格式
std::string GetLastModified();

// 返回版本号
std::string GetVersionId();
```

#### 示例

```cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";
std::string object_name = "sevenyou";

qcloud_cos::PutObjectCopyReq req(bucket_name, object_name);
req.SetXCosCopySource("sevenyousouthtest-12345656.cn-south.myqcloud.com/sevenyou_source_obj");
qcloud_cos::PutObjectCopyResp resp;
qcloud_cos::CosResult result = cos.PutObjectCopy(req, &resp);
```

###  Upload Part Copy

#### 功能说明

Upload Part Copy 请求实现将一个文件的分块内容从源路径复制到目标路径。通过指定 x-cos-copy-source 来指定源文件，x-cos-copy-source-range 指定字节范围。允许分块的大小为 5 MB - 5 GB。

详见: https://cloud.tencent.com/document/product/436/8287

> 与UploadPartData类似，在调用UploadPartCopy之前必须调用InitMultiUpload获取upload_id, 同时可以通过InitMultiUpload设置StorageClass及ACL等信息。 在完成所有UploadPartCopy之后需要调用CompleteMultiUpload来完成Copy操作。

#### 方法原型

```cpp
CosResult UploadPartCopyData(const UploadPartCopyDataReq& req, UploadPartCopyDataResp* resp);
```

#### 参数说明

- req   —— UploadPartCopyDataReq UploadPartCopy操作的请求

``` cpp
/// 构造函数， 其中
/// bucket_name为要复制的目的Bucket
/// object_name为目标Object
/// upload_id是调用InitMultiUpload返回的上传Id
UploadPartCopyDataReq(const std::string& bucket_name,
                      const std::string& object_name,
                      const std::string& upload_id);

/// 构造函数， 其中
/// bucket_name为要复制的目的Bucket
/// object_name为目标Object
/// upload_id是调用InitMultiUpload返回的上传Id
/// part_number是本次上传的分块号
UploadPartCopyDataReq(const std::string& bucket_name,
                      const std::string& object_name,
                      const std::string& upload_id,
                      uint64_t part_number);

/// 设置本次分块复制的ID
void SetUploadId(const std::string& upload_id);

/// 设置本次分块复制的编号
void SetPartNumber(uint64_t part_number);

/// 源文件 URL 路径，可以通过 versionid 子资源指定历史版本
void SetXCosCopySource(const std::string& str);

/// 设置源文件的字节范围
/// 范围值必须使用 bytes=first-last 格式，first 和 last 都是基于 0 开始的偏移量
/// 例如 bytes=0-9 表示你希望拷贝源文件的开头10个字节的数据，如果不指定，则表示拷贝整个文件
void SetXCosCopySourceRange(const std::string& range);

/// 当 Object 在指定时间后被修改，则执行操作，否则返回 412。
/// 可与 x-cos-copy-source-If-None-Match 一起使用，与其他条件联合使用返回冲突。
void SetXCosCopySourceIfModifiedSince(const std::string& str);

/// 当 Object 在指定时间后未被修改，则执行操作，否则返回 412。
/// 可与 x-cos-copy-source-If-Match 一起使用，与其他条件联合使用返回冲突。
void SetXCosCopySourceIfUnmodifiedSince(const std::string& str);

/// 当 Object 的 Etag 和给定一致时，则执行操作，否则返回 412。
/// 可与x-cos-copy-source-If-Unmodified-Since 一起使用，与其他条件联合使用返回冲突
void SetXCosCopySourceIfMatch(const std::string& str);

/// 当 Object 的 Etag 和给定不一致时，则执行操作，否则返回 412。
/// 可与 x-cos-copy-source-If-Modified-Since 一起使用，与其他条件联合使用返回冲突。
void SetXCosCopySourceIfNoneMatch(const std::string& str);
```

- resp   —— UploadPartCopyResp UploadPartCopy操作的返回

``` cpp
// 	返回文件的 MD5 算法校验值。ETag 的值可以用于检查 Object 的内容是否发生变化。
std::string GetEtag();

// 返回文件最后修改时间，GMT 格式
std::string GetLastModified();
```

#### 示例

```cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";
std::string object_name = "sevenyou";
std::string upload_id = "";
std::vector<std::string> etags;
std::vector<int64_t> part_nums;

// 伪代码
// 调用InitMultiUpload获取uploadId
upload_id = InitMultiUpload(...)

// 拷贝第一个分片
{
    std::string part_number = 1;
    qcloud_cos::UploadPartCopyDataReq req(bucket_name, object_name, upload_id, part_number);
    req.SetXCosCopySource("sevenyousouthtest-12345656.cn-south.myqcloud.com/sevenyou_source_obj");
    qcloud_cos::UploadPartCopyDataResp resp;
    qcloud_cos::CosResult result = cos.UploadPartCopyData(req, &resp);
    if (result.IsSucc()) {
        etags.push_back(resp.GetEtag());
        part_nums.push_back(part_number);
    }
}

// 拷贝第二个分片
{
    std::string part_number = 2;
    qcloud_cos::UploadPartCopyDataReq req(bucket_name, object_name, upload_id, part_number);
    req.SetXCosCopySource("sevenyousouthtest-12345656.cn-south.myqcloud.com/sevenyou_source_obj");
    qcloud_cos::UploadPartCopyDataResp resp;
    qcloud_cos::CosResult result = cos.UploadPartCopyData(req, &resp);
    if (result.IsSucc()) {
        etags.push_back(resp.GetEtag());
        part_nums.push_back(part_number);
    }
}

// 拷贝后续分片
...

// 伪代码
// 调用CompleteMultiUpload结束分片拷贝
CompleteMultiUpload(etags, part_nums);
...

###  Copy

#### 功能说明

Copy 请求实现将一个文件从源路径复制到目标路径。通过指定 x-cos-copy-source 来指定源文件，x-cos-copy-source-range 指定字节范围。 内部封装了PutObjectCopy和UploadPartCopyData, 会根据源文件大小选择对应的上传方式。

#### 方法原型

```cpp
CosResult Copy(const CopyReq& req, CopyResp* resp);
```

#### 参数说明

- req   —— CopyReq Copy操作的请求

```
/// 构造函数， 其中
/// bucket_name为要复制的目的Bucket
/// object_name为目标Object
CopyReq(const std::string& bucket_name,
        const std::string& object_name);

/// 源文件 URL 路径，可以通过 versionid 子资源指定历史版本
void SetXCosCopySource(const std::string& str);

/// 当 Object 在指定时间后被修改，则执行操作，否则返回 412。
/// 可与 x-cos-copy-source-If-None-Match 一起使用，与其他条件联合使用返回冲突。
void SetXCosCopySourceIfModifiedSince(const std::string& str);

/// 当 Object 在指定时间后未被修改，则执行操作，否则返回 412。
/// 可与 x-cos-copy-source-If-Match 一起使用，与其他条件联合使用返回冲突。
void SetXCosCopySourceIfUnmodifiedSince(const std::string& str);

/// 当 Object 的 Etag 和给定一致时，则执行操作，否则返回 412。
/// 可与x-cos-copy-source-If-Unmodified-Since 一起使用，与其他条件联合使用返回冲突
void SetXCosCopySourceIfMatch(const std::string& str);

/// 当 Object 的 Etag 和给定不一致时，则执行操作，否则返回 412。
/// 可与 x-cos-copy-source-If-Modified-Since 一起使用，与其他条件联合使用返回冲突。
void SetXCosCopySourceIfNoneMatch(const std::string& str);

/// x-cos-storage-class 设置 Object 的存储级别，枚举值：STANDARD,STANDARD_IA，
/// 默认值：STANDARD（目前仅支持华南园区）
void SetXCosStorageClass(const std::string& storage_class);

/// 定义Object的ACL属性,有效值：private,public-read-write,public-read
/// 默认值：private
void SetXCosAcl(const std::string& str);

/// 赋予被授权者读的权限.格式：x-cos-grant-read: id=" ",id=" ".
/// 当需要给子账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>"
/// 当需要给根账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>"
void SetXCosGrantRead(const std::string& str);

/// 赋予被授权者写的权限,格式：x-cos-grant-write: id=" ",id=" "./
/// 当需要给子账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>",
/// 当需要给根账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>"
void SetXCosGrantWrite(const std::string& str);

/// 赋予被授权者读写权限.格式：x-cos-grant-full-control: id=" ",id=" ".
/// 当需要给子账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<SubUin>",
/// 当需要给根账户授权时,id="qcs::cam::uin/<OwnerUin>:uin/<OwnerUin>"
void SetXCosGrantFullControl(const std::string& str);

/// 允许用户自定义的头部信息,将作为 Object 元数据返回.大小限制2K
void SetXCosMeta(const std::string& key, const std::string& value);
```

- resp   —— CopyResp tCopy操作的返回

```cpp
// 标识返回的结果类型，因为内部可能使用PutObjectCopy或UploadPartCopyData，所以可能有多种返回类型
// 在Copy执行成功后，必须先调用GetRespTag获取Response的类型，可能是PutObjectCopy/CompleteMultiUpload
// @retval "PutObjectCopy"表示使用PutObjectCopy复制成功
//         "Complete"表示使用UploadPartCopy复制成功
std::string GetRespTag();

// RespTag为"PutObjectCopy”时可以调用下列成员函数， "Complete"时调用的返回值无意义
std::string GetEtag() const;
std::string GetLastModified() const;
std::string GetVersionId() const;

// RespTag为"Complete"时可以调用下列成员函数， "Complete"时调用的返回值无意义
std::string GetLocation() const;
std::string GetBucket() const;
std::string GetKey() const;
```

#### 示例

```cpp
qcloud_cos::CosConfig config("./config.json");
qcloud_cos::CosAPI cos(config);

std::string bucket_name = "cpp_sdk_v5-12345";
std::string object_name = "sevenyou";

qcloud_cos::CopyReq req(bucket_name, object_name);
qcloud_cos::CopyResp resp;

req.SetXCosCopySource("sevenyou-54321.cos.ap-beijing.myqcloud.com/sevenyou_copy_test");
qcloud_cos::CosResult result = cos.Copy(req, &resp);

// 调用成功，调用resp的成员函数获取返回内容
if (result.IsSucc()) {
    if (resp.GetRespTag() == "PutObjectCopy") {
        // 调用GetEtag/GetLastModified/GetVersionId
    } else if (resp.GetRespTag() == "Complete") {
        // 调用GetLocation/GetBucket/GetKey
    }
}
...
