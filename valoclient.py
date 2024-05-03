from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, QCheckBox, QComboBox, QLabel, QStyleFactory, QMessageBox, QProgressBar, QListWidget, QListWidgetItem, QAction, QDialog, QSpinBox, QFileDialog
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
import sys
import os
import requests
import pyperclip
import json
import time
import subprocess
import base64
region = "eu"
shard  = "eu"

# Function to get port and password

def get_port_password():
    home_dir = os.path.expanduser("~")
    lockfile_path = os.path.join(home_dir, r"AppData\\Local\\Riot Games\\Riot Client\\Config\\lockfile")
    port = password = None
    if os.path.exists(lockfile_path):
        with open(lockfile_path, "r") as f:
            data = f.read().split(":")
            port = data[2]
            password = data[3]
    return port, password

auth_token = None
entitlement_token = None

# Get puuid of user
def get_puuid(port, password):
    url = f"https://127.0.0.1:{port}/rso-auth/v1/authorization/userinfo"
    response = requests.get(url, auth=("riot", password), verify=False)
    return json.loads(response.json()['userInfo'])['sub']
'''
def get_matchid(port, password):
    puuid = get_puuid(port, password)
    if puuid is None:
        return None
    url = f"https://glz-{region}-1.{shard}.a.pvp.net/core-game/v1/players/{puuid}"
    method = "GET"
    try:
        response = send_api_request(url, method)
        response_data = json.loads(response)
        matchids = response_data.get('MatchID')
        return matchids
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None'''

def get_prematchid(port, password):
    puuid = get_puuid(port, password)
    url = f"https://glz-{region}-1.{shard}.a.pvp.net/pregame/v1/players/{puuid}"
    method = "GET"
    response = send_api_request(url, method)
    response_data = json.loads(response)
    prematchid = response_data.get('MatchID')
    return prematchid

def get_matchid(port, password):
    puuid = get_puuid(port, password)
    url = f"https://glz-{region}-1.{shard}.a.pvp.net/core-game/v1/players/{puuid}"
    method = "GET"
    response = send_api_request(url, method)
    response_data = json.loads(response)
    matchids = response_data.get('MatchID')
    return matchids

def get_partyid(port, password):
    puuid = get_puuid(port, password)
    url = f"https://glz-{region}-1.{shard}.a.pvp.net/parties/v1/players/{puuid}"
    method = "GET"
    response = send_api_request(url, method)
    response_data = json.loads(response)
    partyid = response_data.get('CurrentPartyID')
    return partyid

# Function to get auth token and entitlement token
def get_tokens(port, password):
    global auth_token, entitlement_token
    if auth_token and entitlement_token:
        # If the tokens have already been fetched, return them
        return auth_token, entitlement_token
    else:
        # Otherwise, make the API call to fetch the tokens
        url = f"https://127.0.0.1:{port}/entitlements/v1/token"
        response = requests.get(url, auth=("riot", password), verify=False)
        if response.status_code == 200:
            auth_token, entitlement_token = response.json()["accessToken"], response.json()["token"]
            return auth_token, entitlement_token
        else:
            return None, None

# Function to send API request
def send_api_request(url, method, data=None):
    port, password = get_port_password()
    if port and password:
        auth_token, entitlement_token = get_tokens(port, password)
        if auth_token and entitlement_token:
            headers = {
                "X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9",
                "X-Riot-ClientVersion": "release-08.07-shipping-11-2460481",
                "X-Riot-Entitlements-JWT": entitlement_token,
                "Authorization": f"Bearer {auth_token}"
            }
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers)
            elif method == "PUT":
                response = requests.put(url, headers=headers, json=data)
                
            # Add more elif statements for other methods as needed
            else:
                print(f"Unsupported method: {method}")
                return

            if response.status_code == 200:
                return response.text
            else:
                print("Failed to send API request.")
                return "{}"
        else:
            print("Failed to get auth token and entitlement token.")
    else:
        print("Failed to get port and password.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        

        self.port, self.password = get_port_password()
        self.resize(500, 300)
        self.statusBar().showMessage("Ready")

        self.toolbar = self.addToolBar('yk')
        self.addToolBar(Qt.BottomToolBarArea, self.toolbar)

        # In your __init__ method, after creating the toolbar
        #self.viewMenu = self.menuBar().addMenu("View")
        #self.toggleToolbarAction = self.viewMenu.addAction("Show Toolbar")
        #self.toggleToolbarAction.setCheckable(True)
        #self.toggleToolbarAction.setChecked(True)  # The toolbar is visible initially
        #self.toggleToolbarAction.triggered.connect(self.toggle_toolbar)
        self.delay_time = 6


        self.toolbar.setMovable(False)
        self.toolbar.setStyleSheet("background-color: #1F2041;")
        settings_icon_base64 = "iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAAsTAAALEwEAmpwYAAAC2UlEQVR4nO2av2sUQRTHP8FgUHMngtHCHwg5UCNioqIRS7HRXi099A8wxM4YECGiYv6CWNl5iIWtgoVGLKKthSjmULhYaZFc7pJbGXgLy7ruzszO3e6d+cIXApmbed/deTvffW9hA/8H7gPrgBdiE5iki1CNEOHzA12CItCKEVIH+ukCjMeI8HkoywD3AxPAUMK4soaQSwlzDAE3gH04xgHgqwRRAy7GjH2oIeROzO/PAd9lnMq1kisRpYjkVTnwCBgIjd0BvNEQ8goohH67WS5COL8WgeF2iAjyIzAiefEcWNUQ4XMZeAIcBQ4CCzFjU4nZmyDCZ8Mg+CiqO7CiMW4R2GMjRCdpO82rNkK2Ap9yELwn/AwMYokTDraOCzaB06TEdA6ETOEAyk7MZyjiLbAJRyhltMWWXZwhQZzJ6G6sA0dcCnlhGICyMbeAUWCbcEz2es1wrjlXInbJU0N34acR9iMI9b+KwXy/gC227xPKclwXP/XeUESfxhp9hmJeAw/kkD6VcKG4JzbAdj/XkhaIuGBLKdb7JjH/hbWUialywhS3U665FjVp3OupDo9ZCBlLuWarHUJsfFAhj0IKFkKKeRQympet1cjA2KU1pI2oSW9K8azeocfvduCn5Vp1iXUyye2q9/DLwIxmMcFnxeBAfGYw70vgrpSRDtsW+EwtSkWSOO5OmIj4bWtRXJjGJTnsjstjeVD+nrbYTo/pARvfcm3jRwy3lyuuSM3LCQakEOdlxAWpQqbGbIYiPKEqpabCeQcnvqtcuWArYifwIwcivMCBu9tGyEQOgvdCVD0Tq8aOThF7tUNF7KrE1Ja2wjsZMy6ntW1bYTihCFh10fCJEtOUU7o/otEzr1lMCBtMVU2cinDhTrtWwdbbF+Bsyse1MoD/wslAF8CpiGDjpyzFtjhc0xByRaOlUbZt7HTSlykrnnsUe+WDgZ75hAOpAPbERzUbwBJ/AGHShFfzN0J6AAAAAElFTkSuQmCC"
        settings_icon_bytes = base64.b64decode(settings_icon_base64)
        settings_icon_pixmap = QtGui.QPixmap()
        settings_icon_pixmap.loadFromData(settings_icon_bytes)
        settings_icon = QtGui.QIcon(settings_icon_pixmap)
        self.settings_button = QAction(settings_icon, 'Settings', self)  # Replace 'settings.png' with the path to your settings icon
        self.toolbar.addAction(self.settings_button)
        self.settings_button.triggered.connect(self.open_settings_dialog)



        self.setWindowTitle("pylorant")
        self.setStyleSheet("""
    QMainWindow {
        background-color: #334D50;
        color: #ffffff;
        font-family: 'Cascadia Mono SemiBold';
    }
    QPushButton {
        background-color: #333333;
        border: 2px solid #334D50;
        border-radius: 10px;
        padding: 5px;
        color: #ffffff;
        font-family: 'Cascadia Mono SemiBold';
        
                           
    }
    QPushButton:hover {
        background-color: darkcyan;
    }
    QComboBox {
        background-color: #333333;
        border: 2px solid #555555;
        border-radius: 10px;
        padding: 5px;
        color: #ffffff;
        Cascadia Mono SemiBold
    }
    QComboBox QAbstractItemView {
        background-color: #333333;
        color: #ffffff;
    }
    QCheckBox {
        color: #ffffff;
        Cascadia Mono SemiBold
    }
    
    QTabWidget::pane {
        border: 0;
    }
    QTabBar::tab {
        background: #333333;
        color: #ffffff;
        padding: 10px;
        margin: 4px;
        border-radius: 4px;
        Cascadia Mono SemiBold
    }
    QTabBar::tab:selected {
        background: #555555;
    }
""")
        


        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        

        self.matchmaking_tab = QWidget()
        self.agent_select_tab = QWidget()
        self.reveal_tab = QWidget()
        #self.loadout_tab = QWidget()
        self.friends_tab = QWidget()
        self.misc_tab = QWidget()

        self.tab_widget.setStyleSheet("QTabBar::tab { color: black; }")    
        self.tab_widget.addTab(self.matchmaking_tab, "Matchmaking")
        self.tab_widget.addTab(self.agent_select_tab, "Agent Select")
        self.tab_widget.addTab(self.reveal_tab, "Reveal")
        #self.tab_widget.addTab(self.loadout_tab, "Loadout")
        self.tab_widget.addTab(self.friends_tab, "Friends")
        self.tab_widget.addTab(self.misc_tab, "Misc")

        valorant_icon_base64 = "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"
        valorant_icon_bytes = base64.b64decode(valorant_icon_base64)
        valorant_icon_pixmap = QtGui.QPixmap()
        valorant_icon_pixmap.loadFromData(valorant_icon_bytes)
        valorant_icon = QtGui.QIcon(valorant_icon_pixmap)
        self.start_valorant_button = QAction(valorant_icon, 'Start Valorant', self)
        self.toolbar.addAction(self.start_valorant_button)
        self.start_valorant_button.triggered.connect(self.start_valorant)

        refresh_icon_base64 = "iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAAsTAAALEwEAmpwYAAABsUlEQVR4nO3ZPUoDQRjG8b+yisFgF/AWgoXiHQRBcoTUdmoTBUFIbZELhBxAsRCvYeFHaj2AxEKbHRkYYRl2ya6+rzsD88AUSbHv/rLztRNISUnRzArQB6bAE/ABmAYtiBwAs4Y3HhRkGRj9ERAEZCSEMG13p9y7mU/gCtgF1olkYM88xCuwRWTplzwJLUTPNZVMPYjtThrpAQ+uqWCePciOIsK4poKZe5CuMsK4ZhfaTclCmlNnFcJoYLQgixBGGqMBqYswkhhpSFOEkcJIQ45KrnlX87tBSBCbi8L17oG1kjqrwG3h81mog/20gKiq84M5J/DpN6tRJ5Mq9l9bcKNdJ0EaxqQnUjOpa4Xwg2U1CthTlaAhJ26h6ixYqK6BoURBDcixt3XoVGwdbgqfh6FBBm1t5qQhv91ePwq9+BjJrtUUI4VQGex1MZIItel3EUYaobrwVmE0EBtejfcoD86AvZL38/iOMoGxB5kQ4eHyNvDlQQ6JLBbx5iFe3F8ZwafrxsS45EnkwH6bN2eE2mWbCAlI7hBLMUPsmGi1OxXT5MbnblGduNkpioGdkkKk+Qa0I94kxrm/NwAAAABJRU5ErkJggg==')"
        refresh_icon_bytes = base64.b64decode(refresh_icon_base64)
        refresh_icon_pixmap = QtGui.QPixmap()
        refresh_icon_pixmap.loadFromData(refresh_icon_bytes)
        refresh_icon = QtGui.QIcon(refresh_icon_pixmap)

        self.refresh_button = QAction(refresh_icon, 'Refresh', self)
        self.toolbar.addAction(self.refresh_button)
        self.refresh_button.triggered.connect(self.refresh)


        self.create_matchmaking_tab()
        self.create_agent_select_tab()
        #self.create_loadout_tab()
        self.create_reveal_tab()
        self.create_friends_tab()
        self.create_misc_tab()

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    
    def refresh(self):
    # Refresh the tokens
        get_tokens(self.port, self.password)

        get_partyid(self.port, self.password)

    # Clear the existing layout of the friends tab
        self.clear_layout(self.friends_tab.layout())

    # Refresh the friends tab
        self.create_friends_tab()

    def start_valorant(self):
        valorant_path = r"" #Enter Valorant path
        if not os.path.exists(valorant_path):
            valorant_path, _ = QFileDialog.getOpenFileName(self, "Select Valorant Executable")

        if valorant_path:  # If a path was selected (or the default path exists)
            subprocess.Popen(valorant_path)
        else:
            print("No Valorant executable selected")
        
    def toggle_toolbar(self, state):
        if state:
            self.toolbar.show()
        else:
            self.toolbar.hide()

    def open_settings_dialog(self):
    # Create a dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Settings")
        dialog.setWhatsThis("has to be 6 seconds or higher cuz on lower valo might freeze in loadscreen...")

    # Create a layout for the dialog
        layout = QVBoxLayout()
        dialog.setLayout(layout)
        dialog.setStyleSheet("background-color: #1F2041; color: #E5E5E5;") #fine colors: #334D50 #4A4E69 #225378 oxfordblue: #1F2041

    # Add a QSpinBox for the delay time
        layout.addWidget(QLabel("Delay Time for agent select (seconds):"))
        self.delay_time_spinbox = QSpinBox()
        self.delay_time_spinbox.setRange(6, 60)  # Set the range to 1-60 seconds
        layout.addWidget(self.delay_time_spinbox)

    # Add QSpinBoxes for the window width and height
        layout.addWidget(QLabel("Window Width:"))
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(500, 2000)  # Set the range to 100-2000 pixels
        layout.addWidget(self.width_spinbox)

        layout.addWidget(QLabel("Window Height:"))
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setRange(300, 2000)  # Set the range to 100-2000 pixels
        layout.addWidget(self.height_spinbox)

    # Add a button to save the settings
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

    # Show the dialog
        dialog.exec_()

    def save_settings(self):
    # Get the value from the QSpinBox
        self.delay_time = self.delay_time_spinbox.value()
        self.width = self.width_spinbox.value()
        self.height = self.height_spinbox.value()

        self.resize(self.width, self.height)

        print(f"Saved settings: delay_time={self.delay_time} seconds")
 


    def create_matchmaking_tab(self):
        layout = QVBoxLayout()

        self.enter_queue_button = QPushButton("Enter Queue")
        self.enter_queue_button.clicked.connect(self.enter_queue)
        self.leave_queue_button = QPushButton("Leave Queue")
        self.leave_queue_button.clicked.connect(self.leave_queue)

        self.queue_dropdown = QComboBox()
        queue = [
		"unrated",
		"competitive",
		"swiftplay",
		"spikerush",
		"deathmatch",
		"ggteam",
		"custom"
	]
        self.queue_dropdown.addItems(queue)
        self.change_queue_button = QPushButton("Change queue")
        self.change_queue_button.clicked.connect(self.change_queue)


        layout.addWidget(self.enter_queue_button)
        layout.addWidget(self.leave_queue_button)
        layout.addWidget(self.queue_dropdown)
        layout.addWidget(self.change_queue_button)

        self.matchmaking_tab.setLayout(layout)

    def create_agent_select_tab(self):
        layout = QVBoxLayout()

        self.agent_dropdown = QComboBox()
        agents = requests.get('https://valorant-api.com/v1/agents').json()
        agent_names = [agent['displayName'] for agent in agents['data']]
        self.agent_dropdown.addItems(agent_names)

        self.lock_checkbox = QCheckBox("Lock Agent")
        self.lock_checkbox.stateChanged.connect(self.lock_agent)

        self.auto_lock_checkbox = QCheckBox("Auto Lock")
        self.auto_lock_checkbox.stateChanged.connect(self.auto_lock)

        self.dodge_button = QPushButton("Dodge")
        self.dodge_button.clicked.connect(self.dodge)
        

        layout.addWidget(self.agent_dropdown)
        layout.addWidget(self.lock_checkbox)
        layout.addWidget(self.auto_lock_checkbox)
        layout.addWidget(self.dodge_button)

        self.agent_select_tab.setLayout(layout)

    def create_reveal_tab(self):
        layout = QVBoxLayout()

        # Create a button for revealing names
        self.reveal_names_button = QPushButton("Reveal Names")
        self.reveal_names_button.clicked.connect(self.reveal_names)

        # Create an output field for displaying the names
        self.names_output = QLabel()
        self.names_output.setWordWrap(True)

        # Add the widgets to the layout
        layout.addWidget(self.reveal_names_button)
        layout.addWidget(self.names_output)

        self.reveal_tab.setLayout(layout)
        
    '''
    def create_loadout_tab(self):
        layout = QVBoxLayout()

    # Create a dropdown for the weapons
        self.weapon_dropdown = QComboBox()
        weapons = requests.get('https://valorant-api.com/v1/weapons').json()
        weapon_names = [weapon['displayName'] for weapon in weapons['data']]
        self.weapon_dropdown.addItems(weapon_names)

    # Create a dropdown for the weapon skins
        self.skin_dropdown = QComboBox()
        skins = requests.get('https://valorant-api.com/v1/weapons/skins').json()
        skin_names = [skin['displayName'] for skin in skins['data']]
        self.skin_dropdown.addItems(skin_names)

    # Create a button to change the loadout
        self.change_loadout_button = QPushButton("Change Loadout")
        self.change_loadout_button.clicked.connect(self.change_loadout)

    # Add the widgets to the layout
        layout.addWidget(self.weapon_dropdown)
        layout.addWidget(self.skin_dropdown)
        layout.addWidget(self.change_loadout_button)

        self.loadout_tab.setLayout(layout)

    def change_loadout(self):
        weapons = requests.get('https://valorant-api.com/v1/weapons').json()
        skins = requests.get('https://valorant-api.com/v1/weapons/skins').json()
        selected_weapon_id = next(weapon['uuid'] for weapon in weapons['data'] if weapon['displayName'] == self.weapon_dropdown.currentText())
        selected_skin_id = next(skin['uuid'] for skin in skins['data'] if skin['displayName'] == self.skin_dropdown.currentText())

        # Replace with the actual URL and method for changing the loadout
        puuid = get_puuid(self.port, self.password)
        url = f"https://pd.{shard}.a.pvp.net/personalization/v2/players/{puuid}/playerloadout"
        method = "PUT"
        data = {
            "Guns": [
             {
                    "ID": selected_weapon_id,
                    "SkinID": selected_skin_id,
                    "SkinLevelID": "00000000-0000-0000-0000-000000000000",
                    "ChromaID": "00000000-0000-0000-0000-000000000000",
                    "Attachments": []
                }
            ],
            "Sprays": [],
            "Identity": {},
            "Incognito": False
        }
        send_api_request(url, method, data)
        '''
    def create_misc_tab(self):
        layout = QVBoxLayout()
        self.accessibility_checkbox = QCheckBox("set member ready to false (prevents your party from queuing)")
        self.accessibility_checkbox.stateChanged.connect(self.misc)
        layout.addWidget(self.accessibility_checkbox)

        self.misc_tab.setLayout(layout)

    def misc(self):
        partyid = get_partyid(self.port, self.password)
        puuid = get_puuid(self.port, self.password)
        url = f"https://glz-{region}-1.{shard}.a.pvp.net/parties/v1/parties/{partyid}/members/{puuid}/setReady"
        method = "POST"

        if self.accessibility_checkbox.isChecked():
            data = {"ready": False}
        else:
            data = {"ready": True}

        send_api_request(url, method, data)

    def enter_queue(self):
        # Replace with the actual URL and method for entering the queue
        partyid = get_partyid(self.port, self.password)
        url = f"https://glz-eu-1.eu.a.pvp.net/parties/v1/parties/{partyid}/matchmaking/join"
        method = "POST"
        send_api_request(url, method)

    def leave_queue(self):
        partyid = get_partyid(self.port, self.password)
        # Replace with the actual URL and method for leaving the queue
        url = f"https://glz-eu-1.eu.a.pvp.net/parties/v1/parties/{partyid}/matchmaking/leave"
        method = "POST"
        send_api_request(url, method)

    def lock_agent(self):
        if self.lock_checkbox.isChecked() or self.auto_lock_checkbox.isChecked():
            prematchid = get_prematchid(self.port, self.password)
            agents = requests.get('https://valorant-api.com/v1/agents').json()
            selected_agent_id = next(agent['uuid'] for agent in agents['data'] if agent['displayName'] == self.agent_dropdown.currentText())
            url = f"https://glz-{region}-1.{shard}.a.pvp.net/pregame/v1/matches/{prematchid}/lock/{selected_agent_id}"
            method = "POST"
            response = send_api_request(url, method)
            if response:  # Check if the request was successful
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(f"Successfully locked agent = {self.agent_dropdown.currentText()}")
                msg.setWindowTitle("Agent Lock")
                msg.exec_()
    
    def change_queue(self):
        partyid = get_partyid(self.port, self.password)
        queue_id = self.queue_dropdown.currentText()
        url = f"https://glz-{region}-1.{shard}.a.pvp.net/parties/v1/parties/{partyid}/queue"
        method = "POST"
        data = {"queueId": queue_id}
        send_api_request(url, method, data)

    def dodge(self):
        preid = get_prematchid(self.port, self.password)
        url = f"https://glz-{region}-1.{shard}.a.pvp.net/pregame/v1/matches/{preid}/quit"
        method = "POST"
        send_api_request(url, method)



    def auto_lock(self):
        if self.auto_lock_checkbox.isChecked():
            self.timer = QTimer()
            self.timer.timeout.connect(self.check_pregame_and_lock)
            self.timer.start(800)  # Check every second

    def check_pregame_and_lock(self):
        prematchid = get_prematchid(self.port, self.password)
        if prematchid:
            QTimer.singleShot(self.delay_time * 1000, self.lock_agent)
            self.timer.stop()  # Stop checking once a match is found and the agent is locked
    #reveals all players that have their privacy settings enabled
    def reveal_names(self):
    # Get the pre-game match ID
        match_ids = get_matchid(self.port, self.password)
        if not match_ids:
        # Show a pop-up message if no active game is found
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("No active game found")
            msg.setWindowTitle("Error")
            msg.exec_()
            return

    # Get the match data
        url = f"https://glz-{region}-1.{shard}.a.pvp.net/core-game/v1/matches/{match_ids}"
        method = "GET"
        response = send_api_request(url, method)
        response_data = json.loads(response)
        match_data = response_data

    # Get the list of agents
        agents = requests.get('https://valorant-api.com/v1/agents').json()
        agent_dict = {agent['uuid']: agent['displayName'] for agent in agents['data']}

    # Get the PUUIDs of the players who have incognito enabled and their agent names
        incognito_puuids = []
        player_info = []
        for player in match_data["Players"]:
            if player["PlayerIdentity"]["Incognito"]:
                incognito_puuids.append(player["Subject"])
                agent_name = agent_dict.get(player["CharacterID"], "Unknown Agent")
                player_info.append((player["Subject"], agent_name))

    # Get the names of the players
        url = f"https://pd.{shard}.a.pvp.net/name-service/v2/players"
        method = "PUT"
        data = incognito_puuids
        response = send_api_request(url, method, data)
        response_data = json.loads(response)

    # Combine the player names, taglines, and agent names
        player_names = [f"{player['GameName']} {player['TagLine']} ({next(agent for puuid, agent in player_info if puuid == player['Subject'])})" for player in response_data]

    # Display the names in the output field
        self.names_output.setText("\n".join(player_names))

    def create_friends_tab(self):
    # Check if the friends_tab already has a layout
        layout = self.friends_tab.layout()
        if layout is None:
        # If not, create a new QVBoxLayout
            layout = QVBoxLayout()
            self.friends_tab.setLayout(layout)
        else:
        # If it does, clear the existing layout
            self.clear_layout(layout)

        self.friends_list = QListWidget()
        self.friends_list.setStyleSheet("background-color: #334D50; color: gold;")

    # Get the list of friends
        friends = self.get_presences()
        if isinstance(friends, dict) and 'presences' in friends:
            for friend in friends['presences']:
                # Create a QLabel with rich text
                #label = QLabel()
                #label.setTextFormat(Qt.RichText)
                #label.setText(f"<font color='gold'>{friend['game_name']}#{friend['game_tag']}</font> <font color='black'>Game: {friend['product']} {'ingame' if friend['state'] == 'dnd' else friend['state']}</font>")
                # Create a QLabel with rich text
                label = QLabel()
                label.setTextFormat(Qt.RichText)
                game_color = '#3C0008' if friend['product'] == 'valorant' else '#1F2041' if friend['product'] == 'league_of_legends' else 'black'
                state = 'ingame' if friend['state'] == 'dnd' else friend['state']
                label.setText(f"<font color='#F2A541'>{friend['game_name']}#{friend['game_tag']}</font> <font color='{game_color}'>Game: {friend['product']}</font> <font color='black'>{state}</font>")


            # Create a QListWidgetItem and set the QLabel as its widget
                item = QListWidgetItem(self.friends_list)
                self.friends_list.setItemWidget(item, label)

    # Create an invite button
        self.invite_button = QPushButton('Invite all')
        self.invite_button.clicked.connect(self.invite_friend)
        layout.addWidget(self.friends_list)
        layout.addWidget(self.invite_button)
    '''
    def create_friends_tab(self):
    # Check if the friends_tab already has a layout
        layout = self.friends_tab.layout()
        if layout is None:
        # If not, create a new QVBoxLayout
            layout = QVBoxLayout()
            self.friends_tab.setLayout(layout)
        else:
        # If it does, clear the existing layout
            self.clear_layout(layout)

        self.friends_list = QListWidget()
        self.friends_list.setStyleSheet("background-color: #334D50; color: gold;")

    # Get the list of friends
        friends = self.get_presences()
        if isinstance(friends, dict) and 'presences' in friends:
            for friend in friends['presences']:
                item = QListWidgetItem(f"{friend['game_name']}#{friend['game_tag']}{" "}Game:{" "}{friend['product']}{" "}{friend['state']}")
                self.friends_list.addItem(item)

    # Create an invite button
        self.invite_button = QPushButton('Invite')
        self.invite_button.clicked.connect(self.invite_friend)
        layout.addWidget(self.friends_list)
        layout.addWidget(self.invite_button)'''

    def get_presences(self):
        try:
            if self.port is None:
                print("Error: Valorant is not running")
                return []
            url = f"https://127.0.0.1:{self.port}/chat/v4/presences"
            response = requests.get(url, auth=("riot", self.password), verify=False)
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
            return []

    
    def invite_friend(self):
    # Get the party id
        party_id = get_partyid(self.port, self.password)

    # Get the list of friends
        friends = self.get_presences()
        if isinstance(friends, dict) and 'presences' in friends:
            for friend in friends['presences']:
             # Check if the friend is playing Valorant
                if friend['product'] == 'valorant':
                    game_name, game_tag = friend['game_name'], friend['game_tag']
                    url = f"https://glz-eu-1.eu.a.pvp.net/parties/v1/parties/{party_id}/invites/name/{game_name}/tag/{game_tag}"
                    method = "POST"
                    send_api_request(url, method)


    


app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
app.setStyle(QStyleFactory.create('Fusion'))  # Set the application style to 'Fusion'
window = MainWindow()

icon_base64 = "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"
icon_bytes = base64.b64decode(icon_base64)
icon_pixmap = QtGui.QPixmap()
icon_pixmap.loadFromData(icon_bytes)
icon = QtGui.QIcon(icon_pixmap)

window.setWindowIcon(icon)
window.show()

app.exec_()


# PUT https://pd.{shard}.a.pvp.net/personalization/v2/players/{puuid}/playerloadout

# create new Loadout tab to select presets and change loadout with 1 click. read external api weapon ids and skin ids filter for owned and show a list to select each weapon skin and then save to preset. 2 days later aint doing this getting rito small brain

#Future features: switch button to set party availability on/off | alr done lol