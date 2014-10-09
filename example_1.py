import pyksp,time

vessel=pyksp.ActiveVessel()
vessel.subscribe("vessel_altitude")
vessel.start()
vessel.run_command("sas")
time.sleep(2)
vessel.run_command("stage")
while 1:
	print vessel.get("vessel_altitude")