import numpy as np
from scipy.interpolate import interp1d
import pandas as pd
from scipy import interpolate
def noisuy_hw(mucnuoc,cotH,cotw):
    df = pd.read_excel('data/Thongso.xlsx',sheet_name='QH')
    df.columns = df.loc[0]
    df = df.iloc[4:,:]   
    df = df.dropna(subset=[cotH])
    # Tạo một hàm nội suy spline
    spline = interpolate.InterpolatedUnivariateSpline(df[cotH], df[cotw])

    # Tạo các giá trị mới của Z với khoảng cách 0.01
    new_Z = np.arange(df[cotH].min(), df[cotH].max() + 0.01, 0.01)

    # Tính toán giá trị W tương ứng với các giá trị Z mới
    new_W = spline(new_Z)

    # In ra kết quả
    result_df = pd.DataFrame({'Z': new_Z, 'W': new_W})
    result_df = result_df.applymap("{0:.2f}".format)
    # result_df.to_csv('songtranh222.csv')
    # print(result_df[result_df['Z']==mucnuoc]['W'])
    return result_df[result_df['Z']==str(mucnuoc)]['W'].values[0]
    
a = noisuy_hw(170.96,'Z','W')
print(a)
