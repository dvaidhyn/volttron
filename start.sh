rm -rf volttron.log&

volttron -vvv -l volttron.log&

volttron-ctl start --tag API_test_radiothermostatrelay
volttron-ctl start --tag vtime_now
volttron-ctl start --tag actuator
volttron-ctl start --tag driver

volttron-ctl status

tail -f volttron.log
