#!/usr/bin/env python
# coding: utf-8

# # 📘 Day 7 – Data Quality & Governance (Great Expectations Fluent API)

# ### **Step 1 – Imports & Context**

# In[1]:


import great_expectations as gx

# Create or load the Data Context
context = gx.get_context()


# ### **Step 2 – Add Datasource (CSV Example)**

# In[3]:


# Add (or reuse) a Pandas Datasource
datasource_name = "pandas_local"
# Prefer checking context.datasources (dict-like) to see if a datasource already exists
if hasattr(context, "datasources") and datasource_name in context.datasources:
    # Reuse existing datasource from the DataContext (this avoids writing a duplicate)
    datasource = context.datasources[datasource_name]
else:
    # Create a new fluent Pandas datasource (will write to Data Context)
    datasource = context.sources.add_pandas(name=datasource_name)

# Register (or get) a CSV file as a Data Asset
asset_name = "transactions"
csv_path = r"C:\Users\mrcha\Desktop\docker\ELT\day7-data-quality-governance\transactions.csv"  # replace with your CSV path
try:
    asset = datasource.get_asset(asset_name)
except Exception:
    # Note: PandasDatasource.add_csv_asset expects 'filepath_or_buffer' as the parameter name
    asset = datasource.add_csv_asset(name=asset_name, filepath_or_buffer=csv_path)

# Create a Batch Request to read the file
batch_request = asset.build_batch_request()


# ### **Step 3 – Create Expectation Suite**

# In[5]:


# Create or get an Expectation Suite in a way that works across DataContext implementations
suite_name = "transactions_suite"
suite = None
# Preferred: context.suites.add (fluent managers)
if hasattr(context, "suites") and hasattr(context.suites, "add"):
    try:
        suite = context.suites.add(suite_name)
    except Exception:
        # If it already exists, many managers provide ways to get it
        try:
            # Some implementations offer a .get method
            suite = context.suites.get(suite_name)
        except Exception:
            suite = None

# Fallback: try DataContext convenience methods
if suite is None:
    if hasattr(context, "create_expectation_suite"):
        try:
            suite = context.create_expectation_suite(suite_name, overwrite_existing=False)
        except Exception:
            try:
                suite = context.get_expectation_suite(suite_name)
            except Exception:
                suite = None
    elif hasattr(context, "add_expectation_suite"):
        try:
            suite = context.add_expectation_suite(suite_name)
        except Exception:
            try:
                suite = context.get_expectation_suite(suite_name)
            except Exception:
                suite = None

# Last resort: construct an ExpectationSuite object and attempt to save it
if suite is None:
    try:
        from great_expectations.core.expectation_suite import ExpectationSuite
        suite = ExpectationSuite(expectation_suite_name=suite_name)
        # Try to persist using common helper if available
        if hasattr(context, "_save_expectation_suite"):
            try:
                context._save_expectation_suite(suite)
            except Exception:
                pass
    except Exception:
        pass

print('Expectation suite ready ->', getattr(suite, 'expectation_suite_name', type(suite)))


# ### **Step 4 – Validate Data**

# In[6]:


# Build a Validator to apply Expectations
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite=suite
)

# Preprocess the data: Convert 'transaction_type' column to uppercase
if "transaction_type" in validator.active_batch.data.dataframe.columns:
    validator.active_batch.data.dataframe["transaction_type"] = validator.active_batch.data.dataframe["transaction_type"].str.upper()

# Example Expectations
validator.expect_column_values_to_not_be_null("user_id")
validator.expect_column_values_to_be_in_set("transaction_type", ["CREDIT", "DEBIT"])
validator.expect_column_values_to_be_between("amount", min_value=0, max_value=10000)

# Save the suite
validator.save_expectation_suite(discard_failed_expectations=False)


# ### **Step 5 – Create a Checkpoint**

# In[7]:


# Create a Checkpoint for automated validation
checkpoint_name = "transactions_checkpoint"
checkpoint = None

# Check if the context supports add_checkpoint
if hasattr(context, "add_checkpoint"):
    try:
        checkpoint = context.add_checkpoint(
            name=checkpoint_name,
            config={
                "class_name": "SimpleCheckpoint",
                "validations": [
                    {
                        "batch_request": batch_request,
                        "expectation_suite_name": suite.expectation_suite_name,
                    }
                ],
            },
        )
    except Exception as e:
        print(f"Error adding checkpoint: {e}")

# Fallback: manually configure a checkpoint
if checkpoint is None:
    try:
        from great_expectations.checkpoint import SimpleCheckpoint
        checkpoint = SimpleCheckpoint(
            name=checkpoint_name,
            data_context=context,
            validations=[
                {
                    "batch_request": batch_request,
                    "expectation_suite_name": suite.expectation_suite_name,
                }
            ],
        )
    except Exception as e:
        print(f"Error creating checkpoint manually: {e}")

# Run the Checkpoint
if checkpoint:
    checkpoint_result = checkpoint.run()
    print("Checkpoint executed successfully.")
else:
    print("Failed to create or execute checkpoint.")


# ### **Step 6 – Review Results**

# In[8]:


# Show validation results summary
print(checkpoint_result.list_validation_results())

# Optionally open Data Docs (if configured)
context.open_data_docs()


# 
# # ✅ What This Does
# - Creates **datasource** → local CSV.  
# - Creates **expectation suite** → data rules.  
# - Runs **validation via checkpoint**.  
# - You’ll see results in console (and Data Docs if enabled).  
# 
# 📌 Next Steps:
# 1. Add more **Expectations** (uniqueness, duplicate detection, ranges).  
# 2. Build **Airflow DAG** to trigger this checkpoint daily.  
# 3. In **Snowflake**, implement RBAC + column masking.  
# 
