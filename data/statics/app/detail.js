function createDetailApp(contentId) {
    var detail_tab = $("#detail_tab")
    var grids = {}, urls = {}, cols = {}, controllers = {}, tab = detail_tab.find(".nav-link.active").attr("type"),
        options = undefined;
    console.log(">>>当前激活tab为：", tab)
    detail_tab.on("click", "li.nav-item", function (e) {
        tab = $(this).find("a").attr("type")
        //查询
        if (!urls[tab].done) {
            urls[tab].done = true
            $.request({url: urls[tab].list, data: {theme: options, content: contentId}}, function (res) {
                controllers[tab].clients = res.data
                console.log("》》》》????", controllers[tab].clients)
                grids[tab].jsGrid("loadData");
            })
        }
    })

    var themeSelector = $("#themeSelector")
    themeSelector.on("change", function (e) {
        //var options = themeSelector.find("option:selected").val(); //获取选中的项
        options = themeSelector.val()
        console.log("selector>>", options)
        options != null && options != undefined && addForm.find("[name='theme']").val(options)
        //查询
        urls[tab].done = true
        $.request({url: urls[tab].list, data: {theme: options, content: contentId}}, function (res) {
            controllers[tab].clients = res.data
            console.log("》》》》????", controllers[tab].clients)
            grids[tab].jsGrid("loadData");
        })
    })
    $.request({url: "/set/theme/list"}, function (res) {
        console.log(">>", res)
        var data = res.data
        themeSelector.html("")
        for (var i  in data) {
            var item = data[i], val = item.id, name = item.name
            themeSelector.append($.parseHTML("<option value='" + val + "'>" + name + "</option>"))
        }
        themeSelector.trigger("change")
    })


    var addForm = $("#addModal form")
    var addOpt = $("#addOpt")
    var addOptClose = $("#addOptClose")
    addForm.find("[name='content']").val(contentId)

    var updateForm = $("#updateModal form")
    var updateOpt = $("#updateOpt")
    var updateOptClose = $("#updateOptClose")
    var updateModalBtn = $("#updateModalBtn")

    var delForm = $("#delModal form")
    var delOpt = $("#delOpt")
    var delOptClose = $("#delOptClose")
    var delModalBtn = $("#delModalBtn")

    $('.select2').select2()
    jsGrid.locale("zh-cn");

    function createDetailGrid(columns, url, item) {
        cols[item] = columns
        urls[item] = url

        controllers[item] = {
            loadData: function (filterRow) {
                console.log("》》》》loadData", controllers[tab].clients, controllers[tab].clients.length, controllers[tab], filterRow)
                //return controller.clients
                return $.grep(controllers[tab].clients, function (row) {
                    var res = true
                    for (var i in filterRow) {
                        filterVal = filterRow[i], val = row[i]
                        filterVal = typeof filterVal == "string" ? filterVal.trim() : filterVal
                        val = typeof val == "string" ? val.trim() : val
                        if (filterVal !== "" && filterVal !== undefined && filterVal !== null) {
                            res = val.indexOf ? val.indexOf(filterVal) > -1 : val == filterVal
                        }
                    }
                    return res
                });
            },
            clients: []
        }
        cols[item] = cols[item].concat([
            {
                name: "opt", type: "text", title: "操作",
                width: 160,
                align: "center",
                readOnly: false,
                //filtering: false,
                //visible: false,
                disabled: false,
                inserting: false,
                editing: false,
                sorting: false,
                filterTemplate: function () {
                    return $('<div>' +
                        '<a href="#" class="fas fa-search" style="font-size:18px;align-text:center;line-height:32px;" data-type="search"></a>' +
                        '<a href="#" class="fas fa-share mr-1" style="font-size:18px;align-text:center;line-height:32px; margin-left:5px" data-type="back"></a>' +
                        '</div>').on("click", "a", function (e) {
                        e.stopPropagation();
                        var $e = $(this), type = $e.data("type")
                        type == "back" ? grids[tab].jsGrid("clearFilter").done(function () {
                            console.log("清空搜索条件完成");
                        }) : grids[tab].jsGrid("loadData");
                        //console.log("搜索。。。", arguments[0], arguments[1], $(this).data("type"))
                    })
                },
                insertTemplate: function () {
                    return ""
                },
                filterValue: function () {
                    return ""
                },
                itemTemplate: function (value, item) {
                    return $('<div class="btn-group">' +
                        '<button type="button" class="btn btn-default" data-type="update">修改</button>' +
                        '<button type="button" class="btn btn-default" data-type="delete">删除</button>' +
                        '</div>').on("click", "button",
                        function (e) {
                            e.stopPropagation();
                            var $el = $(this), type = $el.data("type")
                            if (type == "update") {
                                updateModalBtn.trigger("click")
                                updateForm.find(".form-group").css("display", "none")
                                for (var i in cols[tab]) {
                                    var name = cols[tab][i].name
                                    var $el = updateForm.find("[name='" + name + "']")
                                    var type = $el.attr("type")
                                    var val = item[name]
                                    var display = "flex"
                                    if (type == "radio") {
                                        //$el.prop("checked",false);
                                        display = "block"
                                        $el.each(function () {
                                            var $radio = $(this)
                                            if ($radio.val() == val) {
                                                console.log(">>>>", $radio.val(), val)
                                                $radio.prop("checked", true);
                                            }
                                        })
                                    } else if (type == "file") {
                                        $el.siblings(".custom-file-label").text(val)
                                    } else {
                                        $el.val(val)
                                    }
                                    $el.parents(".form-group").css("display", display)
                                }
                                //updateForm.find("[name='number']").val(item.number)
                                //updateForm.find("[name='name']").val(item.name)
                            } else if (type == "delete") {
                                delModalBtn.trigger("click")
                                delForm.find("[name='id']").val(item.id)
                                delForm.find("[name='theme']").val(item.theme)
                                delForm.find("[name='content']").val(item.content)
                            }

                            //$.request({url: "/set/exhibit/add", data: {name: "大厅", number: 3}}, function (res) {
                            //controller.clients = res.data
                            //gridList.jsGrid("loadData");
                            //})
                        })
                }

            }
        ])

        // var gridList = $("#contentList")
        grids[item] = $("#" + item + "_grid")
        grids[item].jsGrid({
            height: "690",
            width: "100%",
            pageSize: 11,
            paging: true,
            //pageButtonCount: 5,
            deleteConfirm: "确定要删除吗",
            loadMessage: "正在装载数据，请稍候......",
            sorting: true,
            filtering: true,
            //data: db.clients,
            controller: controllers[item],
            fields: cols[item]
        });

    }

    var $addBtn = $("#addBtn").on("click", function () {
        addForm.find(".form-group").css("display", "none")
        for (var index in  cols[tab]) {
            var file = cols[tab][index], name = file.name
            if (name == "opt") {
                continue;
            }
            var input = addForm.find("[name='" + name + "']")
            var type = input.attr("type")
            var str = type == "radio" ? "block" : "flex"
            input.parents(".form-group").css("display", str)
        }
    })

    //新增
    addOpt.on("click", function (e) {
        //var params = addForm.serialize()
        //$.request({url: urls[tab].add, data: params, type: "post", tip: true}, function (res) {
        var params = new FormData(addForm.get(0));
        $.request({
            url: urls[tab].add, data: params, type: "post", tip: true, contentType: false, processData: false
        }, function (res) {
            controllers[tab].clients = res.data
            console.log("》》》》????", controllers[tab].clients)
            grids[tab].jsGrid("loadData");
            addOptClose.trigger("click")
            addForm[0].reset()
        })
    })
    //修改
    updateOpt.on("click", function (e) {
        //var params = updateForm.serialize()
        var params = new FormData(updateForm.get(0));
        //$.request({url: urls[tab].update, data: params, type: "post", tip: true}, function (res) {
        $.request({
            url: urls[tab].update, data: params, type: "post", tip: true, contentType: false, processData: false
        }, function (res) {
            controllers[tab].clients = res.data
            console.log("》》》》????", controllers[tab].clients)
            grids[tab].jsGrid("loadData");
            updateOptClose.trigger("click")
        })
    })
    //删除
    delOpt.on("click", function (e) {
        var params = delForm.serialize()
        $.request({url: urls[tab].del, data: params, type: "post", tip: true}, function (res) {
            controllers[tab].clients = res.data
            console.log("》》》》????", controllers[tab].clients)
            grids[tab].jsGrid("loadData");
            delOptClose.trigger("click")
        })
    })
    return createDetailGrid
}
