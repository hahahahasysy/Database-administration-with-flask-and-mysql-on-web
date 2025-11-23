# Database-administration-with-flask-and-mysql-on-web
背景是参加hhu的校庆网页设计大赛，今天拿了一等奖，分享一下我作为后端进行的数据库管理和交互的内容。会有所有的源码和使用说明。

本项目以“百十故事”为名，通过展示学校与大家的“故事”唤起大家对于河海百十载间的记忆。网站内容分为历史、学院、青春三类，用户可以在此查阅建校以来发生的故事、目前学校设立的各类特色学院，也可以查看他人上传的青春故事，或是上传自己的故事。因此，网页作品在以校庆为主题的同时，需要在合适位置展示这三个板块，且作为动态组作品，需要体现前后端交互，即有获取和存储的效果。

·代码编辑器：Visual Studio Code
·前端框架：Vite+Vue3
·前端工具库：Pinia(状态管理)、Boxicon（图标引用）、TailwindCSS（CSS样式）以及基于该CSS的UI组件库Nuxt UI、Element Plus组件库、Macy.js（瀑布流工具）
·后端框架：Flask
·数据库：MySQL
·数据库 ORM：Flask - SQLAlchemy
·数据库迁移：Flask - Migrate
·跨域处理：Flask - CORS

数据库各张表相关定义详见models.py
