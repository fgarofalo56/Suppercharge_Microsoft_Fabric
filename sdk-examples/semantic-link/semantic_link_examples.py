"""
Microsoft Fabric Semantic Link Examples
=======================================

Semantic Link enables integration between Spark/Python notebooks
and Power BI semantic models. This module demonstrates common
patterns for casino analytics.

Prerequisites:
    pip install semantic-link

Usage:
    Run these examples in a Fabric Notebook with Semantic Link enabled.
"""

# =============================================================================
# IMPORTS
# =============================================================================

# Note: sempy is pre-installed in Fabric notebooks
import sempy
import sempy.fabric as fabric
from sempy.fabric import FabricDataFrame
import pandas as pd

# =============================================================================
# SEMANTIC MODEL OPERATIONS
# =============================================================================

def list_datasets():
    """
    List all semantic models (datasets) in the workspace.

    Returns:
        DataFrame with dataset information
    """
    datasets = fabric.list_datasets()
    print(f"Found {len(datasets)} semantic models:")
    for _, ds in datasets.iterrows():
        print(f"  - {ds['Dataset Name']} ({ds['Dataset ID']})")
    return datasets


def get_dataset_info(dataset_name: str):
    """
    Get detailed information about a semantic model.

    Args:
        dataset_name: Name of the semantic model

    Returns:
        Dictionary with model metadata
    """
    # List tables
    tables = fabric.list_tables(dataset_name)
    print(f"\nTables in '{dataset_name}':")
    for _, table in tables.iterrows():
        print(f"  - {table['Name']}")

    # List measures
    measures = fabric.list_measures(dataset_name)
    print(f"\nMeasures in '{dataset_name}':")
    for _, measure in measures.iterrows():
        print(f"  - {measure['Measure Name']}")

    return {
        "tables": tables,
        "measures": measures
    }


# =============================================================================
# READ FROM SEMANTIC MODEL
# =============================================================================

def read_table_from_model(
    dataset_name: str,
    table_name: str,
    columns: list = None
) -> FabricDataFrame:
    """
    Read a table from a semantic model into a FabricDataFrame.

    Args:
        dataset_name: Name of the semantic model
        table_name: Name of the table to read
        columns: Optional list of columns to select

    Returns:
        FabricDataFrame with table data
    """
    df = fabric.read_table(
        dataset=dataset_name,
        table=table_name,
        columns=columns
    )
    print(f"Read {len(df)} rows from {table_name}")
    return df


def execute_dax_query(dataset_name: str, dax_query: str) -> pd.DataFrame:
    """
    Execute a DAX query against a semantic model.

    Args:
        dataset_name: Name of the semantic model
        dax_query: DAX query string

    Returns:
        DataFrame with query results
    """
    result = fabric.evaluate_dax(
        dataset=dataset_name,
        dax_string=dax_query
    )
    return result


# =============================================================================
# CASINO ANALYTICS EXAMPLES
# =============================================================================

def get_daily_revenue_summary(dataset_name: str = "sm_casino_analytics"):
    """
    Get daily revenue summary using DAX.

    Example showing how to query casino KPIs from semantic model.
    """
    dax_query = """
    EVALUATE
    SUMMARIZECOLUMNS(
        'dim_date'[Date],
        "Total Coin In", [Total Coin In],
        "Total Coin Out", [Total Coin Out],
        "Net Revenue", [Net Gaming Revenue],
        "Hold %", [Hold Percentage]
    )
    """

    result = execute_dax_query(dataset_name, dax_query)
    print("Daily Revenue Summary:")
    print(result.head(10))
    return result


def get_machine_performance(
    dataset_name: str = "sm_casino_analytics",
    top_n: int = 10
):
    """
    Get top performing machines using DAX.

    Args:
        dataset_name: Semantic model name
        top_n: Number of machines to return
    """
    dax_query = f"""
    EVALUATE
    TOPN(
        {top_n},
        SUMMARIZECOLUMNS(
            'dim_machine'[machine_id],
            'dim_machine'[floor_location],
            "Revenue", [Net Gaming Revenue],
            "Spins", [Total Spins],
            "Hold %", [Hold Percentage]
        ),
        [Revenue], DESC
    )
    """

    result = execute_dax_query(dataset_name, dax_query)
    print(f"Top {top_n} Machines by Revenue:")
    print(result)
    return result


def get_player_tier_analysis(dataset_name: str = "sm_casino_analytics"):
    """
    Analyze revenue by player loyalty tier.
    """
    dax_query = """
    EVALUATE
    SUMMARIZECOLUMNS(
        'dim_player'[loyalty_tier],
        "Player Count", DISTINCTCOUNT('dim_player'[player_id]),
        "Total Revenue", [Net Gaming Revenue],
        "Avg Revenue Per Player", DIVIDE([Net Gaming Revenue], DISTINCTCOUNT('dim_player'[player_id]))
    )
    """

    result = execute_dax_query(dataset_name, dax_query)
    print("Revenue by Loyalty Tier:")
    print(result)
    return result


# =============================================================================
# WRITE BACK TO LAKEHOUSE
# =============================================================================

def write_analysis_to_lakehouse(
    df: pd.DataFrame,
    lakehouse_name: str,
    table_name: str
):
    """
    Write analysis results back to a Lakehouse table.

    Args:
        df: DataFrame to write
        lakehouse_name: Target lakehouse name
        table_name: Target table name
    """
    # Convert to Spark DataFrame
    spark_df = spark.createDataFrame(df)

    # Write to lakehouse
    spark_df.write \
        .format("delta") \
        .mode("overwrite") \
        .saveAsTable(f"{lakehouse_name}.{table_name}")

    print(f"Wrote {len(df)} rows to {lakehouse_name}.{table_name}")


# =============================================================================
# SEMANTIC MODEL REFRESH
# =============================================================================

def refresh_dataset(dataset_name: str):
    """
    Trigger a refresh of the semantic model.

    Args:
        dataset_name: Name of the semantic model
    """
    fabric.refresh_dataset(dataset=dataset_name)
    print(f"Refresh triggered for '{dataset_name}'")


def get_refresh_status(dataset_name: str):
    """
    Get the refresh status of a semantic model.

    Args:
        dataset_name: Name of the semantic model
    """
    status = fabric.get_refresh_execution_details(dataset=dataset_name)
    print(f"Refresh status for '{dataset_name}':")
    print(status)
    return status


# =============================================================================
# MEASURE MANAGEMENT
# =============================================================================

def create_measure(
    dataset_name: str,
    table_name: str,
    measure_name: str,
    expression: str,
    description: str = None
):
    """
    Create or update a measure in the semantic model.

    Args:
        dataset_name: Semantic model name
        table_name: Table to add measure to
        measure_name: Name of the measure
        expression: DAX expression
        description: Optional description
    """
    # Note: This requires appropriate permissions
    tom_server = fabric.create_tom_server(dataset=dataset_name)

    # Get database
    database = tom_server.Databases[0]
    model = database.Model

    # Find or create measure
    table = model.Tables.Find(table_name)
    measure = table.Measures.Find(measure_name)

    if measure is None:
        # Create new measure
        measure = sempy.tom.Measure()
        measure.Name = measure_name
        table.Measures.Add(measure)

    # Update measure properties
    measure.Expression = expression
    if description:
        measure.Description = description

    # Save changes
    model.SaveChanges()
    print(f"Measure '{measure_name}' saved to '{dataset_name}'")


# =============================================================================
# EXAMPLE WORKFLOW
# =============================================================================

def casino_analytics_workflow():
    """
    Complete example workflow combining multiple Semantic Link operations.
    """
    dataset_name = "sm_casino_analytics"

    print("=" * 50)
    print("CASINO ANALYTICS WORKFLOW")
    print("=" * 50)

    # 1. List available datasets
    print("\n1. Available Semantic Models:")
    datasets = list_datasets()

    # 2. Get dataset info
    print(f"\n2. Dataset Structure for '{dataset_name}':")
    info = get_dataset_info(dataset_name)

    # 3. Query daily revenue
    print("\n3. Daily Revenue Summary:")
    revenue = get_daily_revenue_summary(dataset_name)

    # 4. Top machines
    print("\n4. Top Performing Machines:")
    machines = get_machine_performance(dataset_name, top_n=5)

    # 5. Player tier analysis
    print("\n5. Player Loyalty Analysis:")
    tiers = get_player_tier_analysis(dataset_name)

    # 6. Write results to lakehouse
    print("\n6. Saving Analysis to Lakehouse:")
    write_analysis_to_lakehouse(
        tiers,
        "lh_gold",
        "analysis_player_tiers"
    )

    print("\n" + "=" * 50)
    print("WORKFLOW COMPLETE")
    print("=" * 50)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    # Note: This script should be run in a Fabric Notebook
    casino_analytics_workflow()
