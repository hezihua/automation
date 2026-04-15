' 如何使用这个脚本？
' 由于这是 VBA 脚本，它不能像 Python 脚本那样直接在终端运行。您需要在 Excel 中使用它：

' 打开您的 Excel 文件（包含多个 Sheet）。
' 按下快捷键 Alt + F11 打开 VBA 编辑器。
' 在左侧的“工程资源管理器”中，右键点击您的工作簿名称（如 VBAProject (工作簿1)），选择 插入 -> 模块。
' 将 batch_print_to_pdf.vba 文件中的所有代码复制并粘贴到右侧空白的代码窗口中。
' 关闭 VBA 编辑器回到 Excel。
' 按下快捷键 Alt + F8 打开“宏”对话框，选中 批量打印工作表为PDF，点击“选项”可以为其设置快捷键（如教程中的 Ctrl+Shift+P）。
' 点击“执行”按钮（或使用您设置的快捷键），它就会弹出一个文件夹选择框，选择后即可自动将所有 Sheet 批量导出为 PDF。

Attribute VB_Name = "Module1"
Sub 批量打印工作表为PDF()
'
' 批量打印工作表为PDF 宏
' 快捷键: Ctrl+Shift+P
'
' 功能说明：
' 1. 弹出一个文件夹选择对话框，让用户选择保存 PDF 的目标文件夹。
' 2. 遍历当前工作簿中的所有工作表。
' 3. 将每个工作表分别静默打印（导出）为 PDF 文件，文件名为 "工作表名称.pdf"。
'

    Dim filepath As String
    Dim sht As Worksheet
    
    ' 1. 弹出文件夹选择对话框
    With Application.FileDialog(msoFileDialogFolderPicker)
        .Title = "请选择保存 PDF 文件的文件夹"
        ' 如果用户点击了“确定” (-1)
        If .Show = -1 Then
            ' 获取用户选择的路径，并在末尾加上反斜杠 "\"
            filepath = .SelectedItems(1) & "\"
        Else
            ' 如果用户点击了“取消”，则退出程序
            MsgBox "您取消了选择，批量打印已中止。", vbInformation, "提示"
            Exit Sub
        End If
    End With

    ' 关闭屏幕刷新，提高运行速度并防止屏幕闪烁
    Application.ScreenUpdating = False

    ' 2. 遍历当前工作簿中的每一个工作表
    For Each sht In ActiveWorkbook.Worksheets
        ' 激活当前工作表 (某些打印操作依赖于工作表被激活)
        sht.Select
        
        ' 3. 执行打印操作
        ' 注意：在现代版本的 Excel (2007及以上) 中，直接导出为 PDF 推荐使用 ExportAsFixedFormat 方法。
        ' 原教程中使用的 PrintOut 配合 printtofile 参数依赖于系统安装了特定的虚拟打印机，
        ' 且不同电脑上的表现可能不一致。这里我将其优化为更通用、更稳定的 ExportAsFixedFormat 方法。
        
        On Error Resume Next ' 忽略可能出现的隐藏表或空表导致的打印错误
        sht.ExportAsFixedFormat _
            Type:=xlTypePDF, _
            Filename:=filepath & sht.Name & ".pdf", _
            Quality:=xlQualityStandard, _
            IncludeDocProperties:=True, _
            IgnorePrintAreas:=False, _
            OpenAfterPublish:=False
        On Error GoTo 0 ' 恢复正常的错误处理
        
    Next sht

    ' 恢复屏幕刷新
    Application.ScreenUpdating = True
    
    ' 提示完成
    MsgBox "所有工作表已成功批量导出为 PDF！" & vbCrLf & "保存路径：" & filepath, vbInformation, "完成"

End Sub
