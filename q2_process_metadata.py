# TODO: Add shebang line: #!/usr/bin/env python3
# Assignment 5, Question 2: Python Data Processing
# Process configuration files for data generation.

import os
import random
import statistics

def parse_config(filepath: str) -> dict:
    """
    Parse config file (key=value format) into dictionary.

    Args:
        filepath: Path to q2_config.txt

    Returns:
        dict: Configuration as key-value pairs

    Example:
        >>> config = parse_config('q2_config.txt')
        >>> config['sample_data_rows']
        '100'
    """
    config = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
    return config
    # TODO: Read file, split on '=', create dict
    pass


def validate_config(config: dict) -> dict:
    """
    Validate configuration values using if/elif/else logic.

    Rules:
    - sample_data_rows must be an int and > 0
    - sample_data_min must be an int and >= 1
    - sample_data_max must be an int and > sample_data_min

    Args:
        config: Configuration dictionary

    Returns:
        dict: Validation results {key: True/False}

    Example:
        >>> config = {'sample_data_rows': '100', 'sample_data_min': '18', 'sample_data_max': '75'}
        >>> results = validate_config(config)
        >>> results['sample_data_rows']
        True
    """
    results = {}

    try:
        rows = int(config.get("sample_data_rows", 0))
        results["sample_data_rows"] = rows > 0
    except ValueError:
        results["sample_data_rows"] = False

    try:
        min_val = int(config.get("sample_data_min", 0))
        results["sample_data_min"] = min_val >= 1
    except ValueError:
        results["sample_data_min"] = False

    try:
        max_val = int(config.get("sample_data_max", 0))
        results["sample_data_max"] = max_val > int(config.get("sample_data_min", 0))
    except ValueError:
        results["sample_data_max"] = False

    return results

    # TODO: Implement with if/elif/else
    pass


def generate_sample_data(filename: str, config: dict) -> None:
    """
    Generate a file with random numbers for testing, one number per row with no header.
    Uses config parameters for number of rows and range.

    Args:
        filename: Output filename (e.g., 'sample_data.csv')
        config: Configuration dictionary with sample_data_rows, sample_data_min, sample_data_max

    Returns:
        None: Creates file on disk

    Example:
        >>> config = {'sample_data_rows': '100', 'sample_data_min': '18', 'sample_data_max': '75'}
        >>> generate_sample_data('sample_data.csv', config)
        # Creates file with 100 random numbers between 18-75, one per row
        >>> import random
        >>> random.randint(18, 75)  # Returns random integer between 18-75
    """
    rows = int(config["sample_data_rows"])
    min_val = int(config["sample_data_min"])
    max_val = int(config["sample_data_max"])

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        for _ in range(rows):
            f.write(f"{random.randint(min_val, max_val)}\n")

    # TODO: Parse config values (convert strings to int)
    # TODO: Generate random numbers and save to file
    # TODO: Use random module with config-specified range
    pass


def calculate_statistics(data: list) -> dict:
    """
    Calculate basic statistics.

    Args:
        data: List of numbers

    Returns:
        dict: {mean, median, sum, count}

    Example:
        >>> stats = calculate_statistics([10, 20, 30, 40, 50])
        >>> stats['mean']
        30.0
    """
    return {
        "count": len(data),
         "sum": sum(data),
         "mean": round(statistics.mean(data), 2),
          "median": round(statistics.median(data), 2)
    }
    # TODO: Calculate stats
    pass


if __name__ == '__main__':
    config = parse_config("q2_config.txt")
    print("Parsed config:", config)

    validation = validate_config(config)
    print("Validation:", validation)

    generate_sample_data("data/sample_data.csv", config)
    print("Generated data/sample_data.csv")

    with open("data/sample_data.csv", "r") as f:
        data = [int(x.strip()) for x in f if x.strip()]
    stats = calculate_statistics(data)
    print("Statistics:", stats)

    os.makedirs("output", exist_ok=True)
    with open("output/statistics.txt", "w", encoding="utf-8") as f:
        for key, value in stats.items():
            f.write(f"{key}={value}\n")
    print("Saved results to output/statistics.txt")

    # TODO: Test your functions with sample data
    # Example:
    # config = parse_config('q2_config.txt')
    # validation = validate_config(config)
    # generate_sample_data('data/sample_data.csv', config)
    # 
    # TODO: Read the generated file and calculate statistics
    # TODO: Save statistics to output/statistics.txt
    pass
