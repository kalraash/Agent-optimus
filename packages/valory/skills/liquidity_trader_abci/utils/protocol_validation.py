"""Protocol validation utilities for the liquidity trader skill."""

from typing import List


def validate_and_fix_protocols(
    selected_protocols: List[str], 
    target_investment_chains: List[str],
    available_strategies: dict
) -> List[str]:
    """
    Validate selected protocols and fix invalid ones without resetting to defaults
    
    Args:
        selected_protocols: List of protocols to validate
        target_investment_chains: List of target chains
        available_strategies: Dictionary of available strategies by chain
        
    Returns:
        List of valid protocols
    """
    # Valid protocol names
    VALID_PROTOCOLS = {
        "balancerPool": "balancer_pools_search",
        "uniswapV3": "uniswap_pools_search", 
        "velodrome": "velodrome_pools_search",
        "sturdy": "asset_lending"
    }
    
    # Check if any protocol is invalid
    invalid_protocols = []
    valid_protocols = []
    
    for protocol in selected_protocols:
        if protocol in VALID_PROTOCOLS:
            valid_protocols.append(protocol)
        else:
            invalid_protocols.append(protocol)
    
    # If any invalid protocols found, only fix the invalid ones
    if invalid_protocols:
        # Get default protocols for all target chains as fallback
        default_protocols = []
        for chain in target_investment_chains:
            if chain in available_strategies:
                chain_strategies = available_strategies[chain]
                # Convert strategies to protocol names
                for strategy in chain_strategies:
                    for protocol, strategy_name in VALID_PROTOCOLS.items():
                        if strategy == strategy_name:
                            if protocol not in default_protocols:
                                default_protocols.append(protocol)
        
        # If we have valid protocols, keep them and only add defaults for invalid ones
        if valid_protocols:
            # Add any missing default protocols that aren't already in valid_protocols
            for default_protocol in default_protocols:
                if default_protocol not in valid_protocols:
                    valid_protocols.append(default_protocol)
            return valid_protocols
        else:
            # Only if ALL protocols are invalid, use defaults
            return default_protocols
    
    return valid_protocols 