function createSetApp(columns, url) {
    var addForm = $("#addModal form")
    var addOpt = $("#addOpt")
    var addOptClose = $("#addOptClose")

    var updateForm = $("#updateModal form")
    var updateOpt = $("#updateOpt")
    var updateOptClose = $("#updateOptClose")
    var updateModalBtn = $("#updateModalBtn")

    var delForm = $("#delModal form")
    var delOpt = $("#delOpt")
    var delOptClose = $("#delOptClose")
    var delModalBtn = $("#delModalBtn")

    jsGrid.locale("zh-cn");
    var gridList = $("#jsGrid1")
    var controller = {
        loadData: function (filterRow) {
            console.log("》》》》loadData", controller.clients, controller.clients.length, controller, filterRow)
            //return controller.clients
            return $.grep(controller.clients, function (row) {
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
    var fields = columns.concat([
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
                    type == "back" ? gridList.jsGrid("clearFilter").done(function () {
                        console.log("清空搜索条件完成");
                    }) : gridList.jsGrid("loadData");
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
                            updateForm[0].reset()
                            updateModalBtn.trigger("click")
                            updateForm.find("[name='id']").val(item.id)
                            updateForm.find("[name='number']").val(item.number)
                            updateForm.find("[name='name']").val(item.name)
                        } else if (type == "delete") {
                            delModalBtn.trigger("click")
                            delForm.find("[name='id']").val(item.id)
                        }

                        //$.request({url: "/set/exhibit/add", data: {name: "大厅", number: 3}}, function (res) {
                        //controller.clients = res.data
                        //gridList.jsGrid("loadData");
                        //})
                    })
            }

        }
    ])

    gridList.jsGrid({
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
        controller: controller,
        fields: fields
    });

    //查询
    $.request({url: url.list}, function (res) {
        controller.clients = res.data
        console.log("》》》》????", controller.clients)
        gridList.jsGrid("loadData");
    })

    //新增
    addOpt.on("click", function (e) {
        var params = addForm.serialize()
        $.request({url: url.add, data: params, type: "post", tip: true}, function (res) {
            controller.clients = res.data
            console.log("》》》》????", controller.clients)
            gridList.jsGrid("loadData");
            addOptClose.trigger("click")
            addForm[0].reset()
        })
    })
    //修改
    updateOpt.on("click", function (e) {
        var params = updateForm.serialize()
        $.request({url: url.update, data: params, type: "post", tip: true}, function (res) {
            controller.clients = res.data
            console.log("》》》》????", controller.clients)
            gridList.jsGrid("loadData");
            updateOptClose.trigger("click")
        })
    })
    //删除
    delOpt.on("click", function (e) {
        var params = delForm.serialize()
        $.request({url: url.del, data: params, type: "post", tip: true}, function (res) {
            controller.clients = res.data
            console.log("》》》》????", controller.clients)
            gridList.jsGrid("loadData");
            delOptClose.trigger("click")
        })
    })
}