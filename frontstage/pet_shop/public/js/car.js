window.layui.define(['layer'], function (exports) {
    var car = {
        init: function () {
            var uls = document.getElementById('list-cont').getElementsByTagName('ul');//每一行
            var checkInputs = document.getElementsByClassName('check'); // 所有勾选框
            var checkAll = document.getElementsByClassName('check-all'); //全选框
            var SelectedPieces = document.getElementsByClassName('Selected-pieces')[0];//总件数
            var piecesTotal = document.getElementsByClassName('pieces-total')[0];//总价
            //计算
            function getTotal() {
                var seleted = 0, price = 0;
                for (var i = 0; i < uls.length; i++) {
                    if (uls[i].getElementsByTagName('input')[0].checked) {
                        seleted += parseInt(uls[i].getElementsByClassName('Quantity-input')[0].value);
                        price += parseFloat(uls[i].getElementsByClassName('sum')[0].innerHTML);
                    }
                }
                SelectedPieces.innerHTML = seleted;
                piecesTotal.innerHTML = '￥' + price.toFixed(2);
            }

            // 小计
            function getSubTotal(ul) {
                var unitprice = parseFloat(ul.getElementsByClassName('th-su')[0].innerHTML);
                var count = parseInt(ul.getElementsByClassName('Quantity-input')[0].value);
                var SubTotal = parseFloat(unitprice * count)
                ul.getElementsByClassName('sum')[0].innerHTML = SubTotal.toFixed(2);
            }

            for (var i = 0; i < checkInputs.length; i++) {
                checkInputs[i].onclick = function () {
                    if (this.className === 'check-all check') {
                        for (var j = 0; j < checkInputs.length; j++) {
                            checkInputs[j].checked = this.checked;
                        }
                    }
                    if (this.checked === false) {
                        for (var k = 0; k < checkAll.length; k++) {
                            checkAll[k].checked = false;
                        }
                    }
                    getTotal()
                }
            }

            for (var i = 0; i < uls.length; i++) {
                uls[i].onclick = function (e) {
                    e = e || window.event;
                    var el = e.srcElement;
                    var cls = el.className;
                    var input = this.getElementsByClassName('Quantity-input')[0];
                    var val = parseInt(input.value);
                    switch (cls) {
                        case 'add layui-btn':
                            input.value = val + 1;
                            getSubTotal(this)
                            break;
                        case 'less layui-btn':
                            if (val > 1) {
                                input.value = val - 1;
                            }
                            getSubTotal(this)
                            break;
                    }
                    getTotal()
                }
            }
            checkAll[0].checked = true;
            checkAll[0].onclick();
        }

    }


    exports('car', car)
});
