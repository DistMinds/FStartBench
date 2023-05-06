'use strict';

const express = require('express');
//引入POST参数解析
var bodyParser = require('body-parser');

// Constants
const PORT = 9000;
const HOST = '0.0.0.0';

// Web function invocation
const app = express();

//开放统一资源
app.use('/public/', express.static('./public/'));

//============================================
// Express框架，配置使用 art-template 模板引擎
// 第一个参数，表示，当渲染以 .art 结尾的文件的时候，使用 art-template 模板引擎
// express-art-template 是专门用来在 Express 中把 art-template 整合到 Express 中
// 虽然外面这里不需要记载 art-template 但是也必须安装
// 原因就在于 express-art-template 依赖了 art-template
app.engine('html', require('express-art-template'));
//============================================

//============================================
// 配置 body-parser 中间件（插件，专门用来解析表单 POST 请求体）
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())
//============================================



app.get('/', (req, res) => {
    //使用Express自带的方法(其中对art-template进行了封装)
    //第一个参数默认是从 views 文件下开始查找
    // 如果想要修改默认的 views 目录，则可以
    // 通过使用app.set('views', render函数的默认路径)
    res.render('index.html', {
      comments: comments
  })
});

app.get('/post',function (req, res) {
  res.render('post.html');
})
app.post('/post',function (req, res) {
  var comment=req.body;
  comments.dateTime=getNowTime();
  comments.unshift(comment);
  //Express中封装的重定向方法
  res.redirect('/');
})

//模拟数据
var comments = [
  {
      name: '张三',
      message: '今天天气不错！',
      dateTime: '2018-08-06  08:20:56'
  },
  {
      name: '张三2',
      message: '今天天气不错！',
      dateTime: '2018-08-06  08:20:56'
  },
  {
      name: '张三3',
      message: '今天天气不错！',
      dateTime: '2018-08-06  08:20:56'
  },
  {
      name: '张三4',
      message: '今天天气不错！',
      dateTime: '2018-08-06  08:20:56'
  },
  {
      name: '张三5',
      message: '今天天气不错！',
      dateTime: '2018-08-06  08:20:56'
  }
]



//获取当前时间的方法
function getNowTime() {
  var date = new Date();
  var year = date.getFullYear();
  var month = date.getMonth() + 1;
  var day = date.getDate();
  var hour = date.getHours();
  var minute = date.getMinutes();
  var second = date.getSeconds();
  return (year + '-' + month + '-' + day + '  '
      + (hour > 9 ? hour : '0' + hour) + ':'
      + (minute > 9 ? minute : '0' + minute)
      + ':' + (second > 9 ? second : '0' + second)).toString();
}


var server = app.listen(PORT, HOST);
console.log(`SCF Running on http://${HOST}:${PORT}`);

server.timeout = 0; // never timeout
server.keepAliveTimeout = 0; // keepalive, never timeout