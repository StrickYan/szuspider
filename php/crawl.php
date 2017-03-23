<?php

$ch = curl_init(); // 初始化一个 cURL 对象
curl_setopt($ch, CURLOPT_URL, 'http://www.szu.edu.cn/board/');// 设置需要抓取的URL
curl_setopt($ch, CURLOPT_HEADER, 1);// 设置header
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);// 设置cURL 参数，要求结果保存到字符串中还是输出到屏幕上。
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
//curl_setopt($ch, CURLOPT_SSLVERSION, 3); // Force SSLv3 to fix Unknown SSL Protocol error  
// 设置代理服务器
//curl_setopt($ch, CURLOPT_HTTPPROXYTUNNEL, 1);
curl_setopt($ch, CURLOPT_PROXY, 'http://proxy.szu.edu.cn:8080');
curl_setopt($ch, CURLOPT_PROXYUSERPWD, '123836:074536');

// 运行cURL，请求网页
if(! $data = curl_exec($ch))
{
    var_dump(curl_error($ch));
}

// 关闭URL请求
curl_close($ch);

// 显示获得的数据
var_dump($data);
//var_dump(curl_version());

