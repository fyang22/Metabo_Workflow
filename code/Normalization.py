import pandas as pd
import numpy as np
import sklearn 

data = pd.read_csv('data/xcms_processed/normalized by - SERRF.csv', delimiter=',')
#print(data.head(5))
data_T = data.T
#print(data_T.head(5))
# get sample group from index
data_T['group'] = data_T.index.str.split('-').str[0]
#print(data_T.head(5))

# def get_group(df, group_name):
#     df['group'] = np.nan
#     for index in df.iterrows():
#         for i in group_name:
#             if i == 'QC':
#                 if i in index.str():
#                     df.loc[index, 'group'] = 'QC'
#             elif i == 'label':
#                 if i in index.str():
#                     df.loc[index,'group'] = 'label'
#             else:
#                 if i in index.str():
#                     df.loc[index,'group'] = i
#     return df

for index in  data_T.iterrows():
    print(index.str())


# def get_subgroup(index_name, group_name):
#     for i in group_name:
#         if i == 'QC':
#             if i in index_name:
#                 return 'QC'
#         elif i == 'label':
#             if i in index_name:
#                 return 'label'
#         else:
#             if i in index_name:
#                 return i + '-' + index_name.split("-")[1]

group = ['QC', 'WT', 'KO', 'label']
# Create a new column to define data categories based on the column names
df_test = get_group(data_T, group)
print(df_test.head(5))

# group_row = pd.Series(data=[get_group(col, group) for col in data.columns],
#                             index=data.columns)

# # Append the category row to the dataframe
# data_subgroup = data._append(subgroup_row, ignore_index=True)
# data_group =data._append(group_row, ignore_index=True)

# # print(data_subgroup.tail(5))
# print(data_group.shape)

# from sklearn.preprocessing import MinMaxScaler
# from sklearn.decomposition import PCA

# X = data.iloc[:, 1:]
# scaler = MinMaxScaler()
# scaler.fit(X)
# X_scaled = scaler.transform(X)
# y = data_group.iloc[-1]
# y = pd.factorize(y)[0]
# pca = PCA(n_components=2)
# pca.fit(X_scaled)
# X_pca = pca.transform(X_scaled)
# df_pca = pd.DataFrame(X_pca, columns=['PC1', 'PC2'])
# labels = ['QC', 'WT', 'KO']
# # print(pca.explained_variance_ratio_)
# # print(pca.singular_values_)
# print(df_pca.head(5))
#print(df_pca.shape)
#print(pca.components_)
# # plot pca
# import matplotlib.pyplot as plt

# colors = ['red', 'blue', 'green']
# fig = plt.figure(figsize=(8, 8))
# for l, c in zip(labels, colors):
#     plt.scatter(df_pca[y == l, 0], df_pca[y == l, 1], c=c, label=l)