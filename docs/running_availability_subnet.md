# Running Availability Subnet on Mainnet (Space-Pussy network)

This tutorial shows how to use the cybertensor `ctcli` and the cybertensor subnet template to participate in the Availability Subnet. 

[//]: # (**IMPORTANT:** Before attempting to register on mainnet, we strongly recommend that you:)

[//]: # (- run [Running Subnet Locally]&#40;running_on_staging.md&#41;.)

Your incentive mechanisms running on the mainnet are open to anyone. They emit real GPUSSY. Creating these mechanisms incur a `lock_cost` in GPUSSY.

**DANGER**
- Do not expose your private keys.
- Do not use your main wallet.

## Steps

## 1. Install your subnet template

**NOTE: Skip this step if** you already did this during local testing and development.

In your project directory:

```bash
git clone https://github.com/cybercongress/cybertensor-subnet-template.git 
```

Next, `cd` into `cybertensor-subnet-template` repo directory:

```bash
cd cybertensor-subnet-template
```
Create and activate the python virtual environment:
```bash
python3 -m venv venv
```
```bash
. venv/bin/activate
```
Install the cybertensor subnet template package:
```bash
python -m pip install -e . # Install your subnet template package
```

## 2. Create wallets 

Create wallets for subnet owner, subnet validator and for subnet miner.
  
This step creates local coldkey and hotkey pairs for your three identities: subnet owner, subnet validator and subnet miner.

The validator and miner will be registered to the Availability Subnet. 
This ensures that the validator and miner can run the respective validator and miner scripts.

**NOTE**: You can also use existing wallets to register. Creating new keys is shown here for reference.

Create a coldkey and hotkey for the subnet miner wallet:
```bash
ctcli wallet create --wallet.name=miner --wallet.hotkey=default --cwtensor.network=space-pussy [--no_password]
```

Create a coldkey and hotkey for the subnet validator wallet:

```bash
ctcli wallet create --wallet.name=validator --wallet.hotkey=default --cwtensor.network=space-pussy [--no_password]
```

## 3. Transfer PUSSY tokens to your wallets
Get list of your wallet addresses:
```bash
ctcli wallet list
```
Transfer at list 0.1 GPUSSY to your miner and validator coldkey wallets to register in the subnet.
Transfer at any GPUSSY amount to your miner and validator hotkey wallets to include addresses to blockchain.

## 4. (Optional) Register keys 

This step registers your subnet validator and subnet miner keys to the subnet giving them the **first two slots** on the subnet.

Register your miner key to the subnet:

```bash
ctcli subnet register --netuid=1 --wallet.name=miner --wallet.hotkey=default --cwtensor.network=space-pussy
```

Follow the below prompts:

```bash
Your balance is: GPUSSY0.200000000
The cost to register by recycle is GPUSSY0.100000000
Do you want to continue? [y/n] (n): y
Recycle GPUSSY0.100000000 to register on subnet:1? [y/n]: y
Gas used: 304635
📡 Checking Balance...
Balance:
  GPUSSY0.200000000 ➡ GPUSSY0.100000000
✅ Registered
```

Next, register your validator key to the subnet:

```bash
ctcli subnet register --netuid=1 --wallet.name=validator --wallet.hotkey=default --cwtensor.network=space-pussy
```

Follow the below prompts:

```bash
Your balance is: GPUSSY0.200000000
The cost to register by recycle is GPUSSY0.100000000
Do you want to continue? [y/n] (n): y
Recycle GPUSSY0.100000000 to register on subnet:1? [y/n]: y
Gas used: 305564
📡 Checking Balance...
Balance:
  GPUSSY0.200000000 ➡ GPUSSY0.100000000
✅ Registered
```

## 5. Check that your keys have been registered

Check that your subnet validator key has been registered:

```bash
ctcli wallet overview --wallet.name=validator --cwtensor.network=space-pussy
```

The output will be similar to the below:

```bash
Subnet: 1                                                                                                                                                                
COLDKEY     HOTKEY   UID  ACTIVE  STAKE(GPUSSY)     RANK    TRUST  CONSENSUS  INCENTIVE  DIVIDENDS  EMISSION(GPUSSY)   VTRUST  VPERMIT  UPDATED       AXON  HOTKEY
validator   default    8    True        0.00000  0.00000  0.00000    0.00000    0.00000    0.00000                 0  0.00000        *   251566  ...:10000  pussy1…
                       1                0.00000  0.00000  0.00000    0.00000    0.00000                      GPUSSY0  0.00000
                                                                          Wallet balance: GPUSSY0.1
```

Check that your subnet miner has been registered:

```bash
ctcli wallet overview --wallet.name=miner --cwtensor.network=space-pussy
```

The output will be similar to the below:

```bash
Subnet: 1                                                                                                                                                                
COLDKEY  HOTKEY   UID  ACTIVE  STAKE(GPUSSY)     RANK    TRUST  CONSENSUS  INCENTIVE  DIVIDENDS  EMISSION(GPUSSY)   VTRUST  VPERMIT  UPDATED       AXON  HOTKEY
miner    default    9    True        0.00000  0.00000  0.00000    0.00000    0.00000    0.00000                 0  0.00000        *   251566  ...:10000  pussy1…
                    1                0.00000  0.00000  0.00000    0.00000    0.00000                      GPUSSY0  0.00000
                                                                          Wallet balance: GPUSSY0.1
```

## 7. Get emissions flowing

Nominate your validator to the root subnet using the `ctcli`:
```bash
ctcli root nominate --wallet.name=validator --wallet.hotkey=default --cwtensor.network=space-pussy
```
The output will be similar to the below:
```bash
✅ Finalized
2024-04-17 10:15:43.802 |     SUCCESS      | Become Delegate               Finalized: True
Successfully became a delegate on space-pussy
```


## 8. Run subnet miner and subnet validator

Run the subnet miner:

```bash
python neurons/miner.py --netuid=1  --wallet.name=miner --wallet.hotkey=default --logging.debug  --cwtensor.network=space-pussy --axon.pot=9000
```

You will see the below terminal output:

```bash
>> 2024-04-17 10:17:26.604 |       INFO       | Running neuron on subnet: 1 with uid 9 using network: space-pussy
```

Run the subnet validator:

```bash
python neurons/validator.py --netuid 1  --wallet.name=validator --wallet.hotkey=default --logging.debug --cwtensor.network=space-pussy --axon.pot=10000
```

You will see the below terminal output:

```bash
>> 2024-04-17 10:19:08.523 |       INFO       | Running neuron on subnet: 1 with uid 8 using network: space-pussy
```

[//]: # (## 9. [Optional] Register to the root subnet)

[//]: # (or register your validator to the root subnet using the `ctcli`:)

[//]: # ()
[//]: # (```bash)

[//]: # (ctcli root register --wallet.name=validator --wallet.hotkey=default --cwtensor.network=space-pussy)

[//]: # (```)

[//]: # (You will see the below terminal output:)

[//]: # (```bash)

[//]: # ()
[//]: # (```)

[//]: # (Then set your weights for the subnet:)

[//]: # ()
[//]: # (```bash)

[//]: # (ctcli root weights --wallet.name=validator --wallet.hotkey=default --netuid=1 --weights=1  --cwtensor.network=space-pussy)

[//]: # (```)

[//]: # (You will see the below terminal output:)

[//]: # (```bash)

[//]: # (netuids tensor&#40;[1]&#41;  weights tensor&#40;[1.]&#41;)

[//]: # ()
[//]: # (Raw Weights -> Normalized weights: )

[//]: # (        tensor&#40;[1.]&#41; -> )

[//]: # (        tensor&#40;[1.]&#41;)

[//]: # ()
[//]: # (Do you want to set the following root weights?:)

[//]: # (  weights: tensor&#40;[1.]&#41;)

[//]: # (  uids: tensor&#40;[1]&#41;? [y/n]: y)

[//]: # (✅ Finalized)

[//]: # (2024-04-17 10:28:31.616 |     SUCCESS      | Set weights                   Finalized)

[//]: # (```)

## 9. Stopping your nodes

To stop your nodes, press CTRL + C in the terminal where the nodes are running.

---