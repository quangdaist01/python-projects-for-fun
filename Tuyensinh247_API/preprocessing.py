import pandas as pd

dataset = pd.read_csv("raw_dataset.csv")
dataset

# %%
# Loại bỏ các chương trình đặc biệt
to_drop = []
for index, row in dataset.iterrows():
    if row['Mã trường'] != "QST" and all(x in row['Tên ngành'] for x in ['(', ')']) and 'nhóm ngành' not in row['Tên ngành']:
        to_drop.append(index)
    if row['Mã trường'] == "QST" and \
            (all(x in row['Tên ngành'] for x in ['(']) and \
            ';' not in row['Tên ngành']) or \
            "chương trình" in row['Tên ngành']:
        to_drop.append(index)

new_dataset = dataset.drop(to_drop)
new_dataset.reset_index(drop=True, inplace=True)

# %%
# Bỏ các dữ liệu trùng
new_dataset.drop_duplicates(inplace=True)
new_dataset.reset_index(drop=True,
                          inplace=True)
# %%
# Thêm thông tin điểm cntt của ĐHQT năm 2016. Nguồn: Vietnamnet.com
new_dataset.loc[0, 'Điểm'] = '20.75'
# Chuyển định dạng cột điểm từ str sang float32
new_dataset = new_dataset.astype({'Điểm': 'float32'})
#%%
# Lấy điểm trung bình của 2 ngành Khoa học máy tính và Kỹ thuật máy tính của Bách Khoa năm 2020
new_dataset.loc[21, 'Điểm'] = (new_dataset.loc[20, 'Điểm'] + new_dataset.loc[21, 'Điểm']) /2
new_dataset.drop(20, inplace=True)
new_dataset.reset_index(drop=True,
                          inplace=True)
# Bỏ cột 'tên ngành'
new_dataset.drop(columns=['Tên ngành'], inplace=True)
# Xuất ra file .csv
new_dataset.to_csv('tidy_dataset.csv', index=False)