from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen,ScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.picker import MDDatePicker

class WelcomeScreen(Screen):
    pass
class UsernameScreen(Screen):
    pass
class DOB(Screen):
    pass
class MainScreen(Screen):
    pass
sm = ScreenManager()
sm.add_widget(WelcomeScreen(name = 'welcomescreen'))
sm.add_widget(UsernameScreen(name = 'usernamescreen'))
sm.add_widget(DOB(name = 'dob'))
sm.add_widget(MainScreen(name = 'main_screen'))


class MainApp(MDApp):
    def build(self):
        self.kv = Builder.load_file("main.kv")
        return self.kv
    
    def check_username(self):
        self.username_text = self.kv.get_screen('usernamescreen').ids.username_text_fied.text
        username_check_false = True
        try:
            int(self.username_text)
        except:
            username_check_false = False
        if username_check_false or self.username_text.split() == []:
                cancel_btn_username_dialogue = MDFlatButton(text='Retry',on_release = self.close_username_dialogue)
                self.dialog = MDDialog(title = 'Invalid Username',text = "Please input a valid username",size_hint = (0.7,0.2),buttons = [cancel_btn_username_dialogue])
                self.dialog.open()

        else:
            self.kv.get_screen('usernamescreen').ids.disabled_button.disabled = False

    def close_username_dialogue(self,obj):
        self.dialog.dismiss()

    def show_date_picker(self):
        date_dialog = MDDatePicker(callback = self.get_date,year = 1999,month = 1,day =1,)
        date_dialog.open()
    def get_date(self,date):
        self.dob = date
        self.kv.get_screen('dob').ids.date_picker.text = str(self.dob)
        self.kv.get_screen('dob').ids.second_disabled.disabled = False

        #Storing of DATA
        self.store.put('UserInfo',name = self.username_text,dob = str(self.dob))
        self.username_changer()

    def username_changer(self):
        self.kv.get_screen('mainscreen').ids.profile_name.text = f"welcome {self.store.get('UserInfo')['name']}"

    def on_start(self):
        self.store = JsonStore("userProfile.json")
        try:
            if self.store.get('UserInfo')['name'] != "":
                self.username_changer()
                self.kv.get_screen('mainscreen').manager.current = 'mainscreen'
                
        except KeyError:
            self.kv.get_screen('welcomescreen').manager.current = 'welcomescreen'

    
MainApp().run()