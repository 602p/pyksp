import threading, urllib2, json, time

def _get_apistrings_read(base, vessel):
	"""This function is called by the background thread, and fetches all subscriptions"""
	strings=vessel.subscriptions
	callstring="api_version=a.version"
	for i in strings:
		callstring+="&"+i+"="+vessel.apistrings_read[i] #Build callstring
	result = json.loads(urllib2.urlopen(base+callstring).read())
	for item in strings:
		try:
			vessel.current_values[item]=result[item]
		except KeyError:
			pass

def _fetch_parallel(base, active_vessel):
	"""this thread is run in the backgroun, and contiunously starts new connection threads"""
	while active_vessel.loop_running: #Exit on command of the ActiveVessel tis is attached to
		t=threading.Thread(target=_get_apistrings_read, args=(base, active_vessel))
		t.start() #Start a thread to read from telemachus
		time.sleep(active_vessel.update_speed)

def _run(command):
	"""Called in background when a command is run"""
	urllib2.urlopen(command)

class ActiveVessel:
	"""OO Interface for the Telemachus API"""

	apistrings_read={ #Index of Nice Name:Telemachus API String
	"pause_state":"p.paused",

	"throttle_status":"f.throttle",
	"rcs_status":"v.rcsValue",
	"sas_status":"v.sasValue",
	"action_group_light":"v.lightValue",
	"action_group_gear":"v.gearValue",
	"action_group_brake":"v.brakeValue",

	"universal_time":"t.universalTime",

	"target_name":"tar.name",
	"target_type":"tar.type",
	"target_distance":"tar.distance",
	"target_relative_velocity":"tar.o.relativeVelocity",
	"target_velocity":"tar.o.velocity",
	"target_periapsis":"tar.o.PeA",
	"target_apoapsis":"tar.o.ApA",
	"target_time_to_apoapsis":"tar.o.timeToAp",
	"target_time_to_periapsis":"tar.o.timeToPe",
	"target_inclination":"tar.o.inclination",
	"target_eccentricity":"tar.o.eccentricity",
	"target_period":"tar.o.period",
	"target_argument_of_periapsis":"tar.o.argumentOfPeriapsis",
	"target_transition_1":"tar.o.timeToTransition1",
	"target_transition_2":"tar.o.timeToTransition2",
	"target_semimajor_axis":"tar.o.sma",
	"target_longitude_ascending_node":"tar.o.lan",
	"target_mean_anomaly":"tar.o.maae",
	"target_time_of_periapsis_passage":"tar.o.timeOfPeriapsisPassage",
	"target_true_anomaly":"tar.o.trueAnomaly",
	"target_orbiting_body":"tar.o.orbitingBody",

	"vessel_velocity":"o.velocity",
	"vessel_periapsis":"o.PeA",
	"vessel_apoapsis":"o.ApA",
	"vessel_time_to_apoapsis":"o.timeToAp",
	"vessel_time_to_periapsis":"o.timeToPe",
	"vessel_inclination":"o.inclination",
	"vessel_eccentricity":"o.eccentricity",
	"vessel_period":"o.period",
	"vessel_argument_of_periapsis":"o.argumentOfPeriapsis",
	"vessel_transition_1":"o.timeToTransition1",
	"vessel_transition_2":"o.timeToTransition2",
	"vessel_semimajor_axis":"o.sma",
	"vessel_longitude_ascending_node":"o.lan",
	"vessel_mean_anomaly":"o.maae",
	"vessel_time_of_periapsis_passage":"o.timeOfPeriapsisPassage",
	"vessel_true_anomaly":"o.trueAnomaly",
	"vessel_orbiting_body":"o.orbitingBody",

	"temperature_sensor":"s.sensor.temp",
	"pressure_sensor":"s.sensor.pres",
	"gravity_sensor":"s.sensor.grav",
	"acceleration_sensor":"s.sensor.acc",

	"vessel_altitude":"v.altitude",
	"vessel_asl_height":"v.heightFromTerrain",
	"vessel_mission_time":"v.missionTime",
	"vessel_surface_velocity":"v.surfaceVelocity",
	"vessel_surface_velocity_x":"v.surfaceVelocityx",
	"vessel_surface_velocity_y":"v.surfaceVelocityy",
	"vessel_surface_velocity_z":"v.surfaceVelocityz",
	"vessel_angular_velocity":"v.angularVelocity",
	"vessel_orbital_velocity":"v.orbitalVelocity",
	"vessel_surface_speed":"v.surfaceSpeed",
	"vessel_vertical_speed":"v.verticalSpeed",
	"vessel_gee_force":"v.geeForce",
	"vessel_atmospheric_density":"v.atmosphericDensity",
	"vessel_longitude":"v.long",
	"vessel_latitude":"v.lat",
	"vessel_dynamic_pressure":"v.dynamicPressure",
	"vessel_name":"v.name",
	"vessel_angle_to_prograde":"v.angleToPrograde",
	"vessel_body":"v.body",
	"vessel_heading":"n.heading",
	"vessel_pitch":"n.pitch",
	"vessel_roll":"n.roll",
	"vessel_heading_raw":"n.rawheading",
	"vessel_pitch_raw":"n.rawpitch",
	"vessel_roll_raw":"m.rawroll",

	"docking_delta_x_angle":"dock.ax",
	"docking_delta_y_angle":"dock.ay",
	"docking_delta_z_angle":"dock.az",
	"docking_delta_x":"dock.x",
	"docking_delta_y":"dock.y",
	"docking_delta_z":"dock.z",

	"resource_lf_max":"r.resourceMax[LiquidFuel]",
	"resource_ec_max":"r.resourceMax[ElectricCharge]",
	"resource_ox_max":"r.resourceMax[Oxidizer]",
	"resource_ia_max":"r.resourceMax[IntakeAir]",
	"resource_sf_max":"r.resourceMax[SolidFuel]",
	"resource_mp_max":"r.resourceMax[MonoPropellant]",
	"resource_xg_max":"r.resourceMax[XenonGas]",

	"resource_lf_current":"r.resource[LiquidFuel]",
	"resource_ec_current":"r.resource[ElectricCharge]",
	"resource_ox_current":"r.resource[Oxidizer]",
	"resource_ia_current":"r.resource[IntakeAir]",
	"resource_sf_current":"r.resource[SolidFuel]",
	"resource_mp_current":"r.resource[MonoPropellant]",
	"resource_xg_current":"r.resource[XenonGas]",
	}

	apistrings_write={ #Map of human name:Telemachus API string for functions
	"action_group_1":"f.ag1",
	"action_group_2":"f.ag2",
	"action_group_3":"f.ag3",
	"action_group_4":"f.ag4",
	"action_group_5":"f.ag5",
	"action_group_6":"f.ag6",
	"action_group_7":"f.ag7",
	"action_group_8":"f.ag8",
	"action_group_9":"f.ag9",
	"action_group_10":"f.ag10",

	"abort":"f.abort",
	"stage":"f.stage",

	"throttle_zero":"f.throttleZero",
	"throttle_full":"f.throttleFull",
	"throttle_up":"f.throttleUp",
	"throttle_down":"f.throttleDown",

	"gear":"f.gear",
	"brake":"f.brake",
	"light":"f.light",

	"sas":"f.sas",
	"rcs":"f.rcs",

	"toggle_fbw":"b.setFbW"
	}

	def __init__(self, url="localhost:8085", base_path="/telemachus/datalink?", update_speed=0.1):
		self.base="http://"+url+base_path #Constuct base call path
		self.subscriptions=[]
		self.current_values={}
		self.update_speed=update_speed
		self.loop_running=False #Keep track of whether background thread should exit
		for i in self.apistrings_read.keys():
			self.current_values[i]=None

	def test_connection(self):
		"""Test a connection to the telemachus server, and throw an HTTPError if it fails"""
		urllib2.urlopen(self.base+'a=v.altitude').read()
		return True

	def raw_run_command(self, string):
		"""Run a command, using a raw querystring"""
		t=threading.Thread(target=_run, args=(self.base+string,))
		t.start()
		return True

	def run_command(self, string):
		"""Run a command, constructing a querystring from the API keys"""
		self.raw_run_command("x="+self.apistrings_write[string])
		return True
        
	def run_command(self, string, value):
		"""Run a command, constructing a querystring from the API keys and set a specific value"""
		self.raw_run_command("x="+self.apistrings_write[string]+"["+value+"]")
		return True

	def set_throttle(self, value):
		"""Set throttle, 1-100"""
		self.raw_run_command("x=v.setThrottle["+str(value)+"]")
		return True

	def set_timewarp(self, value):
		"""Set timeWarp, unknown units. 1-6?"""
		self.raw_run_command("x=v.timeWarp["+str(value)+"]")
		return True

	def set_yaw(self, value):
		"""Set Yaw. 0-1"""
		self.raw_run_command("x=v.setYaw["+str(value)+"]")
		return True

	def set_pitch(self, value):
		"""Set Pitch. 0-1"""
		self.raw_run_command("x=v.setPitch["+str(value)+"]")
		return True

	def set_roll(self, value):
		"""Set Roll. 0-1"""
		self.raw_run_command("x=v.setRoll["+str(value)+"]")
		return True

	def set_6dof(self, pitch, yaw, roll, x, y, z):
		"""Set Pitch, Yaw, Roll, X, Y and Z all at once. 0-1"""
		self.raw_run_command("x=v.setPitchYawRollXYZ["+str(pitch)+","+str(yaw)+","+str(roll)+","+str(x)+","+str(y)+","+str(z)+"]")
		return True

	def subscribe_string(self, string):
		"""Start tracking a value. Returns True if tracking succeded."""
		if not string in self.subscriptions:
			if string in self.apistrings_read.keys():
				self.subscriptions.append(string)
				return True
		return False

	def unsubscribe_string(self, string):
		"""Stop Tracking a value"""
		try:
			del self.subscriptions[self.subscriptions.index(string)]
		except ValueError:
			return

	def subscribe(self, s):
		"""Start tracking a value. Returns True if tracking succeded."""
		return self.subscribe_string(s)
	def unsubscribe(self, s):
		"""Stop Tracking a value"""
		self.unsubscribe_string(s)

	def start(self):
		"""Start running the tracing loop. Nothing bad happens if called multiple times on the same ActiveVessel instance."""
		if not self.loop_running:
			self.loop_running=True
			t=threading.Thread(target=_fetch_parallel, args=(self.base, self))
			t.start()

	def stop(self):
		"""Stop tracking"""
		self.loop_running=False

	def get(self, value):
		"""Shorthand to get a value"""
		return self.current_values[value]

	def run(self, string):
		"""Run a command, mapped from the apistrings_write dictionary"""
		self.run_command(string)

class WrappedVessel(ActiveVessel):
	"""EXPERIMENTAL"""
	def __getattr__(self, *args): #Overload __getattr__ to support doing vessel.vessel_altitude and the like
		if not args[0] in self.subscriptions:
			self.subscribe_string(args[0])
		return self.current_values[args[0]]
	def toggle_ag1(self): #Self-Evident
		self.run_command("action_group_1")
	def toggle_ag2(self): #Self-Evident
		self.run_command("action_group_2")
	def toggle_ag3(self): #Self-Evident
		self.run_command("action_group_3")
	def toggle_ag4(self): #Self-Evident
		self.run_command("action_group_4")
	def toggle_ag5(self): #Self-Evident
		self.run_command("action_group_5")
	def toggle_ag6(self): #Self-Evident
		self.run_command("action_group_6")
	def toggle_ag7(self): #Self-Evident
		self.run_command("action_group_7")
	def toggle_ag8(self): #Self-Evident
		self.run_command("action_group_8")
	def toggle_ag9(self): #Self-Evident
		self.run_command("action_group_9")
	def toggle_ag10(self): #Self-Evident
		self.run_command("action_group_10")
	def toggle_gear(self): #Self-Evident
		self.run_command("gear")
	def toggle_light(self): #Self-Evident
		self.run_command("light")
	def toggle_brake(self): #Self-Evident
		self.run_command("brake")
	def toggle_fbw(self):
		"""Enable/Disable fly-by-wire mode. This needs to be on to set YPR"""
		self.run_command("toggle_fbw")
	def throttle_zero(self): #Self-Evident
		self.run_command("throttle_zero")
	def throttle_full(self): #Self-Evident
		self.run_command("throttle_full")
	def throttle_up(self): #Self-Evident
		self.run_command("throttle_up")
	def throttle_down(self): #Self-Evident
		self.run_command("throttle_down")
	def stage(self): #Self-Evident
		self.run_command("stage")
	def abort(self): #Self-Evident
		self.run_command("abort")
	def sas(self): #Self-Evident
		self.run_command("sas")
	def rcs(self): #Self-Evident
			self.run_command("rcs")