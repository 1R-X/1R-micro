# micro_core/sync.py

import requests
import yaml
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from micro_core import datastore


# Load peer config
PEERS_FILE = os.path.join(os.path.dirname(__file__), '..', 'peers.yaml')
with open(PEERS_FILE, 'r') as f:
    peers = yaml.safe_load(f).get("peers", [])

def pull_from_peer(peer_url):
    """Fetch all objects from a peer and store them locally."""
    try:
        response = requests.get(f"{peer_url}/objects")
        response.raise_for_status()
        remote_objects = response.json()
        for obj in remote_objects:
            datastore.save_object(obj)
        print(f"Pulled {len(remote_objects)} objects from {peer_url}")
    except Exception as e:
        print(f"Failed to pull from {peer_url}: {e}")

def push_to_peer(peer_url):
    """Send all local objects to a peer."""
    local_objects = datastore.get_all_objects()
    count = 0
    for obj in local_objects:
        try:
            headers = {"Content-Type": "application/json"}
            response = requests.post(f"{peer_url}/objects", json=obj, headers=headers)
            if response.status_code in [200, 201]:
                count += 1
        except Exception as e:
            print(f"Error pushing to {peer_url}: {e}")
    print(f"Pushed {count} objects to {peer_url}")

def pull_all():
    for peer in peers:
        pull_from_peer(peer['base_url'])

def push_all():
    for peer in peers:
        push_to_peer(peer['base_url'])