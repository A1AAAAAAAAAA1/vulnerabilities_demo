### CDN绕过方法

- 方法一：PingPingPing

  不同地区对应着不同的CDN中心，所以使用不同站点的ping服务可分配到不同的CDN。这很简单，使用各种多站点ping服务来检查对应的IP地址是否唯一。如果不是唯一的，则使用大多数 CDN。多站Ping网站为：

  http://ping.chinaz.com/http://ping.aizhan.com/http://tools.ipip.net/ping.php（强烈推荐这个，这个默认多站ping，真的很多）

- 方法二：nslookup

  使用 nslookup 进行检测，原理同上，如果返回域名解析对应多个 IP 地址多半是使用了 CDN。

- 方法三：工具

  [CDN Finder](https://www.cdnplanet.com/tools/cdnfinder/)

### 方法一：查询DNS解析记录

1.查看IP与域名绑定的历史记录。使用 CDN 之前可能有记录。相关查询网站为：

[Dnsdb](https://dnsdb.io/zh-cn/)

[微步在线](https://x.threatbook.cn/)

[Netcraft](https://sitereport.netcraft.com/)

[IPIP](https://tools.ipip.net/cdn.php)（没错又是这个网站，它太猛了）

2.借助Securitytrails平台（https://securitytrails.com/）

攻击者可以查明真实的原始IP。他们只需在搜索字段中输入站点域名并按 ENTER，即可在左侧菜单中找到“历史数据”。

如何找到隐藏在 CloudFlare 或 Tor 背后的真实原始 IP？

除了过去的 DNS 记录，即使是当前的记录也可能泄露原始服务器 IP。例如，MX 记录是查找 IP 的常用方法。如果网站在与 Web 相同的服务器和 IP 上托管自己的邮件服务器，则原始服务器 IP 将在 MX 记录中。

### 方法二：查询子域名

毕竟CDN还是不便宜，所以很多站长可能只会在主站或者流量大的子站做一个CDN，而很多小站子站跟主站在同一个服务器或者同C段，此时可以通过子域对应的IP查询，帮助找到真实IP站点。

> [微步在线](https://x.threatbook.cn/)
>
> 上面提到的微步在线功能强大，黑客只需输入域名即可查找（如baidu.com），点击子域选项即可找到其子域，但免费用户每月只有5次免费查询机会。
>
> [Dnsdb](https://dnsdb.io/zh-cn/)
>
> 黑客只需要输入baidu.com TYPE:A就可以收集到百度的子域名和IP。
>
> [Google](https://www.google.com/)
>
> 谷歌站点：baidu.com-www 可以看到除WWW以外的子域
>
> **子域扫描器**
>
> Layer子域名挖掘机和lijiejie的subdomain那个工具都很不错
>
> 推荐长亭的xray

### 方法三：网络空间引擎

fofa、鹰图、Zoomeye、shodan、360

推荐鹰图

只需输入：title:“网站的title关键字”或者body：“网站的body特征”就可以找出收录的有这些关键字的ip域名，很多时候能获取网站的真实ip

### 方法四：使用SSL证书寻找真实原IP

如果您在 xyz123boot.com 上托管服务，则原始服务器 IP 为 136.23.63.44。CloudFlare 将为您提供 DDoS 防护、Web 应用防火墙和其他一些[安全](https://www.webshell.cc/tag/security)服务，以保护您的服务免受攻击。为此，您的 Web 服务器必须支持 SSL 并具有证书。此时，CloudFlare 与您的服务器之间的通信，就像您与 CloudFlare 之间的通信一样，将被加密（即没有灵活的 SSL）。这看起来很安全，但问题是当你直接连接到443端口（[https://136.23.63.44:443](https://136.23.63.44/)）上的IP时，会暴露SSL证书。

此时，如果攻击者扫描0.0.0.0/0，整个互联网，就可以在xyz123boot.com的443端口获取有效证书，进而获取提供给你的web服务器IP。

目前，Censys 工具可以扫描整个互联网。Censys 是用于搜索联网设备信息的新搜索引擎。安全专家可以使用它来评估其实施的安全性，黑客可以使用它作为初步调查。攻击目标和收集目标信息的强大武器。Censys 搜索引擎可以扫描整个互联网。Censys每天扫描IPv4地址空间，搜索所有联网设备并收集相关信息，并返回资源（如设备、网站、证书等）配置和部署的整体报告。

攻击者唯一需要做的就是将上述搜索词转换为实际的搜索查询参数。

xyz123boot.com证书的搜索查询参数为：parsed.names: xyz123boot.com

只显示有效证书的查询参数为：tags.raw:trusted

攻击者可以在 Censys 上实现多个参数的组合，这可以通过使用简单的布尔逻辑来完成。

组合的搜索参数是：parsed.names：xyz123boot.com 和 tags.raw：trusted

![CDN_bypass_summary_censys_1.png](https://image.3001.net/images/20220506/1651826886_6274e0c620ad9fc29fd6e.png!small)

Censys 将向您显示在扫描中找到的符合上述搜索条件的所有标准证书。

要一一查看这些搜索结果，攻击者可以通过单击右侧的“探索”来打开一个包含多个工具的下拉菜单。什么在使用这个证书？> IPv4 主机

![CDN_bypass_summary_censys_2.png](https://image.3001.net/images/20220506/1651826887_6274e0c743d3461e7b287.png!small)

使用给定的 SSL 证书

如果您是执法人员，并且想找到隐藏在 cheesecp5vaogohv.onion 下的儿童色情网站。最好的办法是找到它的原始IP，这样就可以追踪它的托管服务器，甚至可以找出它背后的运营商和财务线索。

隐藏服务具有 SSL 证书。要查找它使用的 IPv4 主机，只需将“SHA1 指纹”（签名证书的 sha1 值）粘贴到 Censys IPv4 主机搜索中即可找到证书。这种方法很容易找到配置错误的Web服务器。

### 方法五：使用HTTP头找到真正的原始IP

借助 SecurityTrails 这样的平台，任何人都可以在海量的大数据中搜索自己的目标，甚至可以通过比较 HTTP 标头找到原始服务器。

特别是当用户有一个非常特殊的服务器名称和软件名称时，攻击者更容易找到你。

如果要搜索的数据很多，如上所述，攻击者可以在 Censys 上组合搜索参数。假设您正在与 1500 个 Web 服务器共享您的服务器 HTTP 标头，所有这些服务器都发送相同的标头参数和值组合。而且您还使用新的 PHP 框架来发送唯一的 HTTP 标头（例如：X-Generated-Via: XYZ 框架），目前约有 400 位网站管理员使用该框架。最终，在三台服务器的交汇处，通过人工操作即可找到IP，整个过程仅需几秒。

例如，Censys上用于匹配服务器头的搜索参数为80.http.get.headers.server:，查找CloudFlare服务的网站的参数如下：

80.http.get.headers.server:cloudflare

### 方法六：利用网站返回的内容寻找真实的原IP

如果原服务器IP也返回网站内容，可以在网上搜索很多相关资料。

浏览网站源代码以查找独特的代码片段。在 JavaScript 中使用具有访问权限或标识符参数的第三方服务（例如 Google Analytics、reCAPTCHA）是攻击者经常使用的一种方法。

以下是从 HackTheBox 网站获得的 Google Analytics 跟踪代码示例：

ga('创建','UA-93577176-1','auto');80.http.get.body 可以使用：参数通过body/source过滤Censys数据。不幸的是，普通搜索字段有局限性。但是您可以在 Censys 请求研究访问权限，这使您可以通过 Google BigQuery 进行更强大的查询。

Shodan 是一个类似于 Censys 的服务，同样提供 http.html 搜索参数。

搜索示例：https://www.shodan.io/search?query=http.html%3AUA-32023260-1

![CDN_bypass_summary_censys_3.png](https://image.3001.net/images/20220506/1651826890_6274e0cacb2ee488a94a0.png!small)

### 方法七：使用外地主机解析域名

国内很多CDN厂商因为各种原因只做国内线，国外线路可能几乎没有。这时候我们可能会使用外地主机直接访问真实IP。

### 方法八：网站漏洞搜索

1. 目标敏感文件泄露，如phpinfo、GitHub信息泄露等探针
2. XSS盲打、命令执行反向shell、SSRF等
3. 无论是社会工程还是其他手段，目标网站获取CDN中的管理员账号，在CDN的配置中可以找到网站的真实IP。

### 方法九：网站邮件订阅搜索

RSS邮件订阅，很多网站都有自己的sendmail，会发邮件给我们。此时，服务器的真实IP将包含在邮件的源代码中。

### 方法十：用Zmap扫描全网

要找到xiaix.me网站的真实IP，我们首先从apnic获取IP段，然后使用Zmap的banner-grab扫描出开放80端口的主机进行banner抓包，最后在Host中写入xiaix.me http请求。

### 方法十一：F5 LTM解码方法

服务器使用F5 LTM进行负载均衡时，也可以通过set-cookie关键字解码得到真实ip，例如：Set-Cookie: BIGipServerpool_8.29_8030=487098378.24095.0000，第一个小数部分的十进制数是487098378取出来，然后转换成十六进制数1d08880a，然后从后往前，取出四位数字，就是0a.88.08.1d，最后再转换成十进制数10.136.8.29，也是最后一个真实IP。

### 方法十二：网页敏感信息

这条思路来源于Jacko

#### favicon哈希值

根据网站图标哈希值搜索IP

python2脚本

```
import mmh3
import requests
response = requests.get('https://example.com/favicon.ico')
favicon = response.content.encode('base64')
hash = mmh3.hash(favicon)
print 'http.favicon.hash:'+str(hash)
```

去fofa或者shodan上搜索该哈希值

查询格式：

- fofa：`icon_hash="xxx"`
- shodan：`http.favicon.hash:xxx`

#### HTML源代码检索查找IP

根据网站页面HTML中特有的字符串去搜索引擎中搜索，如目标页面中由HTML标签为`<title>`的字段比较特殊，那么可以去FOFA中搜索：

```
title="xxxxxxxxxxxxxxx"
```

搜索到的结果会显示IP，访问该IP，若能够正常访问则为真正IP，如果打不开则为CDN或虚拟主机服务器