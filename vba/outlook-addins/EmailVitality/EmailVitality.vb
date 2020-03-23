Imports Microsoft.Office.Interop.Outlook

Public Class EmailVitality

    Private Sub Application_ItemSend(Item As Object, ByRef Cancel As Boolean) Handles Application.ItemSend
        Dim objMail As MailItem

        If TypeOf Item Is MailItem Then
            objMail = Item

            ' Fetch user input from Ribbon (Start and End times of WorkingDay & to always postpone delivery)
            Dim WorkingDayStart As String = My.Settings.WorkHoursStart
            Dim WorkingDayEnd As String = My.Settings.WorkHoursEnd
            Dim bShowPrompt As Boolean = My.Settings.ShowPrompt

            Dim today As Date = Date.Now().Date
            Dim bDelayMail As Boolean = True
            Dim NewSendTime As String
            Dim nPrompt As Integer

            Select Case Weekday(today, vbMonday)
                Case 6 'Saturday - Delay 2 days
                    NewSendTime = CombineDateTime(today.AddDays(2), WorkingDayStart)
                Case 7 'Sunday - Delay 1 day
                    NewSendTime = CombineDateTime(today.AddDays(1), WorkingDayStart)
                Case Else 'WeekDay - Only Delay when outside WorkingHours
                    If Now < CombineDateTime(today, WorkingDayStart) Then 'Before WorkingDay
                        NewSendTime = CombineDateTime(today, WorkingDayStart)
                    ElseIf Now > CombineDateTime(today, WorkingDayEnd) Then 'After WorkingDay
                        'Set NewSendTime based on Weekday
                        Select Case Weekday(today, vbMonday)
                            Case 5 'Friday - Delay 3 days
                                NewSendTime = CombineDateTime(today.AddDays(3), WorkingDayStart)
                            Case Else 'Else - Delay till tomorrow morning
                                NewSendTime = CombineDateTime(today.AddDays(1), WorkingDayStart)
                        End Select
                    Else
                        bDelayMail = False
                    End If
            End Select

            'When email should be delayed (NOW is after Business Hours) & Email is not yet delayed
            If bDelayMail = True And objMail.DeferredDeliveryTime = "1/1/4501" Then
                Dim NewDateTime As Date = NewSendTime
                If bShowPrompt = True Then
                    'Ask if to delay sending this email
                    nPrompt = MsgBox("Uh-oh.. it's outside Working Hours:" & vbCrLf & vbCrLf & "Click YES to DELAY (" & WeekdayName(Weekday(NewDateTime, vbMonday), True, vbMonday) & " " & NewSendTime & ")." & vbCrLf & vbCrLf & "Click NO to SEND NOW, when:" & vbCrLf & "- Email is so urgent, colleagues MUST read it now." & vbCrLf & "- You expect a reply BEFORE start of next Working Hours." & vbCrLf & vbCrLf & "Click CANCEL to not send at all.", vbYesNoCancel + vbCritical, "Delay Email")

                    If nPrompt = vbYes Then 'Delay email
                        objMail.DeferredDeliveryTime = NewSendTime
                    ElseIf nPrompt = vbNo Then 'Send directly
                        objMail.DeferredDeliveryTime = "1/1/4501"
                    Else 'Send Operation Cancelled
                        Cancel = True
                    End If
                Else
                    ' Skip prompt and automatically set the NewSendDtime
                    objMail.DeferredDeliveryTime = NewSendTime
                    MsgBox("Email rescheduled to be delivered at " & WeekdayName(Weekday(NewDateTime, vbMonday), True, vbMonday) & " " & NewSendTime)
                End If
            End If
        End If
    End Sub

    Private Function CombineDateTime(DateString As String, TimeString As String)
        CombineDateTime = DateString & " " & TimeString
    End Function

End Class
