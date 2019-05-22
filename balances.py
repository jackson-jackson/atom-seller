import requests


ico_account = 'cosmos1f0kwe42k9xdmlxt939m6nq7h9shj0rygnldusg'
secure_ledger = 'cosmos1rpw2pc2psn87jp9eum5esnpfqmymd9nn7ljd2c'
mcv_account = 'cosmos1k447djp2qrfk8pl44vd02qdlld2asjeeyxj94j'

addresses_list = [ico_account, secure_ledger, mcv_account]


#get rewards for each account
def get_total_rewards(addresses_list):
    total = []
    for address in addresses_list:
        rewards_url = f'https://stargate.cosmos.network/distribution/delegators/{address}/rewards'
        rewards = requests.get(rewards_url) 
        rewards_json = rewards.json()  
        total.append(float(rewards_json[0]['amount']))
    return sum(total)


#get total staked for each account
def get_total_staked(addresses_list):
    total = []
    for address in addresses_list:
        staked_url = f'https://stargate.cosmos.network/staking/delegators/{address}/delegations'
        staked = requests.get(staked_url)
        staked_json = staked.json()
        total.append(float(staked_json[0]['shares']))
    return sum(total)


#get total available balance for each account
def get_available_balances(addresses_list):
    total = []
    for address in addresses_list:
        available_balance_url = f'https://stargate.cosmos.network/bank/balances/{address}'
        available = requests.get(available_balance_url)
        available_json = available.json()
        total.append(float(available_json[0]['amount']))
    return sum(total)


total_rewards = round(get_total_rewards(addresses_list) / 1000000, 8)
total_staked = round(get_total_staked(addresses_list) / 1000000, 8)
total_available = round(get_available_balances(addresses_list) / 1000000, 8)

grand_total = total_rewards + total_staked + total_available

print(f"Total Rewards: {total_rewards}")
print(f"Total Staked: {total_staked}")
print(f"Total Available: {total_available}")
print("")
print(f"Grand Total: {round(grand_total, 8)} ATOM")