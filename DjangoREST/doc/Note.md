# Day14






### APIView

- 子类
  - generics包中
  - GenericAPIView
    - 增加的模型的获取操作
    - get_queryset
    - get_object
      - lookup_field 默认pk
    - get_serializer
    - get_serializer_class
    - get_serializer_context
    - filter_queryset
    - paginator
    - paginate_queryset
    - get_paginated_response
  - CreateAPIView
    - 创建的类视图
    - 继承自GenericAPIView
    - 继承自CreateModelMixin
    - 实现了post进行创建
  - ListAPIView
    - 列表的类视图
    - 继承自GenericAPIView
    - 继承自ListModelMixin
    - 实现了get
  - RetrieveAPIView
    - 查询单个数据的类视图
    - 继承自GenericAPIView
    - 继承自RetrieveModelMixin
    - 实现了get  
  - DestroyAPIView
    - 销毁数据的类视图，删除数据的类视图
    - 继承自GenericAPIView
    - 继承自DestroyModelMixin
    - 实现了delete
  - UpdateAPIView
    - 更新数据的类视图
    - 继承自GenericAPIView
    - 继承自UpdateModelMixin
    - 实现了 put,patch
  - ListCreateAPIView
    - 获取列表数据，创建数据的类视图
    - 继承自GenericAPIView
    - 继承自ListModelMixin
    - 继承自CreateModelMixin
    - 实现了  get,post
  - RetrieveUpdateAPIView
    - 获取单个数据，更新单个数据的类视图
    - 继承自GenericAPIView
    - 继承自RetrieveModelMixin
    - 继承自UpdateModelMixin
    - 实现了 get, put, patch
  - RetrieveDestroyAPIView
    - 获取单个数据，删除单个数据
    - 继承自GenericAPIView
    - 继承自RetrieveModelMixin
    - 继承自DestroyModelMixin
    - 实现了  get, delete
  - RetrieveUpdateDestroyAPIView
    - 获取单个数据，更新单个数据，删除单个数据的类视图
    - 继承自GenericAPIView
    - 继承自RetrieveModelMixin
    - 继承自UpdateModelMixin
    - 继承自DestroyModelMixin
    - 实现了 get, put, patch, delete
- mixins
  - CreateModelMixin
    - create
    - perform_create
    - get_success_headers
  - ListModelMixin
    - list
      - 查询结果集，添加分页，帮你序列化
  - RetrieveModelMixin
    - retrieve
      - 获取单个对象并进行序列化
  - DestroyModelMixin
    - destroy
      - 获取单个对象
      - 调用执行删除
      - 返回Respon  状态码204
    - perform_destroy
      - 默认是模型的delete
      - 如果说数据的逻辑删除
        - 重写进行保存
  - UpdateModelMixin
    - update
      - 获取对象，合法验证
      - 执行更新
    - perform_update
    - partial_update
      - 差量更新，对应的就是patch
- viewsets
  - ViewSetMixin
    - 重写as_view
  - GenericViewSet
    - 继承自GenericAPIView
    - 继承自ViewSetMixin
  - ViewSet
    - 继承自APIView
    - 继承自ViewSetMixin
    - 默认啥都不支持，需要自己手动实现
  - ReadOnlyModelViewSet
    - 只读的模型的视图集合
    - 继承自RetrieveModelMixin
    - 继承自ListModelMixin
    - 继承自GenericViewSet
  - ModelViewSet
    - 直接封装对象的所有操作
    - 继承自GenericViewSet
    - 继承自CreateModelMixin
    - 继承自RetrieveModelMixin
    - 继承自UpdateModelMixin
    - 继承自DestroyModelMixin
    - 继承自ListModelMixin



### 用户模块

- 用户注册
  - RESTful
  - 数据开始
    - 模型，数据库
    - 创建用户
      - 用户身份
        - 管理员
        - 普通
        - 删除用户
  - 注册实现
    - 添加了超级管理员生成
- 用户登陆
  - 验证用户名密码
  - 生成用户令牌
  - 出现和注册公用post冲突
    - 添加action
    - path/?action=login
    - path/?action=register
  - 异常捕获尽量精确
- 用户认证
  - BaseAuthentication
    - authenticate
      - 认证成功会返回 一个元组
        - 第一个元素是user
        - 第二元素是令牌  token，auth
- 用户权限
  - BasePermission
    - has_permission
      - 是否具有权限
      - true拥有权限
      - false未拥有权限
- 用户认证和权限
  - 直接配置在视图函数上就ok了



### Leetcode

- 心情好就去刷几道题
- 心情不好就多刷几道

