# 定义替换映射表
$replacementMap = @{
    'TCM_syndromes_score' = 'indicator1'
    'VAS_score'          = 'indicator2'
    'WOMAC_score'        = 'indicator3'
    'Lysholm_score'      = 'indicator4'
}

# 遍历仓库中的所有.py文件
Get-ChildItem -Recurse -Filter *.py | ForEach-Object {
    $filePath = $_.FullName
    
    # 读取文件内容（UTF-8编码处理）
    $content = [System.IO.File]::ReadAllText($filePath, [System.Text.Encoding]::UTF8)
    
    # 执行顺序替换
    $replacementMap.GetEnumerator() | Sort-Object Key -Descending | ForEach-Object {
        $content = $content.Replace($_.Key, $_.Value)
    }
    
    # 写回文件（保留原始编码）
    [System.IO.File]::WriteAllText($filePath, $content, [System.Text.Encoding]::UTF8)
    
    Write-Host "Processed: $filePath"
}