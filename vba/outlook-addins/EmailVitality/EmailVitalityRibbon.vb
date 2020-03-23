Imports System.Text.RegularExpressions
Imports Microsoft.Office.Tools.Ribbon

Public Class EmailVitalityRibbon

    Public Function ValidateTime(ByVal strTime As String) As Boolean
        ' Check whether not empty
        If Not String.IsNullOrEmpty(strTime) Then
            ' Setup Regex (Regular Expression)
            Dim strTimePattern As String = "^\d{2}:\d{2}:\d{2}$"
            Dim rePhone As New Regex(strTimePattern)

            Return rePhone.IsMatch(strTime) 'Check Validity
        Else
            Return False 'Empty, thus not valid
        End If
    End Function

    Private Sub WorkHoursStart_TextChanged(sender As Object, e As RibbonControlEventArgs) Handles WorkHoursStart.TextChanged
        If Not ValidateTime(WorkHoursStart.Text) Then
            MsgBox("Invalid input provided " & WorkHoursStart.Text & ". Reset to: 08:30:00.")
            WorkHoursStart.Text = "08:30:00"
        Else
            ' When valid new input, update Application Setting
            My.Settings.WorkHoursStart = WorkHoursStart.Text
            My.Settings.Save() 'Save updated settings to ensure consistency after re-opening Application
        End If
    End Sub

    Private Sub WorkHoursEnd_TextChanged(sender As Object, e As RibbonControlEventArgs) Handles WorkHoursEnd.TextChanged
        If Not ValidateTime(WorkHoursEnd.Text) Then
            MsgBox("Invalid input provided " & WorkHoursEnd.Text & ". Reset to: 17:00:00.")
            WorkHoursEnd.Text = "17:00:00"
        Else
            ' When valid new input, update Application Setting
            My.Settings.WorkHoursEnd = WorkHoursEnd.Text
            My.Settings.Save() 'Save updated settings to ensure consistency after re-opening Application
        End If
    End Sub

    Private Sub ShowPrompt_Click(sender As Object, e As RibbonControlEventArgs) Handles ShowPrompt.Click
        My.Settings.ShowPrompt = ShowPrompt.Checked
        My.Settings.Save() 'Save updated settings to ensure consistency after re-opening Application
    End Sub
End Class
