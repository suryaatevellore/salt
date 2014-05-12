# -*- coding: utf-8 -*-
'''
    :codeauthor: :email:`Ted Strzalkowski (tedski@gmail.com)`
    :copyright: © 2013 by the SaltStack Team, see AUTHORS for more details
    :license: Apache 2.0, see LICENSE for more details.


    tests.unit.modules.mdadm_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

# Import Salt Testing libs
from salttesting import skipIf, TestCase
from salttesting.helpers import ensure_in_syspath
from salttesting.mock import NO_MOCK, NO_MOCK_REASON, MagicMock, patch
ensure_in_syspath('../../')

# Import salt libs
from salt.modules import mdadm
from salt.exceptions import CommandNotFoundError

mdadm.__salt__ = {}


@skipIf(NO_MOCK, NO_MOCK_REASON)
class MdadmTestCase(TestCase):

    @patch('salt.utils.which', lambda exe: exe)
    def test_create(self):
        mock = MagicMock(return_value='salt')
        with patch.dict(mdadm.__salt__, {'cmd.run': mock}):
            ret = mdadm.create(
                    '/dev/md0', 5,
                    ['/dev/sdb1',
                     '/dev/sdc1',
                     '/dev/sdd1'],
                    test_mode=False,
                    force=True,
                    chunk=256
            )
            self.assertEqual('salt', ret)
            mock.assert_called_once_with(
                    'mdadm -C /dev/md0 -v --chunk=256 --force -l 5 -n 3 '
                    '/dev/sdb1 /dev/sdc1 /dev/sdd1'
            )

    def test_create_test_mode(self):
        mock = MagicMock()
        with patch.dict(mdadm.__salt__, {'cmd.run': mock}):
            ret = mdadm.create(
                    '/dev/md0', 5,
                    ['/dev/sdb1',
                     '/dev/sdc1',
                     '/dev/sdd1'],
                    test_mode=False,
                    force=True,
                    chunk=256,
                    test_mode=True
            )
            self.assertEqual('mdadm -C /dev/md0 -v --chunk=256 --force -l 5 -n 3 '
                    '/dev/sdb1 /dev/sdc1 /dev/sdd1', ret)
            assert not mock.called, 'test mode failed, cmd.run called'

if __name__ == '__main__':
    from integration import run_tests
    run_tests(MdadmTestCase, needs_daemon=False)
