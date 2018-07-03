#!/bin/bash -ex

#
# Deploys Infrastructure for samples
#

# Prompt User for Input
echo "Enter resource group name:"
read rg_name

echo "Enter key vault name:"
read kv_name

echo "Enter location (westus, westus2, eastus, ...):"
read location

# Get Subscription ID
subscription_id=$(az account show --query id -o tsv)

# Get Tenant ID
tenant_id=$(az account show --query tenantId -o tsv)


# Create Resource Group
echo "Creating Resource Group: $rg_name"
az group create --name $rg_name --location $location

# Create KeyVault and save keyvault_url
echo "Creating Key Vault: $kv_name"
keyvault_url=$(az keyvault create --name $kv_name --resource-group $rg_name | grep "vaultUri" | cut -d '"' -f 4)

# Create Service Principal
sp_name=sample-service-principal
echo "Creating Service Principal: $sp_name"
client_secret=$(az ad sp create-for-rbac --name $sp_name --skip-role --scopes="/subscriptions/$subscription_id/resourceGroups/$rg_name" --query password -o tsv)
client_id=$(az ad sp show --id http://$sp_name --query appId --output tsv)
object_id=$(az ad sp show --id http://$sp_name --query objectId --output tsv)

# Assign Key Vault Policy
# The service principal has the follow permissions to keys:
# get, list, update, create, delete, decrypt, encrypt, unwrapKey, wrapKey
az keyvault set-policy --name $kv_name -g $rg_name --object-id $object_id --key-permissions get list update create delete decrypt encrypt unwrapKey wrapKey

# Create Asymetric Key
key_name=sample-key
az keyvault key create -n $key_name -p software --vault-name $kv_name --size 2048
key_version=$(az keyvault key list-versions --name sample-key --vault-name $kv_name | grep "kid" | cut -d '/' -f 6 | cut -d '"' -f 1)

echo -e "\nPlace the following in your config.json:"
echo '{"azure_tenant_id": "'$tenant_id'", "azure_service_principal_client_id":"'$client_id'", "azure_service_principal_secret":"'$client_secret'", "aes_key_length":32, "aes_iv_length":16, "azure_keyvault_url": "'$keyvault_url'", "azure_keyvault_key_name": "'$key_name'", "azure_keyvault_key_version": "'$key_version'"}' | python -m json.tool