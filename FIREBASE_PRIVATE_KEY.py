import json

# Load JSON file
with open("serviceAccountKey.json") as f:
    data = json.load(f)

# Convert private key to a single line
fixed_private_key = data["private_key"].replace("\n", " ")

print(fixed_private_key)  # Copy this and paste it into Railway
