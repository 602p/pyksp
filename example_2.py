import pyksp,time

vessel=pyksp.WrappedVessel()
vessel.subscribe("vessel_altitude")
vessel.start()
vessel.sas()
time.sleep(2)
vessel.stage()
while 1:
	print vessel.vessel_altitude