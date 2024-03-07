# Running Subnet Locally 
 
This tutorial will guide you through: 
 
- Setting up a local blockchain that is not connected to either cybertensor mainchain (space-pussy)
- Creating a subnet 
- Run your incentive mechanism on the subnet. 
 
## Local blockchain vs local bostrom node  
 
Running a local blockchain is sometimes synonymously referred as running on staging. 
This is **different** from running a node that connects to the cybertensor mainchain.  
 
A localbostrom node will not connect to the mainchain and sync with the mainchain.  
 
Running a local blockchain spins up two authority nodes locally, not connected to any other nodes. 
This tutorial is for running a local blockchain.  
 
## Prerequisites 
 
Before proceeding further, make sure that you have installed cybertensor. See the below instructions: 
 
- [Install `cybertensor`](https://github.com/cybercongress/cybertensor?tab=readme-ov-file#install). 
 
After installing `cybertensor`, proceed as below: 
 
## 1. Run local node 

[Run `localbostrom`](https://github.com/cybercongress/localbostrom?tab=readme-ov-file#get-localbostrom)

## 2. Instantiate cybertensor contract

[Setup `cybertensor` contract](https://github.com/cybercongress/cybertensor?tab=readme-ov-file#dev-setup)

## 3. Install subnet template 
 
`cd` to your project directory and clone the cybertensor subnet template repository: 
 
```bash 
git clone https://github.com/cybercongress/cybertensor-subnet-template.git 
``` 
 
Navigate to the cloned repository: 
 
```bash 
cd cybertensor-subnet-template 
``` 
 
Install the cybertensor-subnet-template Python package: 
 
```bash 
python -m pip install -e . 
``` 
 
## 4. Set up wallets 
 
You will need wallets for the different roles, i.e., subnet owner, subnet validator and subnet miner, in the subnet.  
 
- The owner wallet creates and controls the subnet.  
- The validator and miner will be registered to the subnet created by the owner. This ensures that the validator and miner can run the respective validator and miner scripts. 
 
Create a coldkey for the owner role: 
 
```bash 
ctcli wallet new_coldkey --wallet.name=owner --cwtensor.network=local
``` 
 
Set up the miner's wallets: 
 
```bash 
ctcli wallet new_coldkey --wallet.name=miner --cwtensor.network=local
``` 
 
```bash 
ctcli wallet new_hotkey --wallet.name=miner --wallet.hotkey=default --cwtensor.network=local
``` 
 
Set up the validator's wallets: 
 
```bash 
ctcli wallet new_coldkey --wallet.name=validator --cwtensor.network=local
``` 
```bash 
ctcli wallet new_hotkey --wallet.name=validator --wallet.hotkey=default --cwtensor.network=local
```
 
## 5. Create a subnet 
 
The below commands establish a new subnet on the local chain. The cost will be exactly τ1000.000000000 for the first subnet you create and you'll have to run the faucet several times to get enough tokens. 
 
```bash 
ctcli subnet create --wallet.name=owner --cwtensor.network=local
``` 
 
You will see: 
 
```bash 
>> Your balance is: GBOOT200.000000000 
>> Do you want to register a subnet for GBOOT1000.000000000? [y/n]:  
>> Enter password to unlock key: [YOUR_PASSWORD] 
>> ✅ Registered subnetwork with netuid: 1 
``` 
 
**NOTE**: The local chain will now have a default `netuid` of 1. The second registration will create a `netuid` 2 and so on, until you reach the subnet limit of 8. If you register more than 8 subnets, then a subnet with the least staked BOOT will be replaced by the 9th subnet you register. 
 
## 6. Register keys 
 
Register your subnet validator and subnet miner on the subnet. This gives your two keys unique slots on the subnet. The subnet has a current limit of 128 slots. 
 
Register the subnet miner: 
 
```bash 
ctcli subnet register --wallet.name=miner --wallet.hotkey=default --cwtensor.network=local
``` 
 
Follow the below prompts: 
 
```bash 
>> Enter netuid [1] (1): 1 
>> Continue Registration? [y/n]: y 
>> ✅ Registered 
``` 
 
Register the subnet validator: 
 
```bash 
 
ctcli subnet register --wallet.name=validator --wallet.hotkey=default --cwtensor.network=local
``` 
 
Follow the below prompts: 
 
``` 
>> Enter netuid [1] (1): 1 
>> Continue Registration? [y/n]: y 
>> ✅ Registered 
``` 
 
## 7. Add stake  
 
This step bootstraps the incentives on your new subnet by adding stake into its incentive mechanism. 
 
```bash 
ctcli stake add --wallet.name=validator --wallet.hotkey=default --cwtensor.network=local
``` 
 
Follow the below prompts: 
 
```bash 
>> Stake all GBOOT from account: 'validator'? [y/n]: y 
>> Stake: 
    GBOOT0.000000000 ➡ GBOOT100.000000000 
``` 
 
## 8. Validate key registrations 
 
Verify that both the miner and validator keys are successfully registered: 
 
```bash 
ctcli subnet list --cwtensor.network=local
``` 
 
You will see the `2` entry under `NEURONS` column for the `NETUID` of 1, indicating that you have registered a validator and a miner in this subnet: 
 
```bash 
NETUID  NEURONS  MAX_N   DIFFICULTY  TEMPO  CON_REQ  EMISSION  BURN(GBOOT)   
   1        2     256.00   10.00 M    1000    None     0.00%    GBOOT1.00000  
   2      128     
``` 
 
See the subnet validator's registered details: 
 
```bash 
ctcli wallet overview --wallet.name=validator --cwtensor.network=local
``` 
 
You will see: 
 
``` 
Subnet: 1                                                                                                                                                                 
COLDKEY  HOTKEY   UID  ACTIVE  STAKE(GBOOT)       RANK    TRUST  CONSENSUS  INCENTIVE  DIVIDENDS  EMISSION(ρ)   VTRUST  VPERMIT  UPDATED  AXON  HOTKEY_SS58                     
miner    default  0      True   100.00000      0.00000  0.00000    0.00000    0.00000    0.00000            0  0.00000                14  none  5GTFrsEQfvTsh3WjiEVFeKzFTc2xcf… 
1        1        2            GBOOT100.00000  0.00000  0.00000    0.00000    0.00000    0.00000           ρ0  0.00000                                                          
                                                                          Wallet balance: GBOOT0.0          
``` 
 
See the subnet miner's registered details: 
 
```bash 
ctcli wallet overview --wallet.name=miner --cwtensor.network=local
``` 
 
You will see: 
 
```bash 
Subnet: 1                                                                                                                                                                 
COLDKEY  HOTKEY   UID  ACTIVE  STAKE(GBOOT)     RANK    TRUST  CONSENSUS  INCENTIVE  DIVIDENDS  EMISSION(ρ)   VTRUST  VPERMIT  UPDATED  AXON  HOTKEY_SS58                     
miner    default  1      True       0.00000  0.00000  0.00000    0.00000    0.00000    0.00000            0  0.00000                14  none  5GTFrsEQfvTsh3WjiEVFeKzFTc2xcf… 
1        1        2            GBOOT0.00000  0.00000  0.00000    0.00000    0.00000    0.00000           ρ0  0.00000                                                          
                                                                          Wallet balance: τ0.0    
 
``` 
 
## 9. Run subnet miner and subnet validator 
 
Run the subnet miner and subnet validator. Make sure to specify your subnet parameters. 
 
Run the subnet miner: 
 
```bash 
python neurons/miner.py --netuid=1 --wallet.name=miner --wallet.hotkey=default --logging.debug --cwtensor.network=local
``` 
 
Run the subnet validator: 
 
```bash 
python neurons/validator.py --netuid=1 --wallet.name=validator --wallet.hotkey=default --logging.debug --cwtensor.network=local
``` 
 
## 10. Set weights for your subnet 
 
Register a validator on the root subnet and boost to set weights for your subnet. This is a necessary step to ensure that the subnet is able to receive emmissions. 
 
### Register your validator on the root subnet 
 
```bash 
ctcli root register --wallet.name=validator --wallet.hotkey=default --cwtensor.network=local
``` 
 
### Boost your subnet on the root subnet 
```bash 
ctcli root boost --netuid=1 --increase=1 --wallet.name=validator --wallet.hotkey=default --cwtensor.network=local
``` 
 
## 11. Verify your incentive mechanism 
 
After a few blocks the subnet validator will set weights. This indicates that the incentive mechanism is active. Then after a subnet tempo elapses (360 blocks or 72 minutes) you will see your incentive mechanism beginning to distribute BOOT to the subnet miner.
 
```bash 
ctcli wallet overview --wallet.name=miner --cwtensor.network=local
``` 
 
## Ending your session 
 
To halt your nodes: 
```bash 
# Press CTRL + C keys in the terminal. 
``` 
 
--- 
