import threading, urllib2, json, time

def _get_apistrings_read(base_url, data_dict, subscriptions):
	"""This function is called by the background thread, and fetches all subscriptions"""
	strings=subscriptions
	callstring="universal_time=t.universal_time"
	for i in strings:
		callstring+="&"+i+"="+apistrings_read[i] #Build callstring
	result = json.loads(urllib2.urlopen(base_url+callstring).read())
	for item in strings:
		try:
			data_dict[item]=result[item]
		except KeyError:
			pass
	try:
		data_dict["universal_time"]=result["universal_time"]
	except KeyError:
		pass

def _fetch_parallel(loop_var, update_speed, base_url, data_dict, subscriptions):
	"""This thread is run in the background, and contiunously starts new connection threads"""
	while loop_var: #Exit on command of the ActiveVessel tis is attached to
		t=threading.Thread(target=_get_apistrings_read, args=(base_url, data_dict, subscriptions))
		t.start() #Start a thread to read from telemachus
		time.sleep(update_speed)

def run_command_threaded(command):
	"""Open command in another thread"""
	t=threading.Thread(target=_run_command_threaded_slave, args=(command,))
	t.start()

def _run_command_threaded_slave(command):
	"""Called in background when a command is run thru run_command_threaded"""
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
	"vessel_roll_raw":"n.rawroll",

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
	"api_version":"a.version"
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
	"set_throttle":"f.setThrottle",

	"set_timewarp":"t.timeWarp",
	"set_pitch":"v.setPitch",
	"set_yaw":"v.setYaw",
	"set_roll":"v.setRoll",
	"set_6dof":"v.setPitchYawRollXYZ",

	"gear":"f.gear",
	"brake":"f.brake",
	"light":"f.light",

	"sas":"f.sas",
	"sas_on":"f.sas[1]",
	"sas_off":"f.sas[0]",
	"rcs":"f.rcs",
	"rcs_on":"f.rcs[1]",
	"rcs_off":"f.rcs[0]",

	"enable_fbw":"b.setFbW[1]",
	"disable_fbw":"b.setFbW[0]",
	"set_fbw":"b.setFbW"
	}

	def __init__(self, url="localhost:8085", base_path="/telemachus/datalink?", update_speed=0.1, dont_start=False, dont_check=False):
		"""Use to connect to a telemachus instance. URL is the URI on your network (or internet!) base_path is the URL's HTTP API endpoint. update_speed is the speed (in seconds) to pull new data. If dont_start is ticked, the background loop won't start, otherwise it will start updating immediatly; Useful if instanciating before you want to start using it. If dont_check is ticked, no connection test will be dont, otherwise a check will be made during init; Useful if instanciating before you want to start using it."""
		self.base="http://"+url+base_path #Constuct base call path
		self.subscriptions=[]
		self.current_values={}
		self.update_speed=update_speed
		self.loop_running=False #Keep track of whether background thread should exit
		for i in self.apistrings_read.keys(): #Populate with Nones
			self.current_values[i]=None
		if not dont_check:
			self.test_connection()
		if not dont_start:
			self.start()

	def test_connection(self):
		"""Test a connection to the telemachus server, and throw an HTTPError if it fails"""
		urllib2.urlopen(self.base+'a=v.altitude').read()
		return True

	def _create_qs_params(self, value):
		"""Create a bracket wrapped value set for telemachus API calls. If value is specified as a list, it will be added to the querystring. If not a list, it will be converted to string and added as a single paramerter."""
		value_string=""
		if value!=None:
			if type(value)!=list:
				value_string="["+str(value)+"]"
			else:
				value_string="["
				for i in value:
					value_string+=str(i) #Implicitly convert to string, as python dosent do it automatically on concatination
					if value.index(i)!=len(value)-1:
						value_string+=","
				value_string+="]"
		return value_string

	def raw_run_command(self, stringx, value=None):
		"""Run a command, using a raw querystring. If specified, value will be appended to string"""
		t=threading.Thread(target=_run, args=(self.base+stringx+self._create_qs_params(value),))
		t.start()
		return True

	def run_command(self, stringx, value=None):
		"""Run a command, constructing a querystring from the API keys. If specified, value will be appended to string.""" 
		self.raw_run_command("x="+self.apistrings_write[stringx], value)
		return True

	def set_throttle(self, value):
		"""Set throttle, 0-1"""
		self.run_command("set_throttle",float(value))
		return True

	def set_timewarp(self, value):
		"""Set timeWarp, unknown units. 1-6?"""
		self.run_command("set_timewarp", value)
		return True

	def set_yaw(self, value):
		"""Set Yaw. 0-1"""
		self.run_command("set_yaw", value)
		return True

	def set_pitch(self, value):
		"""Set Pitch. 0-1"""
		self.run_command("set_pitch", value)
		return True

	def set_roll(self, value):
		"""Set Roll. 0-1"""
		self.run_command("set_roll", value)
		return True

	def set_6dof(self, pitch, yaw, roll, x, y, z):
		"""Set Pitch, Yaw, Roll, X, Y and Z all at once. 0-1"""
		self.raw_run_command("set_6dof", [pitch,yaw,roll,x,y,z])
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
		if not args[0] in self.current_values:
			return "ERROR: NOT IMPLEMENTED"
		return self.current_values[args[0]]
	def toggle_ag1(self, boolx=None): #Self-Evident
		"""Set Action Group. Optional boolx: set to this value"""
		if boolx!=None:
			boolx=str(boolx)
		self.run_command("action_group_1", boolx)
	def toggle_ag2(self, boolx=None): #Self-Evident
		"""Set Action Group. Optional boolx: set to this value"""
		if boolx!=None:
			boolx=str(boolx)
		self.run_command("action_group_2", boolx)
	def toggle_ag3(self, boolx=None): #Self-Evident
		"""Set Action Group. Optional boolx: set to this value"""
		if boolx!=None:
			boolx=str(boolx)
		self.run_command("action_group_3", boolx)
	def toggle_ag4(self, boolx=None): #Self-Evident
		"""Set Action Group. Optional boolx: set to this value"""
		if boolx!=None:
			boolx=str(boolx)
		self.run_command("action_group_4", boolx)
	def toggle_ag5(self, boolx=None): #Self-Evident
		"""Set Action Group. Optional boolx: set to this value"""
		if boolx!=None:
			boolx=str(boolx)
		self.run_command("action_group_5", boolx)
	def toggle_ag6(self, boolx=None): #Self-Evident
		"""Set Action Group. Optional boolx: set to this value"""
		if boolx!=None:
			boolx=str(boolx)
		self.run_command("action_group_6", boolx)
	def toggle_ag7(self, boolx=None): #Self-Evident
		"""Set Action Group. Optional boolx: set to this value"""
		if boolx!=None:
			boolx=str(boolx)
		self.run_command("action_group_7", boolx)
	def toggle_ag8(self, boolx=None): #Self-Evident
		"""Set Action Group. Optional boolx: set to this value"""
		if boolx!=None:
			boolx=str(boolx)
		self.run_command("action_group_8", boolx)
	def toggle_ag9(self, boolx=None): #Self-Evident
		"""Set Action Group. Optional boolx: set to this value"""
		if boolx!=None:
			boolx=str(boolx)
		self.run_command("action_group_9", boolx)
	def toggle_ag10(self, boolx=None): #Self-Evident
		"""Set Action Group. Optional boolx: set to this value"""
		if boolx!=None:
			boolx=str(boolx)
		self.run_command("action_group_10", boolx)
	def toggle_gear(self, boolx=None): #Self-Evident
		"""Set Action Group. Optional boolx: set to this value"""
		self.run_command("gear")
	def toggle_light(self, boolx=None): #Self-Evident
		"""Set Action Group. Optional boolx: set to this value"""
		self.run_command("light")
	def toggle_brake(self, boolx=None): #Self-Evident
		"""Set Action Group. Optional boolx: set to this value"""
		self.run_command("brake")
	def enable_fbw(self):
		"""Enable fly-by-wire mode. This needs to be on to set YPR"""
		self.run_command("enable_fbw")
	def disable_fbw(self):
		"""Disable fly-by-wire mode. This needs to be on to set YPR"""
		self.run_command("disable_fbw")
	def set_fbw(self, boolx):
		"""Set FBW. True/False"""
		self.run_command("set_fbw", int(boolx))
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
	def sas(self, boolx=None): #Self-Evident
		"""Set Action Group. Optional boolx: set to this value"""
		if boolx!=None:
			boolx=str(boolx)
		self.run_command("sas", boolx)
	def rcs(self, boolx=None): #Self-Evident
		"""Set Action Group. Optional boolx: set to this value"""
		if boolx!=None:
			boolx=str(boolx)
		self.run_command("rcs", boolx)
