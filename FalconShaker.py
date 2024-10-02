
# Falcon Shaker
# Authored by Yaan Dalzell

# Large parts of this program were generated using digital intelligence applications.
# A real human fixed all of the bits that didn't work.
# Please support human software developers when ever possible.

# Memory connector adapted from copyrighted work done by Dino Duratović

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import json
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.filedialog import askdirectory

import pyaudio
import pygame.mixer
import pygame._sdl2.audio as sdl2_audio
import threading
import time
import ctypes
import struct
import mmap



class FlightEvent:
    def __init__(self, name, fileName, volumeCoefficient=100.0, balance=0.0):
        self.name = name
        self.volumeCoefficient = tk.DoubleVar(value=volumeCoefficient)
        self.balance = tk.DoubleVar(value=balance)
        self.active = tk.BooleanVar(value=True)
        self.volume = None
        self.fileName = fileName


    def testSound(self):
        thisSound = pygame.mixer.Sound(os.path.join('Sound Files', self.fileName))
        thisChannel = pygame.mixer.Channel(19).stop()
        thisChannel = pygame.mixer.Channel(19)
        thisChannel.set_volume(self.get_volumes('l'), self.get_volumes('r'))
        thisChannel.play(thisSound)



    def get_volumes(self, ch):
        balanceValue = self.balance.get()
        volumeCoefficient = self.volumeCoefficient.get()
        # movement to left reduces RHS volume
        # Movement to right reduces LHS volume
        if ch == 'l':
            v = (min(100 - balanceValue, 100) / 100.0) * (volumeCoefficient / 100.0)
        elif ch == 'r':
            v = (min(100 + balanceValue, 100) / 100.0) * (volumeCoefficient / 100.0)
        else:
            v = volumeCoefficient / 100.0
        return v



class FlightData(ctypes.Structure):
    name = "FalconSharedMemoryArea"
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("z", ctypes.c_float),
        ("xDot", ctypes.c_float),
        ("yDot", ctypes.c_float),
        ("zDot", ctypes.c_float),
        ("alpha", ctypes.c_float),
        ("beta", ctypes.c_float),
        ("gamma", ctypes.c_float),
        ("pitch", ctypes.c_float),
        ("roll", ctypes.c_float),
        ("yaw", ctypes.c_float),
        ("mach", ctypes.c_float),
        ("kias", ctypes.c_float),
        ("vt", ctypes.c_float),
        ("gs", ctypes.c_float),
        ("windOffset", ctypes.c_float),
        ("nozzlePos", ctypes.c_float),
        ("internalFuel", ctypes.c_float),
        ("externalFuel", ctypes.c_float),
        ("fuelFlow", ctypes.c_float),
        ("rpm", ctypes.c_float),
        ("ftit", ctypes.c_float),
        ("gearPos", ctypes.c_float),
        ("speedBrake", ctypes.c_float),
        ("epuFuel", ctypes.c_float),
        ("oilPressure", ctypes.c_float),
        ("lightBits", ctypes.c_uint),
        ("headPitch", ctypes.c_float),
        ("headRoll", ctypes.c_float),
        ("headYaw", ctypes.c_float),
        ("lightBits2", ctypes.c_uint),
        ("lightBits3", ctypes.c_uint),
        ("ChaffCount", ctypes.c_float),
        ("FlareCount", ctypes.c_float),
        ("NoseGearPos", ctypes.c_float),
        ("LeftGearPos", ctypes.c_float),
        ("RightGearPos", ctypes.c_float),
        ("AdiIlsHorPos", ctypes.c_float),
        ("AdiIlsVerPos", ctypes.c_float),
        ("courseState", ctypes.c_int),
        ("headingState", ctypes.c_int),
        ("totalStates", ctypes.c_int),
        ("courseDeviation", ctypes.c_float),
        ("desiredCourse", ctypes.c_float),
        ("distanceToBeacon", ctypes.c_float),
        ("bearingToBeacon", ctypes.c_float),
        ("currentHeading", ctypes.c_float),
        ("desiredHeading", ctypes.c_float),
        ("deviationLimit", ctypes.c_float),
        ("halfDeviationLimit", ctypes.c_float),
        ("localizerCourse", ctypes.c_float),
        ("airbaseX", ctypes.c_float),
        ("airbaseY", ctypes.c_float),
        ("totalValues", ctypes.c_float),
        ("TrimPitch", ctypes.c_float),
        ("TrimRoll", ctypes.c_float),
        ("TrimYaw", ctypes.c_float),
        ("hsiBits", ctypes.c_uint),
        ("DEDLines", ctypes.c_char * 5 * 26),
        ("Invert", ctypes.c_char * 5 * 26),
        ("PFLLines", ctypes.c_char * 5 * 26),
        ("PFLInvert", ctypes.c_char * 5 * 26),
        ("UFCTChan", ctypes.c_int),
        ("AUXTChan", ctypes.c_int),
        ("RwrObjectCount", ctypes.c_int),
        ("RWRsymbol", ctypes.c_int * 40),
        ("bearing", ctypes.c_float * 40),
        ("missileActivity", ctypes.c_ulong * 40),
        ("missileLaunch", ctypes.c_ulong * 40),
        ("selected", ctypes.c_ulong * 40),
        ("lethality", ctypes.c_float * 40),
        ("newDetection", ctypes.c_ulong * 40),
        ("fwd", ctypes.c_float),
        ("aft", ctypes.c_float),
        ("total", ctypes.c_float),
        ("VersionNum", ctypes.c_int),
        ("headX", ctypes.c_float),
        ("headY", ctypes.c_float),
        ("headZ", ctypes.c_float),
        ("MainPower", ctypes.c_int),
    ]


class FlightData2(ctypes.Structure):
    name = "FalconSharedMemoryArea2"
    _fields_ = [
        ("nozzlePos2", ctypes.c_float),
        ("rpm2", ctypes.c_float),
        ("ftit2", ctypes.c_float),
        ("oilPressure2", ctypes.c_float),
        ("navMode", ctypes.c_byte),
        ("AAUZ", ctypes.c_float),
        ("tacanInfo", ctypes.c_char * 2),
        ("AltCalReading", ctypes.c_int),
        ("altBits", ctypes.c_uint),
        ("powerBits", ctypes.c_uint),
        ("blinkBits", ctypes.c_uint),
        ("cmdsMode", ctypes.c_int),
        ("uhf_panel_preset", ctypes.c_int),
        ("uhf_panel_frequency", ctypes.c_int),
        ("cabinAlt", ctypes.c_float),
        ("hydPressureA", ctypes.c_float),
        ("hydPressureB", ctypes.c_float),
        ("currentTime", ctypes.c_int),
        ("vehicleACD", ctypes.c_short),
        ("VersionNum", ctypes.c_int),
        ("fuelFlow2", ctypes.c_float),
        ("RwrInfo", ctypes.c_char * 512),
        ("lefPos", ctypes.c_float),
        ("tefPos", ctypes.c_float),
        ("vtolPos", ctypes.c_float),
        ("pilotsOnline", ctypes.c_char),
        ("pilotsCallsign", (ctypes.c_char * 12) * 32),
        ("pilotsStatus", ctypes.c_char * 32),
        ("bumpIntensity", ctypes.c_float),
        ("latitude", ctypes.c_float),
        ("longitude", ctypes.c_float),
        ("RTT_size", ctypes.c_ushort * 2),
        ("RTT_area", (ctypes.c_ushort * 7) * 4),
        ("iffBackupMode1Digit1", ctypes.c_char),
        ("iffBackupMode1Digit2", ctypes.c_char),
        ("iffBackupMode3ADigit1", ctypes.c_char),
        ("iffBackupMode3ADigit2", ctypes.c_char),
        ("instrLight", ctypes.c_char),
        ("bettyBits", ctypes.c_uint),
        ("miscBits", ctypes.c_uint),
        ("RALT", ctypes.c_float),
        ("bingoFuel", ctypes.c_float),
        ("caraAlow", ctypes.c_float),
        ("bullseyeX", ctypes.c_float),
        ("bullseyeY", ctypes.c_float),
        ("BMSVersionMajor", ctypes.c_int),
        ("BMSVersionMinor", ctypes.c_int),
        ("BMSVersionMicro", ctypes.c_int),
        ("BMSBuildNumber", ctypes.c_int),
        ("StringAreaSize", ctypes.c_uint),
        ("StringAreaTime", ctypes.c_uint),
        ("DrawingAreaSize", ctypes.c_uint),
        ("turnRate", ctypes.c_float),
        ("floodConsole", ctypes.c_char),
        ("magDeviationSystem", ctypes.c_float),
        ("magDeviationReal", ctypes.c_float),
        ("ecmBits", ctypes.c_uint * 5),
        ("ecmOper", ctypes.c_char),
        ("RWRjammingStatus", ctypes.c_char * 40),
        ("radio2_preset", ctypes.c_int),
        ("radio2_frequency", ctypes.c_int),
        ("iffTransponderActiveCode1", ctypes.c_char),
        ("iffTransponderActiveCode2", ctypes.c_short),
        ("iffTransponderActiveCode3A", ctypes.c_short),
        ("iffTransponderActiveCodeC", ctypes.c_short),
        ("iffTransponderActiveCode4", ctypes.c_short),
    ]


class IntellivibeData(ctypes.Structure):
    name = "FalconIntellivibeSharedMemoryArea"
    _fields_ = [
        ("AAMissileFired", ctypes.c_ubyte),
        ("AGMissileFired", ctypes.c_ubyte),
        ("BombDropped", ctypes.c_ubyte),
        ("FlareDropped", ctypes.c_ubyte),
        ("ChaffDropped", ctypes.c_ubyte),
        ("BulletsFired", ctypes.c_ubyte),
        ("CollisionCounter", ctypes.c_int),
        ("IsFiringGun", ctypes.c_bool),
        ("IsEndFlight", ctypes.c_bool),
        ("IsEjecting", ctypes.c_bool),
        ("In3D", ctypes.c_bool),
        ("IsPaused", ctypes.c_bool),
        ("IsFrozen", ctypes.c_bool),
        ("IsOverG", ctypes.c_bool),
        ("IsOnGround", ctypes.c_bool),
        ("IsExitGame", ctypes.c_bool),
        ("Gforce", ctypes.c_float),
        ("eyex", ctypes.c_float),
        ("eyey", ctypes.c_float),
        ("eyez", ctypes.c_float),
        ("lastdamage", ctypes.c_int),
        ("damageforce", ctypes.c_float),
        ("whendamage", ctypes.c_uint),
    ]


class Strings():
    name = "FalconSharedMemoryAreaString"
    area_size_max = 1024 * 1024
    id = [
        "BmsExe",
        "KeyFile",
        "BmsBasedir",
        "BmsBinDirectory",
        "BmsDataDirectory",
        "BmsUIArtDirectory",
        "BmsUserDirectory",
        "BmsAcmiDirectory",
        "BmsBriefingsDirectory",
        "BmsConfigDirectory",
        "BmsLogsDirectory",
        "BmsPatchDirectory",
        "BmsPictureDirectory",
        "ThrName",
        "ThrCampaigndir",
        "ThrTerraindir",
        "ThrArtdir",
        "ThrMoviedir",
        "ThrUisounddir",
        "ThrObjectdir",
        "Thr3ddatadir",
        "ThrMisctexdir",
        "ThrSounddir",
        "ThrTacrefdir",
        "ThrSplashdir",
        "ThrCockpitdir",
        "ThrSimdatadir",
        "ThrSubtitlesdir",
        "ThrTacrefpicsdir",
        "AcName",
        "AcNCTR",
        "ButtonsFile",
        "CockpitFile",
        "NavPoint",
        "ThrTerrdatadir"
    ]

    def add(self, id, value):
        setattr(self, id, value)


class FalconShakerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Falcon Shaker 1.4")
        self.root.iconbitmap("FalconShaker.ico")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width // 5 * 4}x{screen_height // 3 * 2}")

        self.audio = pyaudio.PyAudio()
        self.current_device_index = None
        self.profile = None
        self.stop_thread = False
        self.in3D = False

        self.flight_events = self.create_flight_events()
        self.setup_ui()
        self.load_settings()
        self.load_profile()
        self.configAudio()

        # Variables used for tracking ownship status
        self.gearPos = None
        self.airBrakePos = None
        self.bombDropped = 0
        self.AAMFired = 0
        self.AGMFired = 0
        self.lastDamage = None
        self.ARConnected = False
        self.Ejected = False

        self.create_update_thread()

    def configAudio(self):
        # Create the audio player
        device = self.device_var.get()
        if device == '':
            # Create on the default sounds device.
            # This stops the app crashing.
            # Crashing is generally considered bad.
            pygame.mixer.pre_init()
            pygame.mixer.init()
        else:
            try:
                pygame.mixer.quit()
                pygame.mixer.pre_init()
                pygame.mixer.init(devicename=device)
            except Exception as e:
                print("It appears that the device ", device, " does not exist. Connecting to default device.")
                pygame.mixer.pre_init()
                pygame.mixer.init()

        # There's a bit going on so...
        pygame.mixer.set_num_channels(20)

        # Define the audio files for each sound/sound grouping.
        self.rpm1Sound = pygame.mixer.Sound(os.path.join('Sound Files', "rpm.wav"))
        self.rpm2Sound = pygame.mixer.Sound(os.path.join('Sound Files', "rpm.wav"))
        self.cannonSound = pygame.mixer.Sound(os.path.join('Sound Files', "Cannon.wav"))
        self.AAMFiredSound = pygame.mixer.Sound(os.path.join('Sound Files', "AAMFiredSound.wav"))
        self.AGMFiredSound = pygame.mixer.Sound(os.path.join('Sound Files', "AGMFiredSound.wav"))
        self.bombDroppedSound = pygame.mixer.Sound(os.path.join('Sound Files', "BombDroppedSound.wav"))
        self.EjectSound = pygame.mixer.Sound(os.path.join('Sound Files', "eject.wav"))
        self.gearTransitionUpSound = pygame.mixer.Sound(os.path.join('Sound Files', "gearTransitionUp.wav"))
        self.gearTransitionDownSound = pygame.mixer.Sound(os.path.join('Sound Files', "gearTransitionDown.wav"))
        self.gearLockUpSound = pygame.mixer.Sound(os.path.join('Sound Files', "gearLockUp.wav"))
        self.gearLockDownSound = pygame.mixer.Sound(os.path.join('Sound Files', "gearLockDown.wav"))

        self.impactDamageSound = pygame.mixer.Sound(os.path.join('Sound Files', "ImpactDamage.wav"))
        self.blastDamageSound = pygame.mixer.Sound(os.path.join('Sound Files', "BlastDamage.wav"))
        self.gForceSound = pygame.mixer.Sound(os.path.join('Sound Files', "gForce.wav"))
        self.stallSound = pygame.mixer.Sound(os.path.join('Sound Files', "stall.wav"))
        self.runwayBumpSound = pygame.mixer.Sound(os.path.join('Sound Files', "RunwayBump.wav"))
        self.ARBumpSound = pygame.mixer.Sound(os.path.join('Sound Files', "RunwayBump.wav"))
        self.airBrakeMoveSound = pygame.mixer.Sound(os.path.join('Sound Files', "AirBrakeMove.wav"))
        self.airBrakeDragSound = pygame.mixer.Sound(os.path.join('Sound Files', "AirBrakeDrag.wav"))

        #  Constant Play Audio Channels
        self.cannonChannel = pygame.mixer.Channel(0)
        self.cannonChannel.set_volume(0)
        self.cannonChannel.play(self.cannonSound, -1)
        self.rpm1Channel = pygame.mixer.Channel(1)
        self.rpm1Channel.set_volume(0)
        self.rpm1Channel.play(self.rpm1Sound, -1)
        self.rpm2Channel = pygame.mixer.Channel(2)
        self.rpm2Channel.set_volume(0)
        self.rpm2Channel.play(self.rpm2Sound, -1)
        self.gForceChannel = pygame.mixer.Channel(9)
        self.gForceChannel.set_volume(0)
        self.gForceChannel.play(self.gForceSound, -1)
        self.stallChannel = pygame.mixer.Channel(10)
        self.stallChannel.set_volume(0)
        self.stallChannel.play(self.stallSound, -1)
        self.airbrakeMoveChannel = pygame.mixer.Channel(12)
        self.airbrakeMoveChannel.set_volume(0)
        self.airbrakeMoveChannel.play(self.airBrakeMoveSound, -1)
        self.airbrakeDragChannel = pygame.mixer.Channel(13)
        self.airbrakeDragChannel.set_volume(0)
        self.airbrakeDragChannel.play(self.airBrakeDragSound, -1)

        # Queued Audio Channels
        self.runwayBumpChannel = pygame.mixer.Channel(3)
        self.gearChannel = pygame.mixer.Channel(4)
        self.damageChannel = pygame.mixer.Channel(5)
        self.AAMChannel = pygame.mixer.Channel(6)
        self.AGMChannel = pygame.mixer.Channel(7)
        self.bombChannel = pygame.mixer.Channel(8)
        self.ARBumpChannel = pygame.mixer.Channel(11)
        self.EjectionChannel = pygame.mixer.Channel(14)

    def setup_ui(self):
        # Left Frame
        left_frame = tk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=50, pady=10)

        # Haptics Audio Output Device Label and Drop Down
        device_label_frame = tk.Frame(left_frame)
        device_label_frame.pack(expand=False, ipadx=52, pady=10)
        tk.Label(device_label_frame, text="Haptics Audio Output Device").pack(side = tk.LEFT)
        self.device_var = tk.StringVar()
        pygame.mixer.init()
        devices = pygame._sdl2.audio.get_audio_device_names()
        pygame.mixer.quit()
        self.device_menu = ttk.Combobox(left_frame, textvariable=self.device_var, width=40, values=devices)
        self.device_menu.pack()
        self.device_menu.bind("<<ComboboxSelected>>", self.on_device_select)

        # # Profile Directory Selection - Not working yet
        # profile_dir_frame = tk.Frame(left_frame)
        # tk.Label(profile_dir_frame, text="Profile Directory").pack(side=tk.LEFT)
        # self.profile_dir_select = tk.Button(profile_dir_frame, text='Select', command=self.get_profile_directory)
        # self.profile_dir_select.pack(side=tk.LEFT)
        # profile_dir_frame.pack(expand=False, ipadx=65, pady=10)
        self.profile_dir_var = tk.StringVar()
        self.profile_dir_var.set('Profiles')
        # self.profile_dir_entry = tk.Entry(left_frame, width=43, textvariable=self.profile_dir_var, state="disabled").pack()


        # Profile Label and Drop Down
        profile_frame = tk.Frame(left_frame)
        tk.Label(profile_frame, text="Profile").pack(side = tk.LEFT)
        profile_frame.pack(expand=False, ipadx=110, pady=10)
        self.profile_var = tk.StringVar()
        self.profiles = os.listdir(self.profile_dir_var.get())
        self.profile_menu = ttk.Combobox(left_frame, textvariable=self.profile_var, width=40, values=self.profiles)
        self.profile_menu.pack()
        self.profile_menu.bind("<<ComboboxSelected>>", self.on_profile_load)

        # Save Button
        self.save_button = tk.Button(left_frame, text="Save", command=self.save_profile)
        self.save_button.pack(side=tk.BOTTOM, pady=5)

        # Quit Button
        self.quit_button = tk.Button(left_frame, text="Quit", command=self.quit_application)
        self.quit_button.pack(side=tk.BOTTOM, pady=5)

        # Right Frame
        right_frame = tk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a Canvas for scrollable area
        self.canvas = tk.Canvas(right_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a vertical scrollbar to the canvas
        self.scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        # Create a Frame to hold all the frames with controls
        self.controls_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.controls_frame, anchor="nw")
        self.controls_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.create_control_frames()

    def create_control_frames(self):
        for i, flight_event in enumerate(self.flight_events):
            frame = tk.Frame(self.controls_frame, borderwidth=1, relief="solid", padx=10, pady=10, width=200,
                             height=100)
            frame.grid(row=i // 5, column=i % 5, padx=10, pady=10, sticky="nsew")

            # Title
            tk.Label(frame, text=flight_event.name, font=("Arial", 10, "bold")).pack(pady=5)

            # Activate Check Button
            tk.Checkbutton(frame, text="Activate", variable=flight_event.active).pack()

            # Volume Slider
            tk.Scale(frame, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume",
                     variable=flight_event.volumeCoefficient).pack()

            # Balance Slider
            tk.Scale(frame, from_=-100, to=100, orient=tk.HORIZONTAL, label="Balance (Not Implemented)",
                     variable=flight_event.balance).pack()

            # Test Button
            tk.Button(frame, text="Test", command=lambda e=flight_event: self.test_sound(e)).pack()

    def create_flight_events(self):
        events = [
            FlightEvent(name='Engine 1 RPM', volumeCoefficient=100, balance=0, fileName='rpm.wav'),
            FlightEvent(name='Engine 2 RPM', volumeCoefficient=100, balance=0, fileName='rpm.wav'),

            FlightEvent(name='Gear Up', volumeCoefficient=100, balance=0, fileName='GearTransitionUp.wav'),
            FlightEvent(name='Gear Down', volumeCoefficient=100, balance=0, fileName='GearTransitionDown.wav'),

            FlightEvent(name='Cannon', volumeCoefficient=100, balance=0, fileName='Cannon.wav'),
            FlightEvent(name='AA Missile Release', volumeCoefficient=100, balance=0, fileName='AAMFiredSound.wav'),
            FlightEvent(name='AG Missile Release', volumeCoefficient=100, balance=0, fileName='AGMFiredSound.wav'),
            FlightEvent(name='Bomb Release', volumeCoefficient=100, balance=0, fileName='BombDroppedSound.wav'),
            FlightEvent(name='Ejection', volumeCoefficient=100, balance=0, fileName='eject.wav'),

            # FlightEvent(name='Jettison (Not Implemented)', volumeCoefficient=100, balance=0, fileName='nope.wav'),

            FlightEvent(name='Mild Damage', volumeCoefficient=100, balance=0, fileName='ImpactDamage.wav'),
            FlightEvent(name='Heavy Damage', volumeCoefficient=100, balance=0, fileName='BlastDamage.wav'),

            FlightEvent(name='G-Force', volumeCoefficient=100, balance=0, fileName='gForce.wav'),
            FlightEvent(name='Stall', volumeCoefficient=100, balance=0, fileName='stall.wav'),
            FlightEvent(name='Tactile Runway', volumeCoefficient=100, balance=0, fileName='RunwayBump.wav'),
            FlightEvent(name='AR Connect/Disconnect', volumeCoefficient=100, balance=0, fileName='RunwayBump.wav'),
            FlightEvent(name='Air Brakes Actuation', volumeCoefficient=100, balance=0, fileName='AirBrakeMove.wav'),
            FlightEvent(name='Air Brakes Turbulence', volumeCoefficient=100, balance=0, fileName='AirBrakeDrag.wav')
        ]
        return events

    def test_sound(self, event):
        event.testSound()

    def update_active(self, event, var):
        event.active = var.get()

    def update_volume(self, event, var):
        event.volumeCoefficient = float(var.get())

    def update_balance(self, event, var):
        event.balance = float(var.get())

    def update_inputVariable(self, event, var):
        event.inputVariable = float(var.get())

    def save_profile(self):
        profile_name = filedialog.asksaveasfilename(initialdir=self.profile_dir_var.get(), defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if profile_name:
            profile_data = {event.name: {
                'active': event.active.get(),
                'volumeCoefficient': event.volumeCoefficient.get(),
                'balance': event.balance.get()
            } for event in self.flight_events}
            with open(profile_name, 'w') as f:
                json.dump(profile_data, f, indent=4)
        self.profiles = os.listdir(self.profile_dir_var.get())
        self.profile_menu['values'] = self.profiles

    def quit_application(self):
        self.stop_thread = True
        self.save_settings()
        pygame.mixer.music.stop()
        self.root.quit()

    def save_settings(self):
        settings = {
            'sound_device': self.device_var.get(),
            'profile_dir_var': self.profile_dir_var.get(),
            'profile': self.profile_var.get()
        }
        with open('set.cfg', 'w') as f:
            json.dump(settings, f, indent=4)

    def get_profile_directory(self):
        self.profile_dir_var.set(askdirectory())


    def load_settings(self):
        if os.path.exists('set.cfg'):
            with open('set.cfg', 'r') as f:
                settings = json.load(f)
                self.device_var.set(settings.get('sound_device', ''))
                # self.profile_dir_var.set(settings.get('profile_dir_var', ''))
                # self.profiles=os.listdir(self.profile_dir_var.get())
                self.profile_var.set(settings.get('profile', ''))

    def load_profile(self):
        profile_name = self.profile_var.get()
        if profile_name:
            with open(os.path.join(self.profile_dir_var.get(), profile_name), 'r') as f:
                profile_data = json.load(f)
                for event in self.flight_events:
                    if event.name in profile_data:
                        data = profile_data[event.name]
                        event.active.set(data.get('active', True))
                        event.volumeCoefficient.set(data.get('volumeCoefficient', 50))
                        event.balance.set(data.get('balance', 0))

    def on_device_select(self, event):
        device_name = self.device_var.get()
        self.configAudio()
        device_index = next((i for i in range(self.audio.get_device_count()) if
                             self.audio.get_device_info_by_index(i)['name'] == device_name), None)
        if device_index is not None:
            self.current_device_index = device_index

    def on_profile_load(self, event):
        self.load_profile()

    def create_update_thread(self):
        self.update_thread = threading.Thread(target=self.update_audio_from_memory)
        self.update_thread.daemon = True
        self.update_thread.start()

    def update_audio_from_memory(self):
        while not self.stop_thread:
            # Refresh from shared mem
            fd = read_shared_memory(FlightData)
            fd2 = read_shared_memory(FlightData2)
            iv = read_shared_memory(IntellivibeData)

            isOnGroundBit = 0x10 # True if on ground
            lightbits = fd.lightBits
            isAirborne = (lightbits & isOnGroundBit) == 0
            is3D = iv.In3D

            # Update Gun Channel
            if iv.IsFiringGun and is3D and self.flight_events[4].active:
                self.cannonChannel.set_volume(
                    self.flight_events[4].get_volumes('l'),
                    self.flight_events[4].get_volumes('r'))
            else:
                self.cannonChannel.set_volume(0)

            # Update RPM1 Channel
            if fd.rpm > 1 and is3D and self.Ejected is False and self.flight_events[0].active.get():
                rpm1mp = (((fd.rpm / 2) - 25) / 100)
                self.rpm1Channel.set_volume(
                    self.flight_events[0].get_volumes('l')*rpm1mp,
                    self.flight_events[0].get_volumes('r')*rpm1mp
                )
            else:
                self.rpm1Channel.set_volume(0)

            # Update RPM2 Channel
            if fd2.rpm2 > 1 and is3D and self.Ejected is False and self.flight_events[1].active.get():
                rpm2mp = (((fd2.rpm2 / 2) - 25) / 100)
                self.rpm2Channel.set_volume(
                    self.flight_events[1].get_volumes('l') * rpm2mp,
                    self.flight_events[1].get_volumes('r') * rpm2mp
                )
            else:
                self.rpm2Channel.set_volume(0)

            # Update RunWay Bump Channel
            if 0.8 > fd2.bumpIntensity > 0.1 and self.runwayBumpChannel.get_busy() is False and iv.In3D \
                    and self.flight_events[13].active.get():
                self.runwayBumpChannel.set_volume(
                    self.flight_events[13].get_volumes('l'),
                    self.flight_events[13].get_volumes('r')
                )
                self.runwayBumpChannel.play(self.runwayBumpSound)

            # Update Landing Gear Channel
            newGearPos = fd.gearPos
            if self.gearPos is None:
                self.gearPos = newGearPos
            else:
                gearPosDiff = self.gearPos - newGearPos
                if is3D:
                    if self.flight_events[3].active.get():
                        # if gear was descending but is now at limit play gear lock down
                        if gearPosDiff < 0.0 and newGearPos == 1 and self.gearLockDownSound.get_num_channels() == 0:
                            self.gearChannel.set_volume(self.flight_events[3].get_volumes('l'), self.flight_events[3].get_volumes('r'))
                            self.gearChannel.play(self.gearLockDownSound)
                        # Gear is descending and descending sound not playing
                        if gearPosDiff < 0.0 and newGearPos != 1 and self.gearTransitionDownSound.get_num_channels() == 0:
                            self.gearChannel.set_volume(self.flight_events[3].get_volumes('l'), self.flight_events[3].get_volumes('r'))
                            self.gearChannel.play(self.gearTransitionDownSound)
                    # Gear was ascending but is now at limit
                    if self.flight_events[2].active:
                        if gearPosDiff > 0.0 and newGearPos == 0 and self.gearLockUpSound.get_num_channels() == 0:
                            self.gearChannel.set_volume(self.flight_events[2].get_volumes('l'), self.flight_events[2].get_volumes('r'))
                            self.gearChannel.play(self.gearLockUpSound)
                        if gearPosDiff > 0.0 and newGearPos != 0 and self.gearTransitionUpSound.get_num_channels() == 0:
                            self.gearChannel.set_volume(self.flight_events[2].get_volumes('l'), self.flight_events[2].get_volumes('r'))
                            self.gearChannel.play(self.gearTransitionUpSound)
            self.gearPos = newGearPos

            # Update Damage Channel
            newDamage = iv.whendamage
            if self.lastDamage is None:
                self.lastDamage = newDamage
            else:
                damageForce = iv.damageforce
                if newDamage != self.lastDamage and is3D:
                    if damageForce <= 50 and self.flight_events[9].active:
                        self.damageChannel.set_volume(self.flight_events[9].get_volumes('l'), self.flight_events[9].get_volumes('r'))
                        self.damageChannel.play(self.impactDamageSound)
                    if damageForce > 50 and self.flight_events[10].active:
                        self.damageChannel.set_volume(self.flight_events[10].get_volumes('l'), self.flight_events[10].get_volumes('r'))
                        self.damageChannel.play(self.blastDamageSound)
                self.lastDamage = newDamage

            # Update AA Missile Channel
            AAMFired = iv.AAMissileFired
            if AAMFired > self.AAMFired and self.flight_events[5].active:
                self.AAMChannel.set_volume(self.flight_events[5].get_volumes('l'), self.flight_events[5].get_volumes('r'))
                self.AAMChannel.play(self.AAMFiredSound)
            self.AAMFired = AAMFired

            # Update AG Missile Channel
            AGMFired = iv.AGMissileFired
            if AGMFired > self.AGMFired and self.flight_events[6].active:
                self.AGMChannel.set_volume(self.flight_events[6].get_volumes('l'), self.flight_events[6].get_volumes('r'))
                self.AGMChannel.play(self.AGMFiredSound)
            self.AGMFired = AGMFired

            # Update Bomb Release Channel
            BombDropped = iv.BombDropped
            if BombDropped > self.bombDropped and self.flight_events[7].active:
                self.bombChannel.set_volume(self.flight_events[7].get_volumes('l'), self.flight_events[7].get_volumes('r'))
                self.bombChannel.play(self.bombDroppedSound)
            self.bombDropped = BombDropped

            # Update G-Force Channel. Assume that we're going to make out at around 10 G
            if self.flight_events[11].active.get() and is3D and self.Ejected is False and (fd.gs < -1.2 or fd.gs > 1.2):
                gForcemp = ((100/9*abs(fd.gs))-(100/9))/100
                self.gForceChannel.set_volume(
                    self.flight_events[11].get_volumes('l')*gForcemp,
                    self.flight_events[11].get_volumes('r')*gForcemp
                )
            else:
                self.gForceChannel.set_volume(0)

            # Update stall channel
            ias = fd.kias
            if self.flight_events[12].active.get() and is3D and self.Ejected is False and isAirborne and ias > 0 and ias < 200:
                if 0 <= ias <= 100:
                    stallM = 1
                elif 100 < ias < 200:
                    stallM = (1 - ((ias - 100)/100))
                else:
                    stallM = 0
                self.stallChannel.set_volume(
                    self.flight_events[12].get_volumes('l')*stallM,
                    self.flight_events[12].get_volumes('r')*stallM
                )
            else:
                self.stallChannel.set_volume(0)


            # Update Refuel Contact/Disengage
            isARDisconnectBit = 0x10000
            isARConnected = (lightbits & isARDisconnectBit) != 0
            if self.ARConnected != isARConnected and self.flight_events[14].active:
                self.ARBumpChannel.set_volume(self.flight_events[14].get_volumes('l'), self.flight_events[14].get_volumes('r'))
                self.ARBumpChannel.play(self.ARBumpSound)
                self.ARConnected = isARConnected

            # Update AirBrake Drag Sound
            newAirbrakePos = fd.speedBrake
            if self.airBrakePos is None:
                self.airBrakePos = newAirbrakePos
            else:
                airBrakeDiff = self.airBrakePos - newAirbrakePos
                if is3D and self.Ejected is False and self.flight_events[14].active.get() and abs(airBrakeDiff) > 0 and self.airBrakeMoveSound.get_num_channels() == 0:
                    self.airbrakeMoveChannel.set_volume(
                        self.flight_events[14].get_volumes('l')
                        , self.flight_events[14].get_volumes('r'))
                    self.airbrakeMoveChannel.play(self.airBrakeMoveSound)
                else: self.airbrakeMoveChannel.stop()
            self.airBrakePos = newAirbrakePos

            # Update Airbrake Drag Channel
            if self.flight_events[16].active.get() and is3D:
                self.airbrakeDragChannel.set_volume(self.flight_events[16].get_volumes('l')*fd.speedBrake
                                                , self.flight_events[16].get_volumes('r')*fd.speedBrake)
            else:
                self.airbrakeDragChannel.set_volume(0)

            # Update Eject Channel
            if self.flight_events[8].active.get() and is3D and self.Ejected is False and iv.IsEjecting:
                self.EjectionChannel.set_volume(self.flight_events[8].get_volumes('l')
                                                , self.flight_events[8].get_volumes('r'))
                self.EjectionChannel.play(self.EjectSound)
            self.Ejected = iv.IsEjecting


            time.sleep(0.1)



def read_shared_memory(structure):
    try:
        sm = mmap.mmap(-1, ctypes.sizeof(structure), structure.name, access=mmap.ACCESS_READ)
        buffer = sm.read(ctypes.sizeof(structure))
        data = structure.from_buffer_copy(buffer)
        sm.close()
        return data
    except Exception as e:
        print("Error reading shared memory '{}': {}".format(structure.name, e))
        return None


def read_shared_memory_strings():
    try:
        sm = mmap.mmap(-1, Strings.area_size_max, Strings.name, access=mmap.ACCESS_READ)
        version_num = struct.unpack('I', sm.read(4))[0]
        num_strings = struct.unpack('I', sm.read(4))[0]
        data_size = struct.unpack('I', sm.read(4))[0]
        instance = Strings()
        for id in Strings.id:
            str_id = struct.unpack('I', sm.read(4))[0]
            str_length = struct.unpack('I', sm.read(4))[0]
            str_data = sm.read(str_length + 1).decode('utf-8').rstrip('\x00')
            instance.add(id, str_data)
        sm.close()
        return instance
    except Exception as e:
        print("Error reading shared memory '{}': {}".format(Strings.name, e))
        return None


if __name__ == "__main__":
    root = tk.Tk()
    app = FalconShakerApp(root)
    root.mainloop()
