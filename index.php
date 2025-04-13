<?php
// 设置目录
$dir = './';

// 获取文件列表
$files = scandir($dir);

echo "<h2>文件列表</h2>";
echo "<ul>";
foreach($files as $file) {
    if($file != '.' && $file != '..') {
        echo "<li><a href='{$file}'>{$file}</a></li>";
    }
}
echo "</ul>";