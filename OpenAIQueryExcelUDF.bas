Attribute VB_Name = "Module1"
Declare PtrSafe Function GetEnvironmentVariable Lib "kernel32" Alias "GetEnvironmentVariableA" (ByVal lpName As String, ByVal lpBuffer As String, ByVal nSize As Long) As Long

Function GetEnvVar(varName As String) As String
    Dim buffer As String
    Dim length As Long
    
    buffer = String$(255, Chr$(0))
    length = GetEnvironmentVariable(varName, buffer, Len(buffer))
    
    If length > 0 Then
        GetEnvVar = Left$(buffer, length)
    Else
        GetEnvVar = ""
    End If
End Function

Function OpenAIQuery(prompt As String, cellRef As Range) As String

    ' Set a reference to the helperCell as the cell to the right of the calling cell
    Dim helperCell As Range
    Set helperCell = Application.Caller.Offset(0, 1)
    
    ' If the helper cell is not empty, return its value
    If Not IsEmpty(helperCell.Value) Then
        OpenAIQuery = helperCell.Value
        Exit Function
    End If
    
    Dim objHTTP As Object
    Set objHTTP = CreateObject("MSXML2.ServerXMLHTTP")
    
    Dim apiKey As String
    Dim url As String
    Dim body As String
    Dim result As String
    
    ' Get API key from environment variable
    apiKey = GetEnvVar("OPENAI_API_KEY")
    
    ' URL for OpenAI API
    url = "https://api.openai.com/v1/chat/completions"
    
    ' Prepare the JSON body
    body = "{""model"":""gpt-3.5-turbo"","
    body = body & """messages"":["
    body = body & "{""role"": ""system"", ""content"": ""You are a helpful multilingual AI assistant. Your answers are as short as possible. Even shorter. 1 word if you can.""},"
    body = body & "{""role"": ""user"", ""content"": """ & prompt & " " & cellRef.Value & """}"
    body = body & "]}"
    
    ' Send the request
    With objHTTP
        .Open "POST", url, False
        .setRequestHeader "Content-Type", "application/json"
        .setRequestHeader "Authorization", "Bearer " & apiKey
        .send body
        result = .responseText
    End With
    
    ' Manually parse the JSON response to extract the message content
    Dim startPos As Integer
    Dim endPos As Integer
    
    startPos = InStr(result, """content"": """) + 12
    result = Mid(result, startPos)
    endPos = InStr(result, """") - 1
    result = Mid(result, 1, endPos)
    
    ' Save the API response to the helper cell
    helperCell.Parent.Evaluate "CopyOver(" & """" & result & """" & "," & helperCell.Address(False, False) & ")"
    
    ' Return the assistant's reply
    OpenAIQuery = result
End Function

Private Sub CopyOver(result As String, helperCell As Range)
    helperCell.Value = result
End Sub

