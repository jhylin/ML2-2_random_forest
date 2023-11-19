import pandas as pd

# Initial code for converting array into df---

# Convert the feature_imp array into dataframe
feature_imp_df = pd.DataFrame(feature_imp)
#feature_imp_df

# Obtain feature names via column names of dataframe
# Rename the index as "features"
feature = X_mp4_df.columns.rename("features")

# Convert the index to dataframe
feature_name_df = feature.to_frame(index = False)

# Concatenate feature_imp_df & feature_name_df
feature_df = pd.concat([feature_imp_df, feature_name_df], axis=1)

# Rename the column for feature importances
feature_df = feature_df.rename(columns = {0: "feature_importances"})

# Sort values of feature importances in descending order
feature_df = feature_df.sort_values("feature_importances", ascending=False)