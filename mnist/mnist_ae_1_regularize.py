# stacked auto encoder
# 分析0，一般而言自编码器学到的是PCA的一个近似
# 但是如果对因隐层施加稀疏性约束的话，会得到更为紧凑的表达，只有一小部分神经元将被激活。
# 然而始终无法训练到0的水平，甚至不在一个数量级

import keras.backend as K
from keras.datasets import mnist
from keras.layers import Input,Dense
from keras.models import Model
import numpy as np
import matplotlib.pyplot as plt
from keras import regularizers

epochs=7
batch_size=256


# load data
# 数据格式为通道在前
K.set_image_data_format('channels_first')

(x_train,_),(x_test,_)=mnist.load_data()

x_train=x_train.reshape((x_train.shape[0],np.prod(x_train.shape[1:])))
x_test=x_test.reshape((x_test.shape[0],np.prod(x_test.shape[1:])))
x_train=x_train.astype('float32')
x_test=x_test.astype('float32')
x_train/=255
x_test/=255
print('#Get train samples',x_train.shape[0])
print('#Get test samples',x_test.shape[0])

# 隐层神经元个数，即code维度
encoding_dim=32

# ----------输入层
input_img=Input(shape=(784,))
# ----------编码层
# 增加L1正则项
encoded=Dense(encoding_dim,activation='relu',activity_regularizer=regularizers.l1(0.01))(input_img)
# ----------解码层
decoded=Dense(784,activation='sigmoid')(encoded)

# 自编码器模型定义
autoencoder=Model(input_img,decoded)

# 编码器定义
encoder=Model(input_img,encoded)

# 解码器定义
# 编码层的输出是32维
encoded_input=Input(shape=(encoding_dim,))
# 解码层
decoder_layer=autoencoder.layers[-1]
decoder=Model(encoded_input,decoder_layer(encoded_input))

autoencoder.summary()

# 编译
autoencoder.compile(optimizer='adam',loss='binary_crossentropy')

# 训练
autoencoder.fit(x_train,
                x_train,
                epochs=epochs,
                batch_size=batch_size)

# encode and decode some imgs
encoded_imgs=encoder.predict(x_test)
decoded_imgs=decoder.predict(encoded_imgs)

# 可视化
# 可视化几个图
n=10
plt.figure(figsize=(20,4))# figsize指定总的图像大小
for i in range(n):
    # 绘制原图
    # subplot(numRows, numCols, plotNum)
    ax=plt.subplot(2,n,i+1)
    # 原本的一维向量展成28×28图像
    plt.imshow(x_test[i].reshape(28,28))
    plt.gray()
    # 隐藏坐标轴
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # 绘制重建图
    ax=plt.subplot(2,n,i+1+n)
    plt.imshow(decoded_imgs[i].reshape(28,28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

plt.show()

# epoch=7的时候，loss=0.3121





