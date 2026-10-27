$docxPath = 'C:\Project Sem 5\Maharajas_Kitchen_Project_Report.docx'
$pdfPath = 'C:\Project Sem 5\Maharajas_Kitchen_Project_Report.pdf'

Write-Host "Converting Word document to PDF using Microsoft Word..."
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = [Microsoft.Office.Interop.Word.WdAlertLevel]::wdAlertsNone
    $doc = $word.Documents.Open($docxPath)
    $doc.ExportAsFixedFormat($pdfPath, 17) # 17 = wdExportFormatPDF
    $doc.Close($false)
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
    Write-Host "SUCCESS: PDF created at $pdfPath"
} catch {
    Write-Host "Error: $_"
}
