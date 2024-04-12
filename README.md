<div align="center">

# **Cybertensor Subnet Template** <!-- omit in toc -->

<p>
  <img alt="GitHub" src="https://img.shields.io/github/license/cybercongress/cybertensor-subnet-template">
  <img alt="Python" src="https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11-blue">
</p>
---

## The Incentivized Internet <!-- omit in toc -->

[Discord](https://discord.gg/xxRfaUStnu) • [Network](https://cyb.ai/) • [Research](https://github.com/cybercongress/cyber/blob/master/computing-the-knowledge/computing-the-knowledge.md)
</div>

---

- [Quickstarter template](#quickstarter-template)
- [Introduction](#introduction)
    - [Example](#example)
- [Installation](#installation)
    - [Before you proceed](#before-you-proceed)
    - [Install](#install)
- [Writing your own incentive mechanism](#writing-your-own-incentive-mechanism)
- [Subnet Links](#subnet-links)
- [License](#license)

---

## Quickstarter template

This template contains all the required installation instructions, scripts, and files and functions for:

- Building cybertensor subnets.
- Creating custom incentive mechanisms and running these mechanisms on the subnets.

In order to simplify the building of subnets, this template abstracts away the complexity of the underlying blockchain
and other boilerplate code. While the default behavior of the template is sufficient for a simple subnet, you should
customize the template in order to meet your specific requirements.
---

## Introduction

**IMPORTANT**: If you are new to cybertensor subnets, read this section before proceeding
to [Installation](#installation) section.

The cybertensor hosts multiple self-contained incentive mechanisms called **subnets**. Subnets are playing fields in
which:

- Subnet miners who produce value, and
- Subnet validators who produce consensus

determine together the proper distribution of tokens for the purpose of incentivizing the creation of value, i.e.,
generating digital commodities, such as intelligence or data.

Each subnet consists of:

- Subnet miners and subnet validators.
- A protocol using which the subnet miners and subnet validators interact with one another. This protocol is part of the
  incentive mechanism.
- The cybertensor API using which the subnet miners and subnet validators interact with cybernet contract
  on space-pussy network. The [cybernet contract](https://github.com/cybercongress/cybernet/) is designed to drive
  these actors: subnet validators and subnet miners, into agreement on who is creating value and what that value is
  worth.

This starter template is split into three primary files. To write your own incentive mechanism, you should edit these
files. These files are:

1. `template/protocol.py`: Contains the definition of the protocol used by subnet miners and subnet validators.
2. `neurons/miner.py`: Script that defines the subnet miner's behavior, i.e., how the subnet miner responds to requests
   from subnet validators.
3. `neurons/validator.py`: This script defines the subnet validator's behavior, i.e., how the subnet validator requests
   information from the subnet miners and determines the scores.

[//]: # (### Example)

[//]: # ()

[//]: # (The Bittensor Subnet 1 for Text Prompting is built using this template.)

[//]: # (See [Bittensor Text-Prompting]&#40;https://github.com/opentensor/text-prompting&#41; for how to configure the files and how to)

[//]: # (add monitoring and telemetry and support multiple miner types. Also see this Subnet 1 in action)

[//]: # (on [Taostats]&#40;https://taostats.io/subnets/netuid-1/&#41; explorer.)

---

## Installation

### Before you proceed

Before you proceed with the installation of the subnet, note the following:

- Use these instructions to run your subnet locally for your development and testing, or on space-pussy mainnet.
- **IMPORTANT**: We **strongly recommend** that you first run your subnet locally and complete your development and
  testing before running the subnet on space-pussy mainnet.
- You can run your subnet either as a subnet owner, or as a subnet validator or as a subnet miner.
- **IMPORTANT:** Make sure you are aware of the minimum compute requirements for your subnet. See
  the [Minimum compute YAML configuration](./min_compute.yml).
- Note that installation instructions differ based on your situation: For example, installing for local development and
  testing will require a few additional steps compared to installing for testnet. Similarly, installation instructions
  differ for a subnet owner vs a validator or a miner.

### Install

- **Running locally**: Follow the step-by-step instructions described in this
  section: [Running Subnet Locally](./docs/running_on_staging.md).
- **Running on space-pussy mainnet**: Follow the step-by-step instructions described in this
  section: [Running on the Main Network](./docs/running_on_mainnet.md).

---

## Writing your own incentive mechanism

As described in [Quickstarter template](#quickstarter-template) section above, when you are ready to write your own
incentive mechanism, update this template repository by editing the following files. The code in these files contains
detailed documentation on how to update the template. Read the documentation in each of the files to understand how to
update the template. There are multiple **TODO**s in each of the files identifying sections you should update. These
files are:

- `template/protocol.py`: Contains the definition of the wire-protocol used by miners and validators.
- `neurons/miner.py`: Script that defines the miner's behavior, i.e., how the miner responds to requests from
  validators.
- `neurons/validator.py`: This script defines the validator's behavior, i.e., how the validator requests information
  from the miners and determines the scores.
- `template/forward.py`: Contains the definition of the validator's forward pass.
- `template/reward.py`: Contains the definition of how validators reward miner responses.

In addition to the above files, you should also update the following files:

- `README.md`: This file contains the documentation for your project. Update this file to reflect your project's
  documentation.
- `CONTRIBUTING.md`: This file contains the instructions for contributing to your project. Update this file to reflect
  your project's contribution guidelines.
- `template/__init__.py`: This file contains the version of your project.
- `setup.py`: This file contains the metadata about your project. Update this file to reflect your project's metadata.
- `docs/`: This directory contains the documentation for your project. Update this directory to reflect your project's
  documentation.

__Note__
The `template` directory should also be renamed to your project name.
---

# Writing your own subnet API
[Docs](docs/writing_api.md)  
[Dummy example](template/api/dummy.py)  
[Storage subnet example](template/api/subnet21.py)  

# Subnet Links

In order to see real-world examples of subnets in-action, see the `subnet_links.py` document or access them from inside 
the `template` package by:
```python
import template
template.SUBNET_LINKS
[{'name': '1', 'url': ''},
 {'name': '2', 'url': ''},
 {'name': '3', 'url': ''},
 {'name': '4', 'url': ''},
 ...
 ]
```

## License

This repository is licensed under the MIT License.

```text
# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# Copyright (c) 2023 Opentensor
# Copyright © 2024 cyber~Congress

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
```
