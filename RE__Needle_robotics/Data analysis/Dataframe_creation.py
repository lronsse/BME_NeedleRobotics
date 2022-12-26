import pandas as pd

# initialize list of lists
data = [['p1t1', 0, 0, 0], ['p1t2', 0, 0, 0], ['p1t3', 0, 0, 0], ['p1t4', 0, 0, 0], ['p1t5', 0, 0, 0],
        ['p2t1', 0, 0, 0], ['p2t2', 0, 0, 0], ['p2t3', 0, 0, 0], ['p2t4', 0, 0, 0], ['p2t5', 0, 0, 0],
        ['p3t1', 0, 0, 0], ['p3t2', 0, 0, 0], ['p3t3', 0, 0, 0], ['p3t4', 0, 0, 0], ['p3t5', 0, 0, 0],
        ['p4t1', 0, 0, 0], ['p4t2', 0, 0, 0], ['p4t3', 0, 0, 0], ['p4t4', 0, 0, 0], ['p4t5', 0, 0, 0],
        ['p5t1', 0, 0, 0], ['p5t2', 0, 0, 0], ['p5t3', 0, 0, 0], ['p5t4', 0, 0, 0], ['p5t5', 0, 0, 0],
        ['p6t1', 0, 0, 0], ['p6t2', 0, 0, 0], ['p6t3', 0, 0, 0], ['p6t4', 0, 0, 0], ['p6t5', 0, 0, 0]]

# Create the pandas DataFrame
df = pd.DataFrame(data, columns=['Name', 'Insertion', 'Zero', 'Retraction'])

# print dataframe.
df.to_csv('curve_data.csv')