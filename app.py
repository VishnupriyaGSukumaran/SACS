import io
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import tkinter as tk
import tkinter.font as tkFont
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import ttk

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly','https://www.googleapis.com/auth/drive.file']

creds = None

class App:
    def __init__(self, root):
        #setting title
        root.title("SACS")

        #setting window size
        width=780
        height=662
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        #SACS top title
        GLabel_470=tk.Label(root)
        ft = tkFont.Font(family='Times',size=20)
        GLabel_470["font"] = ft
        GLabel_470["fg"] = "#333333"
        GLabel_470["justify"] = "center"
        GLabel_470["text"] = "SACS"
        GLabel_470.place(x=310,y=20,width=113,height=30)

        #Google Drive Login Button
        GButton_635=tk.Button(root)
        GButton_635["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=10)
        GButton_635["font"] = ft
        GButton_635["fg"] = "#000000"
        GButton_635["justify"] = "center"
        GButton_635["text"] = "Login"
        GButton_635.place(x=640,y=20,width=50,height=36)
        GButton_635["command"] = self.btn_google_drive_login

        #Key- File Path label
        GLabel_87=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_87["font"] = ft
        GLabel_87["fg"] = "#333333"
        GLabel_87["justify"] = "left"
        GLabel_87["anchor"] = "w"
        GLabel_87["text"] = "Key File Path"
        GLabel_87.place(x=60,y=110,width=114,height=30)

        #Key- File Path textbox
        global form_key_file_path
        form_key_file_path = tk.StringVar()
        GLineEdit_949=tk.Entry(root,textvariable=form_key_file_path,state="readonly")
        GLineEdit_949["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_949["font"] = ft
        GLineEdit_949["fg"] = "#333333"
        GLineEdit_949["justify"] = "center"
        # GLineEdit_949["text"] = ""
        GLineEdit_949.place(x=60,y=140,width=462,height=37)

        #Key- File Path button
        GButton_770=tk.Button(root)
        GButton_770["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=10)
        GButton_770["font"] = ft
        GButton_770["fg"] = "#000000"
        GButton_770["justify"] = "center"
        GButton_770["text"] = "Select Key File"
        GButton_770.place(x=540,y=140,width=151,height=37)
        GButton_770["command"] = self.btn_key_select

        #Upload- label
        GLabel_2=tk.Label(root)
        ft = tkFont.Font(family='Times',size=18)
        GLabel_2["font"] = ft
        GLabel_2["fg"] = "#333333"
        GLabel_2["justify"] = "left"
        GLabel_2["anchor"] = "w"
        GLabel_2["text"] = "Upload"
        GLabel_2.place(x=60,y=210,width=70,height=25)

        #Upload- file path label
        GLabel_795=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_795["font"] = ft
        GLabel_795["fg"] = "#333333"
        GLabel_795["justify"] = "left"
        GLabel_795["anchor"] = "w"
        GLabel_795["text"] = "File Path"
        GLabel_795.place(x=60,y=240,width=70,height=25)

        #Upload- file path textbox
        global file_path
        file_path = tk.StringVar()
        GLineEdit_711=tk.Entry(root,textvariable= file_path,state="readonly")
        GLineEdit_711["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_711["font"] = ft
        GLineEdit_711["fg"] = "#333333"
        GLineEdit_711["justify"] = "left"
        GLineEdit_711.place(x=60,y=270,width=461,height=36)

        #Upload- file choose button
        GButton_825=tk.Button(root)
        GButton_825["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=10)
        GButton_825["font"] = ft
        GButton_825["fg"] = "#000000"
        GButton_825["justify"] = "center"
        GButton_825["text"] = "Choose File"
        GButton_825.place(x=540,y=270,width=155,height=36)
        GButton_825["command"] = self.btn_upload_file_choose
       
        #Upload- file button 
        GButton_434=tk.Button(root)
        GButton_434["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=10)
        GButton_434["font"] = ft
        GButton_434["fg"] = "#000000"
        GButton_434["justify"] = "center"
        GButton_434["text"] = "Upload"
        GButton_434.place(x=300,y=340,width=154,height=41)
        GButton_434["command"] = self.btn_upload

        #Download- label
        GLabel_222=tk.Label(root)
        ft = tkFont.Font(family='Times',size=18)
        GLabel_222["font"] = ft
        GLabel_222["fg"] = "#333333"
        GLabel_222["justify"] = "left"
        GLabel_222["anchor"] = "w"
        GLabel_222["text"] = "Download"
        GLabel_222.place(x=60,y=420,width=120,height=25)

        #Download- drive link label
        GLabel_394=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_394["font"] = ft
        GLabel_394["fg"] = "#333333"
        GLabel_394["justify"] = "left"
        GLabel_394["anchor"] = "w"
        GLabel_394["text"] = "File Id"
        GLabel_394.place(x=60,y=450,width=70,height=30)

        #Download- drive link url
        global file_id
        file_id = tk.StringVar()
        GLineEdit_0=tk.Entry(root,textvariable=file_id)
        GLineEdit_0["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_0["font"] = ft
        GLineEdit_0["fg"] = "#333333"
        GLineEdit_0["justify"] = "left"
        GLineEdit_0.place(x=60,y=480,width=639,height=37)

        #Download- button
        GButton_368=tk.Button(root)
        GButton_368["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=10)
        GButton_368["font"] = ft
        GButton_368["fg"] = "#000000"
        GButton_368["justify"] = "center"
        GButton_368["text"] = "Download"
        GButton_368.place(x=300,y=540,width=150,height=41)
        GButton_368["command"] = self.btn_download

    def btn_google_drive_login(self):
        global creds
        # If existing token
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

    def btn_key_select(self):
        filename = askopenfilename()
        print(filename)
        global form_key_file_path
        form_key_file_path.set(filename)        

    def btn_upload_file_choose(self):
        filename = askopenfilename()
        print(filename)
        global file_path
        file_path.set(filename)

    def btn_upload(self):
        file_path.get()
        try:
            drive_service = build('drive', 'v3', credentials=creds)
            file_metadata = {
            'name': os.path.basename(file_path.get()),
            'mimeType': '*/*'
            }
            media = MediaFileUpload(file_path.get(),
                                    mimetype='*/*',
                                    resumable=True)
            file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print ('File ID: ' + file.get('id'))
            drive_service.permissions().create(body={"role":"reader", "type":"anyone"}, fileId=file.get('id')).execute()
            print ('File Shared Successfully')
            file.get('id')
            file_id.set(file.get('id'))
        except HttpError as error:
            print(f'An error occurred: {error}')

    def btn_download(self):
        # google_drive_file_id=''
        # url_split = drive_link.split("/")
        # google_drive_file_id=url_split[5]
        google_drive_file_id=file_id.get()

        if(google_drive_file_id!=''):
            try:
                drive_service = build('drive', 'v3', credentials=creds)

                # file name
                file = drive_service.files().get(fileId=google_drive_file_id).execute()
                file_name = file.get("name")
                print(f'File name: {file_name}')

                # file download 
                request = drive_service.files().get_media(fileId=google_drive_file_id)
                file_bytes = io.BytesIO()
                downloader = MediaIoBaseDownload(file_bytes, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print(F'Downloaded {int(status.progress() * 100)}%')

                # save path
                file_name_save = asksaveasfilename(initialfile=file_name)
                print(file_name_save)

                # write to file
                with open(file_name_save, "wb") as f:
                    f.write(file_bytes.getbuffer())

            except HttpError as error:
                print(f'An error occurred: {error}')
                file_bytes = None
        
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
