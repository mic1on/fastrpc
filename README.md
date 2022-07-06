# FastAPI RPC

这是一个基于 FastAPI 的 浏览器 RPC 服务端。
> 此浏览器可以是任何端(pc/手机/平板)的任意浏览器

它提供了一个WS服务和一个HTTP服务。WS服务负责浏览器群和服务端的通信；HTTP服务负责提供一个HTTP接口，用户通过调用接口实现调用远程浏览器群的方法。

此项目主要思路来自于 [sekiro](https://github.com/virjar/sekiro)。项目的初衷是学习并分享学习成果，请勿用于非法用途。

### 作用

当你苦于网站层层加密无法解密时，当你遇到诸如动态cookie加密时，你可以考虑使用此项目，这是解决方案之一。

### 使用

1. 首先你需要确保成功运行python主程序`main.py`
2. 将提供给你的`client.js`注入到浏览器中。注入方式作者用的是油猴。
3. 将浏览器打开任意网站，比如百度。（这时候油猴脚本是将client.js注入到页面里的）
4. 此时，你可以在电脑终端中执行：
> curl http://localhost:8000/do/cookies

你将在终端看到你访问百度留下的cookies

![](https://miclon-job.oss-cn-hangzhou.aliyuncs.com/img/20220705232431.png)

以上就是一次项目的初体验，如果以上步骤非常顺利，那么你可以继续向下看。

### 新增功能

刚刚看到了，我们在API接口调用了/do/cookies，那是因为我们在`client.js`中注册了此方法名称。
```javascript
client.registerAction("cookies",function(request, resolve,reject ){
        resolve(document.cookie);
})
```
所以，顺理成章地，我们可以自定义其他任意操作，比如：
```javascript
client.registerAction("html",function(request, resolve,reject ){
        resolve(document.documentElement.outerHTML);
})
```
随后，我们调用：
> curl http://localhost:8000/do/html -o baidu.txt

ps: -o 输出到文件baidu.txt
![](https://miclon-job.oss-cn-hangzhou.aliyuncs.com/img/20220705234115.png)

### 举例应用场景

##### 某网站登录

其网站登录的时候密码是加密的。
![](https://miclon-job.oss-cn-hangzhou.aliyuncs.com/img/20220705234828.png)

尝试找到调用处。
![](https://miclon-job.oss-cn-hangzhou.aliyuncs.com/img/20220705234952.png)

这里就是它的加密方法。
```javascript
encryptedString(key_to_encode, that.password.val())
```

以往的方式，我们需要进入这个方法，抠出它的实现过程。要么还原要么node调用执行。

现在，不需要这些，直接复制这个加密。

```javascript
client.registerAction("mm",function(request, resolve,reject ){
        resolve(encryptedString(key_to_encode, "qq1234"));
})
```
调用：

> curl http://localhost:8000/do/mm

得到加密结果：
![](https://miclon-job.oss-cn-hangzhou.aliyuncs.com/img/20220705235309.png)


### 更多场景
……