# Tutorial 09: Advanced AI/ML

This tutorial covers implementing machine learning solutions for casino analytics using Fabric Data Science.

## Learning Objectives

By the end of this tutorial, you will:

1. Set up ML experiments in Fabric
2. Build a player churn prediction model
3. Implement fraud detection
4. Deploy models for inference
5. Create ML pipelines

## ML Use Cases for Casino

| Use Case | Model Type | Business Value |
|----------|------------|----------------|
| Player Churn | Classification | Retention campaigns |
| Fraud Detection | Anomaly Detection | Loss prevention |
| Player LTV | Regression | Marketing optimization |
| Jackpot Forecasting | Time Series | Capacity planning |

## Prerequisites

- Gold layer tables populated
- Fabric workspace with Data Science capabilities
- Python/PySpark knowledge

## Step 1: Set Up ML Environment

### Create Notebook

1. **+ New** > **Notebook**
2. Name: `ml_player_churn_model`
3. Attach to Lakehouse: `lh_gold`

### Install Libraries (if needed)

```python
# Most ML libraries are pre-installed
# Install additional if needed
%pip install shap xgboost
```

### Import Libraries

```python
import pandas as pd
import numpy as np
from pyspark.sql.functions import *
from pyspark.ml.feature import VectorAssembler, StandardScaler, StringIndexer
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier, GBTClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator
from pyspark.ml import Pipeline
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
import mlflow
import mlflow.spark
```

## Step 2: Player Churn Prediction

### Prepare Training Data

```python
# Read Gold player data
df = spark.table("gold_player_360")

# Define churn label (no visit in 90+ days)
df_ml = df.withColumn(
    "churned",
    when(col("days_since_visit") > 90, 1).otherwise(0)
)

# Select features
feature_columns = [
    "total_gaming_activity",
    "total_theo_win",
    "slot_games_played",
    "slot_coin_in",
    "table_hours_played",
    "total_visits",
    "total_cash_in",
    "total_markers",
    "player_value_score"
]

# Handle missing values
for col_name in feature_columns:
    df_ml = df_ml.fillna(0, subset=[col_name])

print(f"Total records: {df_ml.count()}")
print(f"Churned: {df_ml.filter(col('churned') == 1).count()}")
print(f"Active: {df_ml.filter(col('churned') == 0).count()}")
```

### Encode Categorical Features

```python
# Index loyalty tier
tier_indexer = StringIndexer(
    inputCol="loyalty_tier",
    outputCol="loyalty_tier_idx"
)

df_ml = tier_indexer.fit(df_ml).transform(df_ml)
feature_columns.append("loyalty_tier_idx")
```

### Create Feature Vector

```python
# Assemble features
assembler = VectorAssembler(
    inputCols=feature_columns,
    outputCol="features_raw"
)

# Scale features
scaler = StandardScaler(
    inputCol="features_raw",
    outputCol="features",
    withStd=True,
    withMean=True
)
```

### Split Data

```python
# Train/test split
train_df, test_df = df_ml.randomSplit([0.8, 0.2], seed=42)

print(f"Training: {train_df.count()}")
print(f"Testing: {test_df.count()}")
```

### Train Model

```python
# Start MLflow experiment
mlflow.set_experiment("player_churn_prediction")

with mlflow.start_run(run_name="gradient_boosted_trees"):
    # Create pipeline
    gbt = GBTClassifier(
        labelCol="churned",
        featuresCol="features",
        maxIter=50,
        maxDepth=5
    )

    pipeline = Pipeline(stages=[assembler, scaler, gbt])

    # Train
    model = pipeline.fit(train_df)

    # Predict
    predictions = model.transform(test_df)

    # Evaluate
    evaluator = BinaryClassificationEvaluator(
        labelCol="churned",
        rawPredictionCol="rawPrediction",
        metricName="areaUnderROC"
    )
    auc = evaluator.evaluate(predictions)

    # Log metrics
    mlflow.log_metric("auc_roc", auc)
    mlflow.log_param("max_depth", 5)
    mlflow.log_param("max_iter", 50)

    # Log model
    mlflow.spark.log_model(model, "churn_model")

    print(f"AUC-ROC: {auc:.4f}")
```

### Feature Importance

```python
# Get feature importance from GBT model
gbt_model = model.stages[-1]
importances = gbt_model.featureImportances.toArray()

# Create importance dataframe
importance_df = pd.DataFrame({
    "feature": feature_columns,
    "importance": importances
}).sort_values("importance", ascending=False)

print("\nFeature Importance:")
print(importance_df.to_string(index=False))
```

## Step 3: Fraud Detection (Anomaly Detection)

### Prepare Transaction Data

```python
# Read financial transactions
df_txn = spark.table("lh_silver.silver_financial_reconciled")

# Aggregate by player/day
df_daily = df_txn.groupBy(
    "player_id",
    to_date("transaction_timestamp").alias("txn_date")
).agg(
    count("*").alias("transaction_count"),
    sum("amount").alias("total_amount"),
    avg("amount").alias("avg_amount"),
    max("amount").alias("max_amount"),
    countDistinct("cage_location").alias("unique_cages"),
    sum(when(col("amount").between(8000, 9999), 1).otherwise(0)).alias("near_ctr_count")
)
```

### Isolation Forest for Anomaly Detection

```python
from sklearn.ensemble import IsolationForest

# Convert to pandas for sklearn
pdf = df_daily.toPandas()

# Features for anomaly detection
anomaly_features = [
    "transaction_count",
    "total_amount",
    "avg_amount",
    "max_amount",
    "unique_cages",
    "near_ctr_count"
]

X = pdf[anomaly_features].fillna(0)

# Train Isolation Forest
iso_forest = IsolationForest(
    contamination=0.05,  # Expected 5% anomalies
    random_state=42,
    n_estimators=100
)

pdf["anomaly_score"] = iso_forest.fit_predict(X)
pdf["is_anomaly"] = (pdf["anomaly_score"] == -1).astype(int)

# Anomalies found
anomalies = pdf[pdf["is_anomaly"] == 1]
print(f"Anomalies detected: {len(anomalies)}")
print(f"Anomaly rate: {len(anomalies) / len(pdf) * 100:.2f}%")
```

### Review Anomalies

```python
# Show suspicious patterns
print("\nPotential Structuring Patterns:")
structuring = anomalies[anomalies["near_ctr_count"] >= 2]
print(structuring[["player_id", "txn_date", "transaction_count", "total_amount", "near_ctr_count"]])
```

## Step 4: Model Registry

### Register Model

```python
# Register the best model
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Get the run ID
run_id = mlflow.active_run().info.run_id

# Register model
model_uri = f"runs:/{run_id}/churn_model"
model_details = mlflow.register_model(model_uri, "PlayerChurnModel")

print(f"Model registered: {model_details.name}")
print(f"Version: {model_details.version}")
```

### Transition to Production

```python
# Transition to production stage
client.transition_model_version_stage(
    name="PlayerChurnModel",
    version=model_details.version,
    stage="Production"
)
```

## Step 5: Batch Scoring Pipeline

### Create Scoring Notebook

```python
# Load production model
model = mlflow.spark.load_model("models:/PlayerChurnModel/Production")

# Score all players
df_current = spark.table("gold_player_360")

# Make predictions
predictions = model.transform(df_current)

# Select relevant columns
scored_players = predictions.select(
    "player_id",
    "loyalty_tier",
    "player_value_score",
    col("probability").getItem(1).alias("churn_probability"),
    col("prediction").alias("churn_prediction")
)

# Save scores
scored_players.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("ml_player_churn_scores")

print(f"Scored {scored_players.count()} players")
```

### Create High-Risk Report

```python
# High-risk VIP players
high_risk_vip = scored_players.filter(
    (col("churn_probability") > 0.7) &
    (col("player_value_score") > 100)
).orderBy(col("churn_probability").desc())

print("High-Risk VIP Players Requiring Intervention:")
display(high_risk_vip.limit(20))
```

## Step 6: Real-Time Inference (Optional)

### Deploy as API

For real-time scoring, deploy model to:
1. **Azure ML Endpoint** (external)
2. **Fabric API** (coming soon)

### Example: Azure ML Deployment

```python
# Export model for Azure ML
import joblib

# For sklearn models
joblib.dump(iso_forest, "fraud_detection_model.pkl")

# Register in Azure ML
# (Use Azure ML SDK to deploy as real-time endpoint)
```

## Step 7: ML Pipeline Automation

### Create Scheduled Notebook

```python
# %% Parameters
# ||||||||||||||||||||||||||||||||||
process_date = ""  # Will be set by pipeline
full_retrain = False
# ||||||||||||||||||||||||||||||||||

# Determine if we need to retrain
from datetime import datetime, timedelta

last_train = spark.sql("""
    SELECT MAX(training_date) as last_train
    FROM ml_model_metadata
    WHERE model_name = 'PlayerChurnModel'
""").first()["last_train"]

days_since_train = (datetime.now() - last_train).days if last_train else 999

if full_retrain or days_since_train > 30:
    print("Retraining model...")
    # Run training code
else:
    print(f"Using existing model (trained {days_since_train} days ago)")
    # Run scoring only
```

### Pipeline Integration

Add to Data Factory pipeline:
1. **Notebook activity**: `ml_player_churn_model`
2. **Schedule**: Weekly retraining, daily scoring
3. **On failure**: Alert data science team

## Validation Checklist

- [ ] MLflow experiment created
- [ ] Churn model trained with good AUC
- [ ] Fraud detection running
- [ ] Model registered in MLflow
- [ ] Batch scoring automated
- [ ] Results saved to Gold layer

## Best Practices

1. **Version everything** - Data, code, models
2. **Monitor performance** - Track model drift
3. **Validate predictions** - Compare to actual outcomes
4. **Document assumptions** - Business rules in models
5. **Test before production** - A/B testing if possible

## Troubleshooting

### Model Performance Degraded

1. Check for data drift
2. Validate feature distributions
3. Retrain with recent data

### Memory Issues

1. Use Spark for large datasets
2. Sample for development
3. Increase cluster size for training

## Next Steps

You've completed the tutorial series! Review the [POC Agenda](../../poc-agenda/README.md) for workshop preparation.

## Resources

- [Fabric Data Science](https://learn.microsoft.com/fabric/data-science/)
- [MLflow in Fabric](https://learn.microsoft.com/fabric/data-science/mlflow)
- [Spark ML Library](https://spark.apache.org/docs/latest/ml-guide.html)
- [scikit-learn](https://scikit-learn.org/)
