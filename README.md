#### 一、项目配置：

1. 项目依赖：项目文件夹中有requirements.txt，此即为项目运行所需配置环境。
    使用pip installl -r requirements.txt进行安装。
    
2. 配置数据库，数据库使用mysql数据库，在本地新建数据库，然后在settings中进行库名、用户名、密码配置

3. 执行项目迁移
    python manage.py makemigrations
    python manage.py migrate

4. 导入数据文件
    mysql -uroot -p
    use 数据库;
    source  bus.sql

5. 运行项目：
    python3 manage.py runserver

#### 二、主要包含前台和后台：

1. 前台用户
    登录、注册、修改个人信息、修改密码、浏览信息、批量导入数据
    
2. 后台用户
    登录、添加普通用户、修改个人信息、分配后台权限、批量导入数据、插入站点、插入类型


**admin管理平台账号：**
账号：admin
密码：admin123456

**普通用户：**
账号：ybkb
密码：ybkb123

**v1.0 用户模块**

1. 用户数据表搭建
2. 修改个人信息
3. 修改密码
4. 重置密码（邮箱校验）

**v2.0 图片-站点模块** 
1. 展示图片
2. hdfs存储文件信息
3. 多线程解析xml
4. 批量导入和导出


**v3.0 三维展示数据---待定**
1. 首页展示
2. 图片时间轴展示

**v4.0 admin管理平台**

1. 主要使用数据插入模块插入图片和站点信息
2. 附带权限管理可以对管理员进行权限控制

#### **Be careful**：

系统名称暂定为：遥感数据服务平台，修改时对每页的title进行修改
数据库中站点信息较少，可以补充站点信息。

#### **2. 统计信息展示：**数据总数、今日上传、站点总数等

>![image-20220417120955660](C:\Users\11237\AppData\Roaming\Typora\typora-user-images\image-20220417120955660.png)

#### **3. 数据列表展示**：分页展示所有数据、可进行条件搜索

>图片可缩放移动
>
>条件搜索（地点、图像类型、来源等）
>
>![image-20220417120030618](C:\Users\11237\AppData\Roaming\Typora\typora-user-images\image-20220417120030618.png)

#### **4. 时间地图展示：**以时间轴为顺序的图片展示

>1. 可通过鼠标操作进行地图的缩放
>
>2. 点击锚点图标后会弹出一个图片信息列表，以时间轴为顺序展示该地点历年的所有图片（图片来自各个渠道）
>3. 点击图片可以查看真实尺寸的图片：该图片可以通过滑动滚轮缩放、移动鼠标平移
>
>![image-20220417121525262](C:\Users\11237\AppData\Roaming\Typora\typora-user-images\image-20220417121525262.png)

#### **5. 联合搜索**：查询所选时间段内站点的图片信息

> <img src="C:\Users\11237\AppData\Roaming\Typora\typora-user-images\image-20220417122104342.png" alt="image-20220417122104342" style="zoom:80%;" />
>
> <img src="C:\Users\11237\AppData\Roaming\Typora\typora-user-images\image-20220417122131348.png" alt="image-20220417122131348" style="zoom:67%;" />

#### **6. 批量导入：**多文件批量上传数据库

>批量上传的文件在后台会进行自动分类，自动建立地理信息系统里的锚点，自动建立各类数据库表，并且将XML文件中的图片描述信息自动入库。
>
>HDFS上传文件代码：
>
>https://www.codeleading.com/article/56502660339/
>
>https://www.programminghunter.com/article/57011388538/
>
>![image-20220417123100767](C:\Users\11237\AppData\Roaming\Typora\typora-user-images\image-20220417123100767.png)
>
>![image-20220417123609762](C:\Users\11237\AppData\Roaming\Typora\typora-user-images\image-20220417123609762.png)

#### 7. 批量导出：数据库里的所有数据进行打包下载

>![image-20220417123440063](C:\Users\11237\AppData\Roaming\Typora\typora-user-images\image-20220417123440063.png)

# 二、数据库设计

- 图像
  ID号、名称、图像路径、图像json、图像类型ID、站点ID、图像来源、长宽高、描述、添加时间、修改时间
- 站点
  ID号、名称、添加时间、修改时间
- 图像类型
  ID号、名称、添加时间、修改时间
- 用户
  ID号、用户名、密码、添加时间、修改时间

## **图像表 image**

| 序号 | 列名       | 字段名      | 属性          | 非空     | 默认 | 说明               |
| ---- | ---------- | ----------- | ------------- | -------- | ---- | ------------------ |
| 1    | 图像id     | id          | int(11)       | not null |      | 主键、自增、无符号 |
| 2    | 图像名称   | name        | varchar(1024) |          |      | 唯一性约束         |
| 3    | 图像路径   | img_path     | varchar(100)  |          |      |                    |
| 4    | 图像json    | img_json     | varchar(100)  |          |      |                    |
| 5    | 图像类型id | pictype_id  | int(11)       |          |      |                    |
| 6    | 站点id     | station_id  | int(11)       |          |      |                    |
| 7    | 图像来源   | pic_source  | varchar(1024) |          |      |                    |
| 8    | 长         | length      | int(11)       |          |      |                    |
| 9    | 宽         | width       | int(11)       |          |      |                    |
| 10   | 高         | height      | int(11)       |          |      |                    |
| 11   | 状态       | status      | tinyint(1)    | not null | 1    | 1：正常；9：删除   |
| 12   | 描述信息   | description | varchar(1024) |          |      |                    |
| 13   | 添加时间   | create_at   | datetime      |          |      |                    |
| 14   | 修改时间   | update_at   | datetime      |          |      |                    |

## **站点表 image_station**

| 序号 | 列名     | 字段名      | 属性          | 非空     | 默认 | 说明               |
| ---- | -------- | ----------- | ------------- | -------- | ---- | ------------------ |
| 1    | 站点id   | id          | int(11)       | not null |      | 主键、自增、无符号 |
| 2    | 站点名称 | name        | varchar(200)  |          |      | 唯一性约束         |
| 3    | 状态     | status      | tinyint(1)    | not null | 1    | 1：正常；9：删除   |
| 4    | 描述信息 | description | varchar(1024) |          |      |                    |
| 5    | 添加时间 | create_at   | datetime      |          |      |                    |
| 6    | 修改时间 | update_at   | datetime      |          |      |                    |

## **图像类型表 image_type**

| 序号 | 列名     | 字段名      | 属性          | 非空     | 默认 | 说明               |
| ---- | -------- | ----------- | ------------- | -------- | ---- | ------------------ |
| 1    | 类型id   | id          | int(11)       | not null |      | 主键、自增、无符号 |
| 2    | 类型名称 | name        | varchar(1024) |          |      | 唯一性约束         |
| 3    | 状态     | status      | tinyint(1)    | not null | 1    | 1：正常；9：删除   |
| 4    | 描述信息 | description | varchar(1024) |          |      |                    |
| 5    | 添加时间 | create_at   | datetime      |          |      |                    |
| 6    | 修改时间 | update_at   | datetime      |          |      |                    |

## **用户表 users**

| 序号 | 列名             | 字段名        | 属性         | 非空     | 默认 | 说明                          |
| ---- | ---------------- | ------------- | ------------ | -------- | ---- | ----------------------------- |
| 1    | 用户id           | id            | int(11)      | not null |      | 主键、自增、无符号            |
| 2    | 用户名           | username      | varchar(150) |          |      |                               |
| 3    | 密码             | password_hash | varchar(100) |          |      |                               |
| 4    | 密码干扰值       | password_salt | varchar(50)  |          |      |                               |
| 5    | 手机号           | phone         | int(11)      |          |      | 唯一性约束                    |
| 6    | 状态             | status        | tinyint(1)   | not null | 1    | 1:普通/2:管理员/3:禁用/9:删除 |
| 7    | 最后一次登录时间 | last_login    | datetime     |          |      |                               |
| 8    | 添加时间         | create_at     | datetime     |          |      |                               |
| 9    | 修改时间         | update_at     | datetime     |          |      |                               |



FINISH！