PER_PAGE = 15
INDEX = "/dev/lamp"
# multiple 0多场景模式，single 1单场景模式
PATTERN = 0
# 是否允许修改
CHANGE = False
ASIDE = [
    {
        "title": "设备管理",
        "pre": "首页",
        "url": "/dev",
        "item": [
            {
                "title": "光电配置",
                "url": "/dev/lamp"
            },
            {
                "title": "主机配置",
                "url": "/dev/host"
            },
            {
                "title": "红外配置",
                "url": "/dev/infrared"
            },
            {
                "title": "串口配置",
                "url": "/dev/serial_port"
            },
            {
                "title": "设备部署",
                "url": "/dev/groups"
            },
            {
                "title": "同步",
                # "url": "/api/update",
                "url": "#"
            }
        ]
    },
    {
        "title": "内容管理",
        "url": "/content",
        "item": []
    },
    {"title": "权限管理", "url": "/rights"},
    {
        "title": "系统设置", "url": "/set",
        "item": [
            {
                "title": "展区管理",
                "url": "/set/exhibit"
            },
            {
                "title": "主题管理",
                "url": "/set/theme"
            },
            {
                "title": "标签管理",
                "url": "/set/label"
            }
        ]
    },
    {
        "title": "素材管理", "url": "/material",
        "item": [
            # {
            #     "title": "视频",
            #     "url": "/material/video"
            # },
            # {
            #     "title": "图片",
            #     "url": "/material/image"
            # },
            {
                "title": "PDF",
                "url": "/material/pdf"
            },
            {
                "title": "PPT",
                "url": "/material/ppt"
            }
            # ,{
            #     "title": "音频",
            #     "url": "/material/voice"
            # }
        ]
    }
    # {
    #     "title": "同步",
    #     "url": "/api/update",
    #     "item": []
    # },

    #     {
    #         "title": "内容管理",
    #         "pre": "表格",
    #         "url": "#",
    #         "item": [
    #             {
    #                 "title": "dataTable",
    #                 "url": "/table/data"
    #             },
    #             {
    #                 "title": "jsTable",
    #                 "url": "/table/js"
    #             }
    #         ]
    #     },
    #     {
    #         "title": "样式管理",
    #         "pre": "表单",
    #         "url": "#",
    #         "item": [
    #             {
    #                 "title": "input",
    #                 "url": "/form/input?name=wf"
    #             },
    #             {
    #                 "title": "other",
    #                 "url": "/form/other"
    #             }
    #         ]
    #     }
]
