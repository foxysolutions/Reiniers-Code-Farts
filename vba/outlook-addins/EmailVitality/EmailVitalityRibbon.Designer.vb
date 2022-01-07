Partial Class EmailVitalityRibbon
    Inherits Microsoft.Office.Tools.Ribbon.RibbonBase

    <System.Diagnostics.DebuggerNonUserCode()> _
    Public Sub New(ByVal container As System.ComponentModel.IContainer)
        MyClass.New()

        'Required for Windows.Forms Class Composition Designer support
        If (container IsNot Nothing) Then
            container.Add(Me)
        End If

    End Sub

    <System.Diagnostics.DebuggerNonUserCode()> _
    Public Sub New()
        MyBase.New(Globals.Factory.GetRibbonFactory())
        'This call is required by the Component Designer.
        InitializeComponent()

    End Sub

    'Component overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Required by the Component Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Component Designer
    'It can be modified using the Component Designer.
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Me.EmailVitalityTab = Me.Factory.CreateRibbonTab
        Me.WorkHoursGroup = Me.Factory.CreateRibbonGroup
        Me.WorkHoursStart = Me.Factory.CreateRibbonEditBox
        Me.WorkHoursEnd = Me.Factory.CreateRibbonEditBox
        Me.ShowPrompt = Me.Factory.CreateRibbonCheckBox
        Me.EmailVitalityTab.SuspendLayout()
        Me.WorkHoursGroup.SuspendLayout()
        Me.SuspendLayout()
        '
        'EmailVitalityTab
        '
        Me.EmailVitalityTab.ControlId.ControlIdType = Microsoft.Office.Tools.Ribbon.RibbonControlIdType.Office
        Me.EmailVitalityTab.ControlId.OfficeId = "TabNewMailMessage"
        Me.EmailVitalityTab.Groups.Add(Me.WorkHoursGroup)
        Me.EmailVitalityTab.Label = "TabNewMailMessage"
        Me.EmailVitalityTab.Name = "EmailVitalityTab"
        '
        'WorkHoursGroup
        '
        Me.WorkHoursGroup.Items.Add(Me.WorkHoursStart)
        Me.WorkHoursGroup.Items.Add(Me.WorkHoursEnd)
        Me.WorkHoursGroup.Items.Add(Me.ShowPrompt)
        Me.WorkHoursGroup.Label = "Email Vitality Working hours"
        Me.WorkHoursGroup.Name = "WorkHoursGroup"
        '
        'WorkHoursStart
        '
        Me.WorkHoursStart.Label = "Start"
        Me.WorkHoursStart.MaxLength = 8
        Me.WorkHoursStart.Name = "WorkHoursStart"
        Me.WorkHoursStart.ScreenTip = "hh:mm:ss"
        Me.WorkHoursStart.Text = Global.EmailVitality.MySettings.Default.WorkHoursStart
        '
        'WorkHoursEnd
        '
        Me.WorkHoursEnd.Label = "End"
        Me.WorkHoursEnd.MaxLength = 8
        Me.WorkHoursEnd.Name = "WorkHoursEnd"
        Me.WorkHoursEnd.ScreenTip = "hh:mm:ss"
        Me.WorkHoursEnd.Text = Global.EmailVitality.MySettings.Default.WorkHoursEnd
        '
        'ShowPrompt
        '
        Me.ShowPrompt.Checked = Global.EmailVitality.MySettings.Default.ShowPrompt
        Me.ShowPrompt.Label = "ShowPrompt"
        Me.ShowPrompt.Name = "ShowPrompt"
        Me.ShowPrompt.ScreenTip = "Always ask whether or not to delay an email send outside working hours."
        Me.ShowPrompt.SuperTip = "When deselected each email which is send after Workinghours will automatically be" &
    " scheduled for the start of the next workday."
        '
        'EmailVitalityRibbon
        '
        Me.Name = "EmailVitalityRibbon"
        Me.RibbonType = "Microsoft.Outlook.Mail.Compose"
        Me.Tabs.Add(Me.EmailVitalityTab)
        Me.EmailVitalityTab.ResumeLayout(False)
        Me.EmailVitalityTab.PerformLayout()
        Me.WorkHoursGroup.ResumeLayout(False)
        Me.WorkHoursGroup.PerformLayout()
        Me.ResumeLayout(False)

    End Sub

    Friend WithEvents EmailVitalityTab As Microsoft.Office.Tools.Ribbon.RibbonTab
    Friend WithEvents WorkHoursGroup As Microsoft.Office.Tools.Ribbon.RibbonGroup
    Friend WithEvents WorkHoursStart As Microsoft.Office.Tools.Ribbon.RibbonEditBox
    Friend WithEvents WorkHoursEnd As Microsoft.Office.Tools.Ribbon.RibbonEditBox
    Friend WithEvents ShowPrompt As Microsoft.Office.Tools.Ribbon.RibbonCheckBox
End Class

Partial Class ThisRibbonCollection

    <System.Diagnostics.DebuggerNonUserCode()>
    Friend ReadOnly Property EmailVitalityRibbon() As EmailVitalityRibbon
        Get
            Return Me.GetRibbon(Of EmailVitalityRibbon)()
        End Get
    End Property
End Class
