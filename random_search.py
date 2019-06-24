import json
import multiprocessing
import os
import random
import subprocess

PREFIX='data/'

def generate_params():
    params = {
        'send_enabled': True,
        'max_memo_characters': random.randint(100, 200),
        'tx_sig_limit': random.randint(1, 7),
        'tx_size_cost_per_byte': random.randint(5, 15),
        'sig_verify_cost_ed25519': random.randint(100, 500),
        'sig_verify_cost_secp256k1': random.randint(100, 500),
        'deposit_params_min_deposit': [{'denom': 'stake', 'amount': str(random.randint(1, 1000))}],
        'voting_params_voting_period': 1000**3 * random.randint(1, 2*60*60*24*2),
        'tally_params_quorum': round(random.randint(334, 500) / 1000, 3),
        'tally_params_threshold': round(random.randint(450, 550) / 1000, 3),
        'tally_params_veto': round(random.randint(250, 334) / 1000, 3),
        'unbonding_time': 1000**3 * random.randint(60, 60*60*24*3*2),
        'max_validators': random.randint(1, 250),
        'signed_blocks_window': random.randint(10, 1000),
        'min_signed_per_window': round(random.randint(0, 10) / 10, 1),
        'downtime_jail_duration': 1000**3 * random.randint(60, 60*60*24),
        'slash_fraction_double_sign': round(1 / random.randint(1, 50), 18),
        'slash_fraction_downtime': round(1 / random.randint(1, 200), 18),
        'inflation_rate_change': round(random.randint(0, 99) / 100, 2),
        'inflation': round(random.randint(0, 99) / 100, 2),
        'inflation_max': 0.2,
        'inflation_min': 0.07,
        'goal_bonded': 0.67,
        'community_tax': 0.01 + round(random.randint(0, 30) / 100, 2),
        'base_proposer_reward': 0.01 + round(random.randint(0, 30) / 100, 2),
        'bonus_proposer_reward': 0.01 + round(random.randint(0, 30) / 100, 2),
        'op_weight_deduct_fee': random.randint(2, 20),
        'op_weight_msg_send': random.randint(25, 175),
        'op_weight_single_input_msg_multisend': random.randint(2, 20),
        'op_weight_msg_set_withdraw_address': random.randint(20, 100),
        'op_weight_msg_withdraw_validator_commission': random.randint(20, 100),
        'op_weight_submit_voting_slashing_text_proposal': random.randint(2, 20),
        'op_weight_submit_voting_slashing_community_spend_proposal': random.randint(2, 20),
        'op_weight_submit_voting_slashing_param_change_proposal': random.randint(2, 20),
        'op_weight_msg_deposit': random.randint(25, 400),
        'op_weight_msg_create_validator': random.randint(25, 175),
        'op_weight_msg_edit_validator': random.randint(2, 20),
        'op_weight_msg_delegate': random.randint(25, 175),
        'op_weight_msg_undelegate': random.randint(25, 175),
        'op_weight_msg_begin_redelegate': random.randint(25, 175),
        'op_weight_msg_unjail': random.randint(25, 175)
    }
    for k, v in params.items():
        if k not in ['send_enabled', 'deposit_params_min_deposit', 'max_validators']:
            params[k] = str(v)
    return params

def writej(obj, f_path, overwrite=True):
    if os.path.exists(f_path):
        if overwrite:
            os.remove(f_path)
        else:
            return
    with open(f_path, 'w') as f:
        json.dump(obj, f)

def run_test(seed):
    random.seed(seed)
    params = generate_params()
    params_file = PREFIX + f'{seed}_params.json'
    writej(params, params_file)
    cmd = ' '.join([
        'go test',
        '-mod=readonly',
        'github.com/cosmos/cosmos-sdk/simapp',
        '-run TestFullAppSimulation',
        '-SimulationEnabled=true',
        '-SimulationNumBlocks=100',
        '-SimulationBlockSize=200',
        '-SimulationCommit=true',
        f'-SimulationParams={os.getcwd()}/{params_file}',
        f'-SimulationSeed={seed}',
        '-SimulationPeriod=5',
        '-v' ,'-timeout 24h', '-coverpkg=./...'
    ])
    res = subprocess.run(cmd, shell=True, capture_output=True)
    writej({
        'stderr': res.stderr.decode('utf-8') ,
        'stdout': res.stdout.decode('utf-8')
        },
        PREFIX + f'{seed}_output.json'
    )

if __name__ == '__main__':
    num_runs = 10000
    p = multiprocessing.Pool(multiprocessing.cpu_count())
    p.map(run_test, [random.randint(0, 99999999999) for i in range(num_runs)])
