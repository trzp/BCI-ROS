![bciros](bciros_logo.png)
Copyright (C) 2018, Nudt, JingshengTang, All Rights Reserved

Author: Jingsheng Tang

Email: mrtang@nudt.edu.cn

# Home, GuiEngine, Phase

##GuiEngine是什么
一个简洁的图形刺激引擎

##GuiEngine的特性
- 为了确保图形刺激的精确性，我们使用了opengl硬件加速技术，并且运用了垂直同步(Vertical Hold)方法，使每一帧图形都能被精确渲染</li>
- EEG刺激实验的信号标签由GuiEngine来发射，确保标签记录的时刻是被请求的图形刺激真正被渲染时。</li>
- 跨平台，目前已在windows和linux系统经过测试</li>

## GuiEngine的下载与安装
- 请确保您的电脑安装有[python](https://www.python.org/)和[pygame](https://www.pygame.org/)
- [下载](https://github.com/trzp/guiengine)所有文件，修改setup.py中python_path，比如'c:\Python27'，并运行setup.py即完成安装
 
    ```
    if __name__ == '__main__':
          install_package(python_path,'guiengine_trzp')
    
    ```

## GuiEngine编程</h2>