import pandas as pd

carac = pd.read_csv('Caracteristicas y composicion del hogar.CSV', sep = ";")
carac.info()

carac = carac[['DIRECTORIO', 'ORDEN', 'P6020', 'P6040', 'P5502']]
print(carac)

tec = pd.read_csv('Tecnologias de información y comunicación.CSV', sep = ";")
tec.info()

tec = tec[['DIRECTORIO', 'ORDEN','P1910', 'P1911', 'P1912', 'P1084', 'P1710S12', 'P1083S3', 'P1083S9', 'P805S2']]
tec.info()
print(tec)

condi = pd.read_csv('DBF_ENCV_591_3.CSV', sep = ";")
condi.info()

condi = condi[['DIRECTORIO', 'ORDEN','P9010', 'P9025S1', 'P9025S2']]
condi.info()
print(condi)


data = carac.merge(tec, how = 'outer', on = ['DIRECTORIO', 'ORDEN']).merge(condi, how = 'outer', on = ['DIRECTORIO', 'ORDEN'])
print(data)
data.info()
data['DIRECTORIO'].dtypes


for col in ['DIRECTORIO', 'ORDEN', 'P6020', 'P6040', 'P5502', 'P1910', 
            'P1911', 'P1912', 'P1084', 'P1710S12', 'P1083S3', 'P1083S9', 'P805S2', 'P9010', 'P9025S1', 'P9025S2']:
    if data[col].dtypes == 'int64':
        data[col] = data[col].astype('int16')
    else:
        data[col] = data[col].astype('float16')




data.to_excel('base.xlsx')
data.to_stata('base.dta')
data.to_csv('base.csv')

#####Ultimando detalles en los datos####
data = pd.read_csv('base.csv')
data.info()
print(data)

for col in data:
    print('-----------------------')
    print(col)
    data[col].value_counts()

data1 = data.copy()
for col in ['P1710S12', 'P9010', 'P9025S1', 'P9025S2']:
    data[col] = data[col].replace(2, 0)

data['FDI'] = '1'

for index, row in data.iterrows():
    x = row['P1910'] + row['P1911'] + row['P1912']
    if x >= 9:
        data.at[index, 'FDI'] = data.at[index, 'FDI'].replace('1', '0')

data['FDI'].value_counts()

data['FI'] = '1'
for index, row in data.iterrows():
    if row['P1084'] >= 3:
        data.at[index, 'FI'] = data.at[index, 'FI'].replace('1', '0')

data['FI'].value_counts()


data = data.rename({'P6020' : 'sex', 'P6040' : 'edad', 
                    'P1710S12':'nf', 'P1083S3' : 'ir', 'P1083S9' : 'im',
                    'P805S2':'rn', 'P9010':'pi', 'P9025S1':'vic', 'P9025S2':'vico'}, axis = 1)
data = data.drop(['Unnamed: 0', 'P5502', 'P1910', 'P1911', 'P1912', 'P1084'], axis = 1)

for col in ['FI', 'FDI']:
    data[col] = data[col].astype(int)
data.info()

data.to_csv('base.csv')
data.to_excel('base.xlsx')
data.to_stata('base.dta')