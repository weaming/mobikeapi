## Mobike API

采用Mongo作为存储，遍历区域经纬度。

深圳区域大概有9W多单车(2017/04/22)。

前端配合高德地图作展示，标记出每辆单车的话，由于数据量太多，采用分区域展示，拖动地图自动更新。

## Screenshots

对`distId`进行去重后再进行展示。可以发现共享车在不同城市环境中的分布情况。

![](screenshots/1.png)

![](screenshots/2.png)

![](screenshots/3.png)

加上颜色区分后：红色普通车，蓝色Lite，黄色红包车(型号99)？

![](screenshots/4.png)
