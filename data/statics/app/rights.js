function createDevApp(columns, url) {
    // var exhibitSelector = $("#exhibitSelector")
    // exhibitSelector.on("change", function (e) {
    //     //var options = exhibitSelector.find("option:selected").val(); //获取选中的项
    //     var options = exhibitSelector.val()
    //     console.log("selector>>", options)
    //     options != null && addForm.find("[name='exhibit']").val(options)
    //     //查询
    //     $.request({url: url.list, data: {exhibit: options}}, function (res) {
    //         controller.clients = res.data
    //         console.log("》》》》????", controller.clients)
    //         gridList.jsGrid("loadData");
    //     })
    // })
    // $.request({url: "/set/exhibit/list"}, function (res) {
    //     console.log(">>", res)
    //     var data = res.data
    //     exhibitSelector.html("")
    //     for (var i  in data) {
    //         var item = data[i], val = item.id, name = item.name
    //         exhibitSelector.append($.parseHTML("<option value='" + val + "'>" + name + "</option>"))
    //     }
    //     exhibitSelector.trigger("change")
    // })

    // var addForm = $("#addModal form")
    // var addOpt = $("#addOpt")
    // var addOptClose = $("#addOptClose")

    var refreshLinks = function (links) {
        var linksStr = ""
        for (var i in links) {
            var link = links[i], id = link.id
            linksStr += '<div class="icheck-primary d-inline">' +
                '<input type="checkbox" id="checkbox_' + id + '" value=' + id + '>' +
                '<label for="checkbox_' + id + '">' + link.name + '&nbsp;&nbsp;&nbsp;&nbsp;</label>' +
                '</div>'
        }
        linkForm.find(".form-group.clearfix").html(linksStr)
    }

    var updateForm = $("#updateModal form")
    var updateOpt = $("#updateOpt")
    var updateOptClose = $("#updateOptClose")
    var updateModalBtn = $("#updateModalBtn")

    var delForm = $("#delModal form")
    var delOpt = $("#delOpt")
    var delOptClose = $("#delOptClose")
    var delModalBtn = $("#delModalBtn")

    var linkForm = $("#linksModal form")
    var linksOpt = $("#linksOpt")
    var linksOptClose = $("#linksOptClose")
    var linkModalBtn = $("#linksModalBtn")

    $('.select2').select2()
    jsGrid.locale("zh-cn");
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
                var btnStr = parseInt($.pattern()) == 0 ? '<button type="button" class="btn btn-default" data-type="theme">主题</button>' : ''
                return $('<div class="btn-group">' +
                    '<button type="button" class="btn btn-default" data-type="update">修改</button>' +
                    '<button type="button" class="btn btn-default" data-type="delete">删除</button>' +
                    btnStr +
                    '</div>').on("click", "button",
                    function (e) {
                        e.stopPropagation();
                        var $el = $(this), type = $el.data("type")
                        if (type == "update") {
                            updateForm[0].reset()
                            updateModalBtn.trigger("click")
                            for (var i in fields) {
                                var name = fields[i].name
                                var $el = updateForm.find("[name='" + name + "']")
                                var val = item[name]
                                if ($el.attr("type") == "radio") {
                                    //$el.prop("checked",false);
                                    $el.each(function () {
                                        var $radio = $(this), radioVal = $radio.val()
                                        if (radioVal <= val) {
                                            console.log(">>>>", $radio.val(), val)
                                            $radio.prop("checked", true);
                                        }
                                    })
                                } else {
                                    $el.val(val)
                                }
                            }
                            //updateForm.find("[name='number']").val(item.number)
                            //updateForm.find("[name='name']").val(item.name)
                        } else if (type == "delete") {
                            delModalBtn.trigger("click")
                            delForm.find("[name='id']").val(item.id)
                            delForm.find("[name='exhibit']").val(item.exhibit)
                        } else if (type == "theme") {
                            var row = controller.clients.indexOf(item)
                            linksOpt.attr("row", row)
                            linkForm[0].reset()
                            linkForm.find("[name='id']").val(item.id)
                            // linkForm.find("[name='exhibit']").val(item.exhibit)
                            var show = {display: "inline-block"}, hidden = {display: "none"}
                            // linkForm.find("#checkbox_" + item.id).css(hidden).siblings().css(hidden).parents(".icheck-primary.d-inline").css(hidden).siblings().css(show).children().css(show)
                            if (item.theme == "all") {
                                linkForm.find("[id^='checkbox_']").prop("checked", true)
                            } else {
                                var links = []
                                try {
                                    links = JSON.parse(item.theme)
                                } catch (e) {
                                    console.log("item.theme不是JSON格式！")
                                }
                                for (var i in links) {
                                    var linkId = links[i]
                                    linkForm.find("#checkbox_" + linkId).prop("checked", true)
                                }
                            }

                            linkModalBtn.trigger("click")
                        }

                        //$.request({url: "/set/exhibit/add", data: {name: "大厅", number: 3}}, function (res) {
                        //controller.clients = res.data
                        //gridList.jsGrid("loadData");
                        //})
                    })
            }

        }
    ])

    var gridList = $("#contentList")
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
        console.log("》》》》theme>>", res.theme)
        gridList.jsGrid("loadData");
        refreshLinks(res.theme)
    })
    //新增
    // addOpt.on("click", function (e) {
    //     var params = addForm.serialize()
    //     $.request({url: url.add, data: params, type: "post", tip: true}, function (res) {
    //         controller.clients = res.data
    //         console.log("》》》》????", controller.clients)
    //         gridList.jsGrid("loadData");
    //         addOptClose.trigger("click")
    //         addForm[0].reset()
    //     })
    // })
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
            refreshLinks(res.theme)
        })
    })

    //关联
    linksOpt.on("click", function (e) {
        var check_list = [], nocheck_list = [], $el = $(this)
        linkForm.find("input[type='checkbox']:checked").each(function () {
            check_list.push($(this).val())
        })
        linkForm.find("input[type='checkbox']:not(:checked)").each(function () {
            nocheck_list.push($(this).val())
        })
        var theme = nocheck_list.length > 0 ? check_list.join(",") : "all"
        console.log(check_list.join(","))
        $.request({
            url: url.theme,
            data: {"theme": theme, "id": linkForm.find("[name='id']").val()},
            type: "post",
            tip: true
        }, function (res) {
            var index = parseInt($el.attr("row"))
            console.log(">>>>>?>>", res.data, index, controller.clients[index])
            controller.clients[index].theme = res.data
            gridList.jsGrid("loadData");
            linksOptClose.trigger("click")
        })
    })
}