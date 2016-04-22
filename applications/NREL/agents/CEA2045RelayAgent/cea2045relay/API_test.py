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
# Author(s): Deepthi Vaidhynathan, National Renewable Energy Laboratory
#            Harry Sorensen, National Renewable Energy Laboratory
# Version: 0.1
# Date: April 20, 2016
#
# National Renewable Energy Laboratory is a national laboratory of the
# U.S. Department of Energy, Office of Energy Efficiency and Renewable Energy,
# operated by the Alliance for Sustainable Energy, LLC
# under Contract No. DE-AC36-08GO28308.
#

import unittest
import CEA_2045

cea =  CEA_2045.CEA2045_API("Fake",0)
#cea =  CEA_2045.CEA2045_API("/dev/cu.usbserial-A603Y394",19200)
cea.initialize(1)

class CEA2045TestCase(unittest.TestCase):

    def test_normal(self):
        '''Test normal run'''
        return_query = {}
        cea.send_msg('normal')
        cea.recv_msg()
        cea.recv_msg()
        cea.send_msg('link_ack')
        cea.send_msg('query')
        cea.recv_msg()
        return_query = cea.recv_msg()
        cea.send_msg('link_ack')
        self.assertEqual(CEA_2045.switch_query_response(return_query['opcode2']), "Running Normal")

    def test_emergency(self):
        '''Test emergency command'''
        return_query = {}
        cea.send_msg('emergency')
        cea.recv_msg()
        cea.recv_msg()
        cea.send_msg('link_ack')
        cea.send_msg('query')
        cea.recv_msg()
        return_query = cea.recv_msg()
        cea.send_msg('link_ack')
        self.assertEqual(CEA_2045.switch_query_response(return_query['opcode2']), "Idle Grid")

    def test_shed(self):
        '''Test shed command'''
        return_query = {}
        cea.send_msg('shed')
        cea.recv_msg()
        cea.recv_msg()
        cea.send_msg('link_ack')
        cea.send_msg('query')
        cea.recv_msg()
        return_query = cea.recv_msg()
        cea.send_msg('link_ack')
        self.assertEqual(CEA_2045.switch_query_response(return_query['opcode2']), "Running Curtailed Grid")
