#!/usr/bin/env python3
"""
Lamatic Config Updater

Updates config.yaml with credentials from .env file.

Usage: python update_config.py
"""

import os
import sys
import yaml
from pathlib import Path
from dotenv import load_dotenv


def load_credentials():
    """Load credentials from .env file"""
    env_path = Path(__file__).parent / '.env'
    
    if not env_path.exists():
        print("Error: .env file not found!")
        print("Copy .env.example to .env and fill in your credentials.")
        sys.exit(1)
    
    load_dotenv(env_path)
    
    gemini_credential_id = os.getenv('GEMINI_CREDENTIAL_ID')
    if not gemini_credential_id:
        print("Error: GEMINI_CREDENTIAL_ID not found in .env file!")
        sys.exit(1)
    
    return {
        'gemini_credential_id': gemini_credential_id,
        'gemini_credential_name': os.getenv('GEMINI_CREDENTIAL_NAME'),
        'lamatic_config_id': os.getenv('LAMATIC_CONFIG_ID')
    }


def update_yaml_values(data, credentials):
    """Recursively update YAML data with credentials"""
    updates = 0
    
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'credentialId':
                data[key] = credentials['gemini_credential_id']
                updates += 1
            elif key == 'credential_name' and credentials['gemini_credential_name']:
                data[key] = credentials['gemini_credential_name']
                updates += 1
            elif key == '_configId' and credentials['lamatic_config_id']:
                data[key] = credentials['lamatic_config_id']
                updates += 1
            elif isinstance(value, (dict, list)):
                updates += update_yaml_values(value, credentials)
    
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                updates += update_yaml_values(item, credentials)
    
    return updates


def main():
    """Main function"""
    try:
        # Load credentials
        credentials = load_credentials()
        
        # Load config.yaml
        config_path = Path(__file__).parent / 'config.yaml'
        if not config_path.exists():
            print("Error: config.yaml not found!")
            sys.exit(1)
        
        with open(config_path, 'r', encoding='utf-8') as file:
            config_data = yaml.safe_load(file)
        
        # Update values
        updates = update_yaml_values(config_data, credentials)
        
        # Save updated config
        with open(config_path, 'w', encoding='utf-8') as file:
            yaml.dump(config_data, file, default_flow_style=False, allow_unicode=True)
        
        print(f"Updated {updates} credential values in config.yaml")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
