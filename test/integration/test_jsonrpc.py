import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from dashd import DashDaemon
from dash_config import DashConfig


def test_dashd():
    config_text = DashConfig.slurp_config_file(config.dash_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'0000003d1edd3bd1d5c485d34c19bd1888d5ff78bc4cf57062975aa043f7c405'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'000006aa6738f56e02859c97ed1256467c29324c0055dc5355bc02d295b88f46'

    creds = DashConfig.get_rpc_creds(config_text, network)
    dashd = DashDaemon(**creds)
    assert dashd.rpc_command is not None

    assert hasattr(dashd, 'rpc_connection')

    # Dash testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = dashd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert dashd.rpc_command('getblockhash', 0) == genesis_hash
