# Log in
az login --use-device-code

# Create Resource Group and VM
az group create --name NewsResourceGroup --location westeurope
az vm create \
  --resource-group NewsResourceGroup \
  --name insight-vm \
  --image Ubuntu2204 \
  --admin-username azureuser \
  --generate-ssh-keys \
  --size Standard_DS2_v2 \
  --generate-ssh-keys 




# Open required ports
# Starting from 1300 to avoid conflicts with default rules
START_PRIORITY=1300
RESOURCE_GROUP="NewsResourceGroup"
VM_NAME="insight-vm"

PORTS=(22 8080 8000 5173 9090 9088)

for i in "${!PORTS[@]}"; do
  PORT=${PORTS[$i]}
  PRIORITY=$((START_PRIORITY + i))
  echo "Opening port $PORT with priority $PRIORITY..."
  az vm open-port \
    --port $PORT \
    --resource-group "$RESOURCE_GROUP" \
    --name "$VM_NAME" \
    --priority $PRIORITY
done


# Get public IP
PUBLIC_IP=$(az vm show --name insight-vm --resource-group NewsResourceGroup -d --query publicIps -o tsv)
echo "Public IP is: $PUBLIC_IP"

# SCP and SSH
scp -r . azureuser@$PUBLIC_IP:/home/azureuser/
ssh azureuser@$PUBLIC_IP

scp -r ui/insight_africa azureuser@$PUBLIC_IP:/home/azureuser/
