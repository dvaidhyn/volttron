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




rm -rf volttron.log&

volttron -vvv -l volttron.log&



volttron-ctl start --tag API_test_radiothermostatrelay
volttron-ctl start --tag API_test_radiothermostatrelay

volttron-ctl start --tag driver
volttron-ctl start --tag driver
#
#
volttron-ctl start --tag actuator
volttron-ctl start --tag actuator
#
# volttron-ctl start --tag schouse_controller


volttron-ctl start --tag tt
volttron-ctl start --tag tt


volttron-ctl start --tag vtime_now

volttron-ctl status

tail -f volttron.log
