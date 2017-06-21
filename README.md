# turtle_war
OneNightROBOCON競技「turtle war」プロジェクト

ロボットで戦車対戦をするようなゲームです。

現状は、自律移動を練習する簡易版として、単体でキャンディをさがして集めるゲームになっています。

TODO [ここにサンプルを動かしたときの動画を貼る]

## Quick Start
最後までできてロボットを動かせれば当日までの準備はOKです。

以下は、ubuntu14.04環境で動かしてください。
Windows、MACの場合はvirtualbox等の仮想環境でubuntu環境を作ってください。

### install ros indigo
rosのインストールが終わっている人は飛ばしてください。

参考  公式サイト<http://wiki.ros.org/ja/indigo/Installation/Ubuntu>
```
$ sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu trusty main" > /etc/apt/sources.list.d/ros-latest.list'
$ wget http://packages.ros.org/ros.key -O - | sudo apt-key add -
$ sudo apt-get update
$ sudo apt-get install ros-indigo-desktop-full
```
環境設定(終わっている人は飛ばしてください)
```
$ sudo rosdep init
$ rosdep update
$ echo "source /opt/ros/indigo/setup.bash" >> ~/.bashrc
$ source ~/.bashrc
```
ワークスペース作成(終わっている人は飛ばしてください)

参考<http://wiki.ros.org/ja/catkin/Tutorials/create_a_workspace>
```
$ mkdir -p ~/catkin_ws/src
$ cd ~/catkin_ws/src
$ catkin_init_workspace
$ cd ~/catkin_ws/
$ catkin_make
$ echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
$ source ~/.bashrc
```


### install turtlebot package
タートルボット関連のパッケージのインストール

```
$ sudo apt-get update
$ sudo apt-get upgrade
$ apt-get install ros-indigo-turtlebot ros-indigo-turtlebot-apps ros-indigo-turtlebot-interactions ros-indigo-turtlebot-simulator ros-indigo-kobuki-ftdi ros-indigo-rocon-remocon ros-indigo-rocon-qt-library ros-indigo-ar-track-alvar-msgs
```

### clone this repo
このリポジトリをクローン

```
$ cd ~/catkin_ws/src
$ git clone https://github.com/dashimaki360/turtle_war.git
```

### make
```
$ cd ~/catkin_ws/src
$ catkin_make
```

### launch sample(please open 2 terminals)
サンプルの実行

ロボットが出てきてランダムな動きができれば成功
初回起動時は3DモデルのダウンロードがあるためGAZEBOがしばらく固まることがあります。

terminal one
```
$ roslaunch turtle_war make_field.launch
```

terminal two
```
$ roslaunch turtle_war spawn_robot.launch
```

## 動作環境
- OS  : Ubuntu 14.04
- ROS : indigo
- GAZEBO : 2.
- Python : 2.7


