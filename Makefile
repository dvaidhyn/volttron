all: remove API_test_radiothermostatrelay schouse_controller vtime_now actuator driver listener

remove:
	rm -rf home_v/*

API_test_radiothermostatrelay:
		volttron-ctl remove --force --tag API_test_radiothermostatrelay
		volttron-pkg package $(AGENTS_HOME)/RadioThermostatRelayAgent/
		volttron-pkg configure $(VOLTTRON_HOME)/packaged/radiothermostatrelayagent-3.0-py2-none-any.whl $(AGENTS_HOME)/RadioThermostatRelayAgent/config_api_test
		volttron-ctl install API_test_radiothermostatrelay=$(VOLTTRON_HOME)/packaged/radiothermostatrelayagent-3.0-py2-none-any.whl

schouse_controller:
		volttron-ctl remove --force --tag schouse_controller
		volttron-pkg package $(AGENTS_HOME)/SC_HouseAgent/
		volttron-pkg configure $(VOLTTRON_HOME)/packaged/schouseagent-3.0-py2-none-any.whl $(AGENTS_HOME)/SC_HouseAgent/config
		volttron-ctl install schouse_controller=$(VOLTTRON_HOME)/packaged/schouseagent-3.0-py2-none-any.whl

vtime_now:
		volttron-ctl remove --force --tag vtime_now
		volttron-pkg package $(AGENTS_HOME)/VolttimeAgent
		volttron-pkg configure $(VOLTTRON_HOME)/packaged/volttimeagent-3.0-py2-none-any.whl $(AGENTS_HOME)/VolttimeAgent/config
		volttron-ctl install vtime_now=$(VOLTTRON_HOME)/packaged/volttimeagent-3.0-py2-none-any.whl

actuator:
		volttron-ctl remove --force --tag actuator
		volttron-pkg package $(COM_AGENTS_HOME)/ActuatorAgent
		volttron-pkg configure $(VOLTTRON_HOME)/packaged/actuatoragent-0.3-py2-none-any.whl $(COM_AGENTS_HOME)/ActuatorAgent/config
		volttron-ctl install actuator=$(VOLTTRON_HOME)/packaged/actuatoragent-0.3-py2-none-any.whl

driver:
		volttron-ctl remove --force --tag driver
		volttron-pkg package $(COM_AGENTS_HOME)/MasterDriverAgent
		volttron-pkg configure $(VOLTTRON_HOME)/packaged/master_driveragent-0.1-py2-none-any.whl $(COM_AGENTS_HOME)/MasterDriverAgent/master-driver.agent
		volttron-ctl install driver=$(VOLTTRON_HOME)/packaged/master_driveragent-0.1-py2-none-any.whl


listener:
		volttron-ctl remove --force --tag listener
		volttron-pkg package examples/ListenerAgent
		volttron-pkg configure $(VOLTTRON_HOME)/packaged/listeneragent-3.0-py2-none-any.whl examples/ListenerAgent/config
		volttron-ctl install listener=$(VOLTTRON_HOME)/packaged/listeneragent-3.0-py2-none-any.whl
