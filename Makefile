#
# THIS SOFTWARE IS PROVIDED BY Alliance for Sustainable Energy, LLC ''AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL  Alliance for Sustainable Energy, LLC
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
#
# This software is an extension of VOLTTRON. The FreeBSD license of the
# VOLTTRON distribution applies to this software.
#
# Author: Deepthi Vaidhynathan, National Renewable Energy Laboratory
# Version:
# Date:
#
# National Renewable Energy Laboratory is a national laboratory of the
# U.S. Department of Energy, Office of Energy Efficiency and Renewable Energy,
# operated by the Alliance for Sustainable Energy, LLC
# under Contract No. DE-AC36-08GO28308.
#


all: remove API_test_radiothermostatrelay schouse_controller vtime_now actuator driver listener tt

remove:
	rm -rf home_v/*

API_test_radiothermostatrelay:
		volttron-ctl remove --force --tag API_test_radiothermostatrelay
		volttron-pkg package $(AGENTS_HOME)/RadioThermostatRelayAgent/
		volttron-pkg configure $(VOLTTRON_HOME)/packaged/radiothermostatrelayagent-3.0-py2-none-any.whl $(AGENTS_HOME)/RadioThermostatRelayAgent/config
		volttron-ctl install API_test_radiothermostatrelay=$(VOLTTRON_HOME)/packaged/radiothermostatrelayagent-3.0-py2-none-any.whl

schouse_controller:
		volttron-ctl remove --force --tag schouse_controller
		volttron-pkg package $(AGENTS_HOME)/SC_HouseAgent/
		volttron-pkg configure $(VOLTTRON_HOME)/packaged/schouseagent-3.0-py2-none-any.whl $(AGENTS_HOME)/SC_HouseAgent/config
		volttron-ctl install schouse_controller=$(VOLTTRON_HOME)/packaged/schouseagent-3.0-py2-none-any.whl


tt:
		volttron-ctl remove --force --tag tt
		volttron-pkg package $(AGENTS_HOME)/SC_ThermostatAgent/
		volttron-pkg configure $(VOLTTRON_HOME)/packaged/scthermostatagent-3.0-py2-none-any.whl $(AGENTS_HOME)/SC_ThermostatAgent/config
		volttron-ctl install tt=$(VOLTTRON_HOME)/packaged/scthermostatagent-3.0-py2-none-any.whl

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
