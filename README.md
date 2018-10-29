# Custom Data Encryption
[![Build Status](https://travis-ci.org/Microsoft/custom-azure-data-encryption.svg?branch=master)](https://travis-ci.org/Microsoft/custom-azure-data-encryption)

Azure Custom Data Encryption Library provides a light weight SDK for securing your encryption keys with asymetrical RSA keys.

## Installation

TODO: pip command!

## High Level Overview

### Encryption
![High Level Encryption](./images/high_level_encryption.jpg)

### Decryption
![High Level Decryption](./images/high_level_decryption.jpg)

This encryption library seemlessly ties into Azure Key Vault for easy use!

### Quick Start

1. Just authenticate into Azure Key Vault by initializing `AESKeyWrapper`
    ```python
    wrapper = AESKeyWrapper(
        vault = azure_keyvault_url,
        client_id = azure_service_principal_client_id,
        secret = azure_service_principal_secret,
        tenant = azure_tenant_id,
        key_name = azure_keyvault_key_name,
        key_version = azure_keyvault_key_version)
    ```

2. Generate or use your own symmetric key
    ```python
    aes_key = os.urandom(aes_key_length) # 32 bytes
    ```

3. Encrypt your symmetric key and save for later use
    ```python
    wrapper.wrap_aes_key_local(aes_key, wrapper.get_public_key())
    ```

4. Create a cipher and encrypt your data
    ```python
    cipher = AESCipher(wrapper.unwrap_aes_key(encrypted_keys), config.aes_iv_length)
    encrypted_data = cipher.encrypt(sample_data)
    ```

5. Further down the line, you can still use the cipher to decrypt.
    ```python
    cipher.decrypt(encrypted_data)
    ```

## Samples

### Prerequisites
- `python 2.7`
- `virtualenv` for managing python packages between projects.


### Run Samples
1. Clone Repository

2. Create virtual environment using python 2.7 interpreter
    ```bash
    virtualenv --python=/usr/bin/python2.7 sample_virtual_env
    ```

3. Install Dependencies
    ```bash
    pip install -r requirements.txt
    ```
4. Create a copy of `config.example.json` and name it `config.json`
    ```bash
    cp config/config.example.json config/config.json
    ```

5. Log in and use the Azure CLI
    ```bash
    az login
    To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code <Your Code> to authenticate.
    ```

6. Set the subscription you would like to provision the resources on
    ```bash
    az account set -s <Your Subscrition Name or Id>
    ```

7. Provision a `Service Principal` and `Key Vault` by running `deploy.sh`
    - Copy the config generated at the end of the script into `config.json`
    ```bash
    bash scripts/deploy.sh
    Enter resource group name:
    sample-rg
    Enter key vault name:
    sample-kv
    Enter location (westus, westus2, eastus, ...):
    westus

    ...

    place the following in your config.json
    {
        "aes_iv_length": 16,
        "aes_key_length": 32,
        "azure_keyvault_key_name": "sample-key",
        "azure_keyvault_key_version": "<key version guid>",
        "azure_keyvault_url": "https://sample-kv.vault.azure.net",
        "azure_service_principal_client_id": "<service principal client id>",
        "azure_service_principal_secret": "<service principal secret>",
        "azure_tenant_id": "<azure tenant id>"
    }
    ```

8. Run Sample from root directory
    ```bash
    PYTHONPATH=. python samples/encrypt_key.py
    PYTHONPATH=. python samples/simple_encrypt.py
    ```

# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
