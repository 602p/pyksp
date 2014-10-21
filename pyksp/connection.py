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
