#!/usr/bin/env python3

import argparse
import os
import sys
import csv
import datetime
import networkx as nx
from collections import defaultdict
from typing import Dict, Set, Tuple

def parse_mat_csv(csv_file: str) -> Tuple[Dict[str, int], Dict[str, Set[str]], Dict[str, Set[str]]]:
    """
    Parse Eclipse MAT histogram CSV file and extract class hierarchy and instance counts.
    Returns:
    - class_counts: Dict mapping class names to instance counts
    - class_hierarchy: Dict mapping class names to their parent class names
    - package_hierarchy: Dict mapping package names to their parent package names
    """
    class_counts = defaultdict(int)
    class_hierarchy = defaultdict(set)
    package_hierarchy = defaultdict(set)
    
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        
        for row in reader:
            if len(row) < 2:  # Skip empty or malformed rows
                continue
                
            class_name = row[0].strip()
            count = int(row[1].strip())
            
            # Store class count
            class_counts[class_name] = count
            
            # Build package hierarchy
            parts = class_name.split('.')
            if len(parts) > 1:  # Has a package
                package = '.'.join(parts[:-1])
                class_name = parts[-1]
                
                # Add package to hierarchy
                package_parts = package.split('.')
                for i in range(len(package_parts)):
                    current_package = '.'.join(package_parts[:i+1])
                    if i > 0:
                        parent_package = '.'.join(package_parts[:i])
                        package_hierarchy[current_package].add(parent_package)
                    else:
                        package_hierarchy[current_package].add("root")
    
    return dict(class_counts), dict(class_hierarchy), dict(package_hierarchy)

def build_dag(class_hierarchy: Dict[str, Set[str]], 
             package_hierarchy: Dict[str, Set[str]]) -> nx.DiGraph:
    """
    Build a DAG from class and package hierarchies
    """
    G = nx.DiGraph()
    
    # Add root node
    G.add_node("root")
    
    # Add package nodes and edges
    for package, parents in package_hierarchy.items():
        G.add_node(package)
        if not parents:  # If no parents, connect to root
            G.add_edge("root", package)
        else:
            for parent in parents:
                G.add_edge(parent, package)
    
    # Add class nodes and edges
    for class_name, parents in class_hierarchy.items():
        G.add_node(class_name)
        if not parents:  # If no parents, connect to containing package
            package = ".".join(class_name.split(".")[:-1])
            if package:
                G.add_edge(package, class_name)
            else:
                G.add_edge("root", class_name)
        else:
            for parent in parents:
                G.add_edge(parent, class_name)
    
    return G

def write_items_names(G: nx.DiGraph, output_file: str):
    """
    Write itemsNames.txt file with node IDs and names
    """
    with open(output_file, 'w') as f:
        # Write root node
        f.write("0,root\n")
        
        # Write other nodes with sequential IDs
        for i, node in enumerate(G.nodes(), start=1):
            if node != "root":
                f.write(f"{i},{node}\n")

def write_dag(G: nx.DiGraph, output_file: str):
    """
    Write DAG.txt file with parent-child relationships
    """
    with open(output_file, 'w') as f:
        for u, v in G.edges():
            f.write(f"{u},{v}\n")

def write_snapshots(class_counts: Dict[str, int], 
                   snapshot_name: str,
                   output_file: str):
    """
    Write supportAllSnapshots.txt file with class instance counts
    """
    with open(output_file, 'w') as f:
        for class_name, count in class_counts.items():
            f.write(f"{snapshot_name},{class_name},{count}\n")

def write_snapshot_names(snapshot_name: str, output_file: str):
    """
    Write snapshotNames.txt file with snapshot metadata
    """
    with open(output_file, 'w') as f:
        f.write(f"0,{snapshot_name}\n")

def main():
    parser = argparse.ArgumentParser(description='Convert Eclipse MAT histogram CSV to sca-miner format')
    parser.add_argument('csv_file', help='Input CSV file from Eclipse MAT')
    parser.add_argument('output_dir', help='Output directory for sca-miner files')
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("Parsing MAT CSV file...")
    # Parse CSV file
    class_counts, class_hierarchy, package_hierarchy = parse_mat_csv(args.csv_file)
    
    print("Building DAG...")
    # Build DAG
    G = build_dag(class_hierarchy, package_hierarchy)
    
    print("Generating snapshot name...")
    # Generate snapshot name from timestamp
    snapshot_name = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    print("Writing output files...")
    # Write output files
    write_items_names(G, os.path.join(args.output_dir, "itemsNames.txt"))
    write_dag(G, os.path.join(args.output_dir, "DAG.txt"))
    write_snapshots(class_counts, snapshot_name, 
                   os.path.join(args.output_dir, "supportAllSnapshots.txt"))
    write_snapshot_names(snapshot_name, 
                       os.path.join(args.output_dir, "snapshotNames.txt"))

if __name__ == "__main__":
    main() 