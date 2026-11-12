# 穿搭偏好：项目工作约定

- 本项目独立于早晚小冒险；不要修改晚睡消灭器、旧Sites或旧Pages。
- 开发源码在 app/；执行 python3 collector/build_pages.py 生成 docs/ 的发布文件。发布 GitHub Pages：Minghe4419/outfit-swipe，main，/docs。
- 当前图库按用户要求替换为50张经GPT视觉审核的整套造型；保留真实原帖出处与人工标签；旧图库选择须继续可导出备份，不计入新图库进度；外部摄影版权属于原作者，不能把源图当成开源资产。outputs/ 的原始候选、下载预览、测试截图与备份样本不上传。
- 个人选择只保存在当前浏览器 localStorage（outfit-preference-v1），不采集个人数据到服务器。增加云同步、账号或在线AI须先说明影响。
- 数据准备使用 Scrapling；先检查robots；不抓搜索限制、登录或付款路径。固定清单经人工整套造型审核后再更新，不自动覆盖人工标签。
- 发布前运行 node tests/engine.mjs；界面变更需验证手机宽度、真实左右滑、手机撤销、刷新恢复和备份。原始网络和真机可用性不可因模拟浏览器通过而宣称完成。
- 每轮更新 docs/接续记录.md；更新 app 后重新生成 docs，保持两处一致。
