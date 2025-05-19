import wx

class LoginFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(300, 200))

        self.panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Elementos de Login
        wx.StaticText(self.panel, label="Usuario:")
        self.username_ctrl = wx.TextCtrl(self.panel)
        wx.StaticText(self.panel, label="Contraseña:")
        self.password_ctrl = wx.TextCtrl(self.panel, style=wx.TE_PASSWORD)
        login_button = wx.Button(self.panel, label="Iniciar Sesión")
        login_button.Bind(wx.EVT_BUTTON, self.OnLogin)

        vbox.Add(wx.StaticText(self.panel, label=""), proportion=1, flag=wx.EXPAND) # Espacio
        vbox.Add(wx.StaticText(self.panel, label="Acceso al Sistema"), flag=wx.ALIGN_CENTER)
        vbox.Add(wx.StaticText(self.panel, label=""), proportion=1, flag=wx.EXPAND) # Espacio
        vbox.Add(wx.StaticText(self.panel, label="Usuario:"), flag=wx.LEFT | wx.RIGHT | wx.TOP, border=5)
        vbox.Add(self.username_ctrl, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)
        vbox.Add(wx.StaticText(self.panel, label="Contraseña:"), flag=wx.LEFT | wx.RIGHT | wx.TOP, border=5)
        vbox.Add(self.password_ctrl, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)
        vbox.Add(login_button, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        vbox.Add(wx.StaticText(self.panel, label=""), proportion=1, flag=wx.EXPAND) # Espacio

        self.panel.SetSizer(vbox)
        self.Centre()
        self.Show()
        self.main_app_frame = None # Para la ventana principal después del login

    def OnLogin(self, event):
        username = self.username_ctrl.GetValue()
        password = self.password_ctrl.GetValue()

        #Cambiar por el mecanismo de validación con cifrado y obtención de datos desde la BD
        if username == "admin" and password == "admin":
            wx.MessageBox("Inicio de sesión exitoso", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.main_app_frame = MainAppFrame(None, "Aplicación Bancaria")
            self.Close()
        else:
            wx.MessageBox("Credenciales incorrectas", "Error", wx.OK | wx.ICON_ERROR)

class UserInfoPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        wx.StaticText(self, label="Información de Usuarios")
        # Aquí irían los controles para mostrar la información de los usuarios
        # Por ejemplo, una lista o una tabla.
        self.user_list = wx.ListCtrl(self, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.user_list.InsertColumn(0, 'ID', width=50)
        self.user_list.InsertColumn(1, 'Nombre', width=150)
        self.user_list.InsertColumn(2, 'Email', width=200)

        # Datos de ejemplo
        self.user_list.InsertItem(0, '1')
        self.user_list.SetItem(0, 1, 'Ricardo Aguilar')
        self.user_list.SetItem(0, 2, 'ricardo.aguilar@email.com')
        self.user_list.InsertItem(1, '2')
        self.user_list.SetItem(1, 1, 'Uriel Erandi')
        self.user_list.SetItem(1, 2, 'u.erandi@email.com')
        self.user_list.InsertItem(1, '3')
        self.user_list.SetItem(1, 1, 'Luz Ojeda')
        self.user_list.SetItem(1, 2, 'luz.ojeda@email.com')
        self.user_list.InsertItem(1, '4')
        self.user_list.SetItem(1, 1, 'Sara')
        self.user_list.SetItem(1, 2, 'sari.maji@email.com')

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label="Lista de Usuarios:"), flag=wx.ALL, border=5)
        sizer.Add(self.user_list, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        self.SetSizer(sizer)

class OperationsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        wx.StaticText(self, label="Operaciones Bancarias")

        # Controles para Retirar
        wx.StaticText(self, label="Retirar:")
        self.withdraw_amount_ctrl = wx.TextCtrl(self)
        withdraw_button = wx.Button(self, label="Retirar")
        withdraw_button.Bind(wx.EVT_BUTTON, self.OnWithdraw)

        # Controles para Consultar Saldo
        balance_button = wx.Button(self, label="Consultar Saldo")
        balance_button.Bind(wx.EVT_BUTTON, self.OnCheckBalance)
        self.balance_text = wx.StaticText(self, label="Saldo: $0.00")

        # Controles para Transferir
        wx.StaticText(self, label="Transferir a Cuenta:")
        self.transfer_account_ctrl = wx.TextCtrl(self)
        wx.StaticText(self, label="Monto a Transferir:")
        self.transfer_amount_ctrl = wx.TextCtrl(self)
        transfer_button = wx.Button(self, label="Transferir")
        transfer_button.Bind(wx.EVT_BUTTON, self.OnTransfer)

        # Layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        withdraw_sizer = wx.BoxSizer(wx.HORIZONTAL)
        withdraw_sizer.Add(wx.StaticText(self, label="Retirar:"), flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border=5)
        withdraw_sizer.Add(self.withdraw_amount_ctrl, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)
        withdraw_sizer.Add(withdraw_button, flag=wx.LEFT, border=5)
        main_sizer.Add(withdraw_sizer, flag=wx.ALL | wx.EXPAND, border=10)

        balance_sizer = wx.BoxSizer(wx.HORIZONTAL)
        balance_sizer.Add(balance_button)
        balance_sizer.Add(self.balance_text, flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=10)
        main_sizer.Add(balance_sizer, flag=wx.ALL | wx.EXPAND, border=10)

        transfer_sizer = wx.BoxSizer(wx.VERTICAL)
        transfer_sizer.Add(wx.StaticText(self, label="Transferir:"), flag=wx.BOTTOM, border=5)
        transfer_sizer.Add(wx.StaticText(self, label="Cuenta Destino:"), flag=wx.LEFT | wx.RIGHT | wx.TOP, border=5)
        transfer_sizer.Add(self.transfer_account_ctrl, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)
        transfer_sizer.Add(wx.StaticText(self, label="Monto:"), flag=wx.LEFT | wx.RIGHT | wx.TOP, border=5)
        transfer_sizer.Add(self.transfer_amount_ctrl, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)
        transfer_sizer.Add(transfer_button, flag=wx.ALIGN_RIGHT | wx.TOP, border=10)
        main_sizer.Add(transfer_sizer, flag=wx.ALL | wx.EXPAND, border=10)

        self.SetSizer(main_sizer)

    '''Método para Retirar'''
    def OnWithdraw(self, event):
        amount_str = self.withdraw_amount_ctrl.GetValue()
        try:
            amount = float(amount_str)
            wx.MessageBox(f"Se ha solicitado un retiro de ${amount:.2f}", "Retiro", wx.OK | wx.ICON_INFORMATION)
            # Aquí iría la lógica real del retiro
        except ValueError:
            wx.MessageBox("Por favor, ingrese un monto válido.", "Error", wx.OK | wx.ICON_ERROR)

    '''Método para revisar el saldo de una cuenta y mostrarlo en pantalla'''
    def OnCheckBalance(self, event):
        # Aquí iría la lógica para obtener el saldo real
        balance = 1234.56
        self.balance_text.SetLabel(f"Saldo: ${balance:.2f}")

    '''Método para transferir'''
    def OnTransfer(self, event):
        account = self.transfer_account_ctrl.GetValue()
        amount_str = self.transfer_amount_ctrl.GetValue()
        try:
            amount = float(amount_str)
            wx.MessageBox(f"Se ha solicitado una transferencia de ${amount:.2f} a la cuenta {account}", "Transferencia", wx.OK | wx.ICON_INFORMATION)
            # Aquí iría la lógica real de la transferencia
        except ValueError:
            wx.MessageBox("Por favor, ingrese un monto válido.", "Error", wx.OK | wx.ICON_ERROR)

class MainAppFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(600, 400))

        self.notebook = wx.Notebook(self)
        self.user_info_panel = UserInfoPanel(self.notebook)
        self.operations_panel = OperationsPanel(self.notebook)

        self.notebook.AddPage(self.user_info_panel, "Usuarios")
        self.notebook.AddPage(self.operations_panel, "Operaciones")

        self.CreateStatusBar()
        self.SetStatusText("Bienvenido a la Aplicación Bancaria")

        self.Centre()
        self.Show()

if __name__ == '__main__':
    app = wx.App()
    login_frame = LoginFrame(None, "Iniciar Sesión")
    app.MainLoop()