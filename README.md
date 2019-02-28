# face-recognition-service

#### 介绍
在face_recognition库的基础上构建的人脸识别服务（人脸对比接口...）

#### 安装教程

1. 从此[链接](http://www.lfd.uci.edu/~gohlke/pythonlibs/)下载并安装`scipy`和`numpy+mkl`（必须是mkl版本）软件包（所有信用都归Christoph Gohlke所有）。请记住根据您当前的Python版本获取正确的版本。
2. `Boost`从此[链接](https://sourceforge.net/projects/boost/files/)下载当前MSVC的库源代码或二进制版本。
3. 如果您已经下载了二进制版本的`Boost`，则只需将内容解压缩到C:\local\boost_1_XX_X
4. `dlib`从此[repo](https://github.com/davisking/dlib)中获取最新版本并将其解压缩
5. 转到`dlib`目录并打开cmd并按照以下命令构建dlib:(记得用当前版本替换XX `Boost`）
```
set BOOST_ROOT=C:\local\boost_X_XX_X
set BOOST_LIBRARYDIR=C:\local\boost_X_XX_X\stage\lib
python setup.py install --yes USE_AVX_INSTRUCTIONS
or
python setup.py install --yes USE_AVX_INSTRUCTIONS --yes DLIB_USE_CUDA
```
6. 现在您可以`import dlib`在python脚本中使用没有任何问题
7. 您还可以查看`dlib`的当前版本`pip show dlib`
8. 现在，只需安装`face_recognition`，执行命令 `pip install face_recognition`
9. 请享用！

#### 打包教程

1. xxxx
2. xxxx
3. xxxx

#### 参与贡献

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request