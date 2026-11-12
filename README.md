# 穿搭偏好 · 韩系男生

网站：https://minghe4419.github.io/outfit-swipe/

仓库：https://github.com/Minghe4419/outfit-swipe

手机优先的个人穿搭发现 demo。原生 HTML/CSS/JavaScript，无第三方前端依赖和在线 AI 调用。

- 左滑不喜欢、右滑喜欢、想穿按钮、撤销；支持方向键与按钮。
- 整套造型的六个标签维度（含厚度）；AND/OR 组合筛选。
- 收藏、想穿清单、标签纠错、默认/偏好顺序、JSON 导出与恢复。
- 安装说明：https://minghe4419.github.io/outfit-swipe/install.html 。联网使用，无离线缓存。
- 反馈保存在当前浏览器的 localStorage，不跨设备自动同步。
- 固定200张人工标注样本；未启动定时采集。

## 本地使用

在此目录执行 `python3 -m http.server 8878 --directory app`，浏览器打开 `http://127.0.0.1:8878`。

## 发布

运行 `python3 collector/build_pages.py` 将 `app/` 复制到 `docs/`；GitHub Pages 发布 main 分支的 `/docs`。开发请修改 `app/` 后重新生成。不要上传 outputs/、本机测试截图、聊天或任何账户信息。外部穿搭摄影版权属于原作者，不适用代码开源许可。Demo 通过原站图片地址展示，保留出处；不提供图片再分发许可，来源失效时展示重试和出处。

## 采集

Python 3.10+，安装 `scrapling>=0.5`。`collector/collect.py` 获取公开分类候选，遵循 robots；`collector/static_candidates.py` 获取公开详情中的静态图片。`outputs` 存原始候选和本地人工预览。

候选不自动进入已发布清单。人工检查全身画面、重复、标签和出处后写入 app/looks.json。不要将局部特写当成整套穿搭。

GitHub Pages 不能运行 Python。日后可由电脑定时任务或 Actions 定时调用采集程序；当前 demo 不创建后台或定时任务。采集失败不影响固定清单。

## 网络和数据边界

无账号、云数据库或在线 AI 费用；GitHub Pages 承载静态页面。图片来自韩国源站，访问受当地网络影响，不能保证中国大陆所有运营商可用。尚未完成真实手机和多运营商测试。换浏览器、清理网站数据可能丢失记录，请导出备份。导入前有覆盖确认。

本次试用样本、厚度分布及验收边界见 docs/200套试用说明.md；完整标签规则见 docs/标签与筛选体系.md。
