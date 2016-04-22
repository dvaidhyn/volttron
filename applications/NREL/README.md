##Directory to release VOLTTRON agents

https://github.com/VOLTTRON/volttron/tree/master/applications/nrel

```
 THIS SOFTWARE IS PROVIDED BY Alliance for Sustainable Energy, LLC ''AS IS''
 AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 ARE DISCLAIMED. IN NO EVENT SHALL  Alliance for Sustainable Energy, LLC
 BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
 THE POSSIBILITY OF SUCH DAMAGE.

 This software is an extension of VOLTTRON. The FreeBSD license of the
 VOLTTRON distribution applies to this software.

 Author(s): National Renewable Energy Laboratory
 Version: 0.1
 Date: April 2016

 National Renewable Energy Laboratory is a national laboratory of the
 U.S. Department of Energy, Office of Energy Efficiency and Renewable Energy,
 operated by the Alliance for Sustainable Energy, LLC
 under Contract No. DE-AC36-08GO28308.
```

**Directory structure**

NREL:

    bin:
        functional_test.sh
        start.sh

    agents:
        RadioThermostatRelayAgent
        CEA2045RelayAgent
        VolttimeAgent
        SC_HouseAgent

    docs:
        README.md
        requiremtnts.txt
        topics.txt

    Makefile:

    README.md    


**Agents:**

**CEA-2045:**

The CEA-2045 standard specifies a modular communications interface (MCI) to facilitate communications with residential devices for applications such as energy management. The MCI provides a standard interface for energy management signals and messages to reach devices. Typical devices include energy management controllers, appliances, sensors, and other consumer products. CEA-2045 standard is analogous to the USB standard for the computer electronics; any residential devices that is CEA-2045 compliant should be play-and-plug.

**Radio Thermostat:**

Implementing the most common functions.
Radio Thermostat Company of America, Wi-Fi USNAP Module API, Version 1.3, March 22, 2012. Available on http://lowpowerlab.com/downloads/RadioThermostat_CT50_Honeywell_Wifi_API_V1.3.pdf. Retrieved on April 6, 2016.

**SC_House-Agent:**

Shows example controls for the Relays

**Volttime-Agent:**

Synchronize time

**For information on using the agents refer to docs/README.md**
