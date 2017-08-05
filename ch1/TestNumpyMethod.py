from numpy import *

dataset = array([[0, 1, 0, 1], [1, 0., 1, 0], [1, 0, 1, 1], [0, 1, 1, 0]])

data_multi_dim = array([[[1, 2], [2, 3], [1, 7]], [[1, 5], [1, 6], [3, 1]]])

def test_shape():
    """shape属性得到了array的大小, 例如上述array是一个4*4的二维矩阵, 因此得到(4, 4)"""
    print(dataset.shape)
    print(dataset.shape[0])
    print(data_multi_dim.shape)  # (2, 3, 2) result 是一个tuple(元组,即不能改变的数组) 描述了每一位的长度.从最外面到最里面.


def test_tile():
    """tile(A, rep) 函数是用一个array(A)构建一个重复rep次的array, 看函数的定义即可
    """
    dataset_size = dataset.shape[0]
    in_x = [[1, 2], [1, 3]]
    a = tile(in_x, (dataset_size))
    print(a)


def test_zeros():
    """返回一个全是0的array, 维度由参数决定"""
    a = zeros((2, 2, 2))
    print(a)


def test_all():
    # test_shape()
    # test_tile()
    test_zeros()
