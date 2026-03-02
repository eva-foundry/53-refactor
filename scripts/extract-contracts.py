#!/usr/bin/env python3
"""Extract API contracts and build dependency graph from discovery data."""

import json
from pathlib import Path

def extract_contracts(discovery_file: str, output_dir: str = ".eva") -> dict:
    """Extract OpenAPI contracts and endpoint-container relationships."""
    
    with open(discovery_file, 'r') as f:
        discovery = json.load(f)
    
    # Build endpoint-to-container mapping
    relationships = []
    for feature in discovery.get('features', []):
        for endpoint in feature.get('endpoints', []):
            for container in feature.get('containers', []):
                relationships.append({
                    'feature_id': feature['id'],
                    'endpoint': endpoint,
                    'container': container,
                    'direction': 'read/write'
                })
    
    # Generate OpenAPI-like contracts
    contracts = {
        'openapi': '3.0.0',
        'info': {
            'title': 'EVA-JP-v1.2 API Reference',
            'version': '1.2.0'
        },
        'paths': {}
    }
    
    for endpoint in discovery.get('endpoints', []):
        path = endpoint['path']
        method = endpoint['method'].lower()
        
        if path not in contracts['paths']:
            contracts['paths'][path] = {}
        
        contracts['paths'][path][method] = {
            'summary': endpoint.get('description', ''),
            'operationId': f"{method}_{path.replace('/', '_')}",
            'security': [{'bearer': []}],
            'tags': [endpoint.get('service', 'api')]
        }
    
    # Write outputs
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    with open(output_path / 'contracts.json', 'w') as f:
        json.dump(contracts, f, indent=2)
    
    with open(output_path / 'relationships.json', 'w') as f:
        json.dump(relationships, f, indent=2)
    
    summary = {
        'total_endpoints': len(discovery.get('endpoints', [])),
        'total_containers': len(discovery.get('containers', [])),
        'relationships': len(relationships),
        'api_operations': len(contracts['paths'])
    }
    
    return summary

if __name__ == '__main__':
    summary = extract_contracts('.eva/discovery.json')
    print('[OK] Contracts extracted')
    print(f"  Endpoints: {summary['total_endpoints']}")
    print(f"  Containers: {summary['total_containers']}")
    print(f"  Relationships: {summary['relationships']}")
    print(f"  API Operations: {summary['api_operations']}")
