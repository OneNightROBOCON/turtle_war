# turtle_war
OneNightROBOCON競技「turtle war」プロジェクト

ロボットで戦車対戦をするようなゲームです。

現状は、自律移動を練習する簡易版として、単体でキャンディをさがして集めるゲームになっています。


![demo](turtle_war.gif)


## 目次
- インストール
- ルール
- ファイル構成
- その他
- 動作環境


## インストール
最後までできてロボットを動かせれば当日までの準備はOKです。

以下は、ubuntu14.04環境で動かしてください。
Windows、MACの場合はvirtualbox等の仮想環境でubuntu環境を作ってください。

### 1. ros (indigo) のインストール
rosのインストールが終わっている人は`2. タートルボットパッケージのインストール`まで飛ばしてください。

参考  ROS公式サイト<http://wiki.ros.org/ja/indigo/Installation/Ubuntu>
上記サイトと同じ手順です。
ros インストール
```
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu trusty main" > /etc/apt/sources.list.d/ros-latest.list'
wget http://packages.ros.org/ros.key -O - | sudo apt-key add -
sudo apt-get update
sudo apt-get install ros-indigo-desktop-full
```
環境設定
```
sudo rosdep init
rosdep update
echo "source /opt/ros/indigo/setup.bash" >> ~/.bashrc
source ~/.bashrc
```
ワークスペース作成

参考<http://wiki.ros.org/ja/catkin/Tutorials/create_a_workspace>
```
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
catkin_init_workspace
cd ~/catkin_ws/
catkin_make
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc
```


### 2. タートルボットパッケージのインストール
タートルボット関連のパッケージのインストール

以下`6.サンプルの実行`までは一括スクリプトがあります。`setting_for_robocon.sh`　もろもろインストールしてサンプルの実行まで動きます。

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install ros-indigo-turtlebot ros-indigo-turtlebot-apps ros-indigo-turtlebot-interactions ros-indigo-turtlebot-simulator ros-indigo-kobuki-ftdi ros-indigo-rocon-remocon ros-indigo-rocon-qt-library ros-indigo-ar-track-alvar-msgs
```

### 3. OpenCVのインストール
openCVに必要なnumpyのインストール
```
sudo apt-get install python-numpy
```
openCVのインストール
```
sudo apt-get install python-opencv
```
### 4. このリポジトリをクローン
turtlr_war リポジトリをクローンします。
先程作ったワークスペースの`src/`の下においてください。
```
cd ~/catkin_ws/src
git clone https://github.com/OneNightROBOCON/turtle_war
```

### 5. make

```
cd ~/catkin_ws
catkin_make
```

### 6. サンプルの実行
サンプルの実行します。うまく行けばインストール終了です。

```
roscd turtle_war
bash start.sh
```

ターミナルが2つ立ち上がり、
GAZEBOが起動して、ロボットが出てきてランダムな動きができれば成功です。
初回起動時は3DモデルのダウンロードがあるためGAZEBOがしばらく固まることがあります。

2分間立つとキャンディが消えなくなり、ターミナルにタイムアップ表示と、スコアとキャンディの取得個数が表示されます。

## ルール
※ルールは基本的な部分は決定しましたが、キャンディの個数や、大きさ、障害物の配置など当日までに微調整をする場合があります。
変更があった場合はなるべく早くお知らせいたします。

### 基本ルール

ロボットを自律移動させ制限時間内にたくさんのキャンディを集めるゲームです。

キャンデイにロボットが近づくとキャンディをとることが出来ます。特別な操作は必要ありません。

キャンディをとると加算されるポイントを競います。

制限時間は2分間です。

競技は全てロボットシュミレータgazebo上で行います。

### ポイントの加算方法

勝ち負けを決めるポイントは、キャンディをとると増えます。減ることはありません。

通常のキャンディは赤色で、とると1ポイント加算されます。スペシャルキャンディは黄色で、とると5ポイント加算されます。

制限時間の2分をすぎるとポイントは加算されません。

### キャンディの出現ルール

キャンディは常に全部で20個あります。キャンディをとるとキャンディは消えて、すぐに別の場所に出現します。

キャンディの出現場所はランダムに決定します。しかし、キャンディはロボットを中心として半径1.5mには出現しないようになっています。

キャンディには通常の赤いキャンディと、黄色いスペシャルキャンディがあります。黄色いスペシャルキャンディは少し小さめです。

スペシャルキャンディの出現条件について。
開始から15秒経過後に出現する1つ目のキャンディがスペシャルキャンディになります。
その後、スペシャルキャンディが出現してから15秒経過後に出現する1つ目のキャンディがスペシャルキャンディになります。
15秒経過しても、他のキャンディをとってキャンディを出現させるまでスペシャルキャンディは出現しません。15秒の計測はスペシャルキャンディが出現してから計測を再開します。


### フィールド
フィールドは6m四方の壁で囲われた空間です。

フィールドには直方体と球の障害物が設置されています。設置初期位置は常に同じです。障害物は固定されておらず、ロボットで押すと動きます。
壁はロボットで押しても動きません。

### ロボット
ロボットはタートルボットを使用します。

最高速度は実機で走行可能な範囲と定めます。(詳細は後日更新します)

使用可能なセンサは
- バンパーセンサ
- kinect(rgb画像、depth画像)
- オドメトリ

とします。

## 当日の運営に関して
当日は競技時間は設けず、作業中随時運営の用意した競技用PCで作ったプログラムを実行することが出来ます。

つまり時間内ならば、なんどでも挑戦が可能で、最高スコアが最終的な記録になります。

競技PCの様子はスクリーンで参加者が観戦できます。

運営の簡略化と、参加者間でソースコードを共有し参考にし合うために、
当日は、このリポジトリをforkしたリポジトリをそれぞれ作成いただき、そこで作業していただく予定です。
ソースコード提出はgithubのforkしたリポジトリを介して行います。
参加者はお互いのコードを見ることができます。
いい動きをしている参加者のコードをその場でみて、参考にすることで全体のレベルアップをはかる狙いです。
gitに慣れていない方むけに、操作法など具体的な説明は後日更新します。

## ファイル構成
各ディレクトリの役割と、特に参加者に重要なファイルについての説明

下記のようなフォルダ構成になっています。  
**`!!!`は変更禁止ファイル、ディレクトリであることを表しています。**
`yourBot.launch`が競技開始スクリプト`start.sh`の最後で実行されるので、そこで自分の作ったノードを立ち上げるように設定してください。
現在はランダム走行する`randomBot.py`が実行されるように設定されています。

```
turtle_war/
|-launch/        : launchファイルの置き場
| |-yourBot.launch  参加者の作成したロボット制御ノードのlaunchファイル
| |-make_field.launch : !!! フィールドの立ち上げ、キャンディ、スコアの管理
| |-spawn_robot.launch : !!! ロボットの立ち上げ、`yourBot.lanch`の実行
|
|- src/          : cppファイルの置き場
|
|- scripts/      : pythonファイルの置き場
| |-abstractBot.py : 走行制御ノードの抽象クラス。
| |-randomBot.py   : ランダム走行するサンプルプログラム
| |-controlCandy.py : !!! candy の管理ノード
|
|- world/        : !!! gazeboの環境ファイルの置き場
|
|- models/       : !!! gazeboの3Dモデルファイルの置き場
|
|-start.sh      : !!! 競技開始スクリプト
|-setting_for_robocon.sh : 環境構築用スクリプト
|-README.md : これ
```
↑ディレクトリと特に重要なファイルのみ説明しています。

## 動作環境
- OS  : Ubuntu 14.04
- ROS : indigo
- GAZEBO : 2
- Python : 2.7
