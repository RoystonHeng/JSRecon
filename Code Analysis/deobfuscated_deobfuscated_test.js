(function(_0x17cfe3, _0x335a63) {
    var _0x3aa63b = _0x1b7a,
        _0x53a0b8 = _0x17cfe3();
    while (!![]) {
        try {
            var _0x3daf75 = -parseInt(_0x3aa63b(0xa2)) / 0x1 + -parseInt(_0x3aa63b(0x9f)) / 0x2 + parseInt(_0x3aa63b(0x98)) / 0x3 * (-parseInt(_0x3aa63b(0x9a)) / 0x4) + -parseInt(_0x3aa63b(0x9c)) / 0x5 * (parseInt(_0x3aa63b(0xa8)) / 0x6) + -parseInt(_0x3aa63b(0xa5)) / 0x7 + parseInt(_0x3aa63b(0x9b)) / 0x8 + -parseInt(_0x3aa63b(0xa4)) / 0x9 * (-parseInt(_0x3aa63b(0x97)) / 0xa);
            if (_0x3daf75 === _0x335a63) break;
            else _0x53a0b8.push(_0x53a0b8.shift());
        } catch (_0x1ab59d) {
            _0x53a0b8.push(_0x53a0b8.shift());
        }
    }
}(_0x3546, 0xc0744));

function _0x1b7a(_0x489412, _0x2e496a) {
    var _0x354678 = _0x3546();
    return _0x1b7a = function(_0x1b7a84, _0x3bf341) {
        _0x1b7a84 = _0x1b7a84 - 0x93;
        var _0x47a27e = _0x354678[_0x1b7a84];
        return _0x47a27e;
    }, _0x1b7a(_0x489412, _0x2e496a);
}

function _0x3546() {
    var _0x28d63d = ['827541fSlcmD', 'success', '4853106OlsFIL', '4011693uQdXon', 'location', 'href', '552FdSrTb', 'error', 'then', 'stringify', 'catch', '70ddVpqw', '91311yXioMj', 'Adding product...', '100LDGRBY', '6412640Oosfys', '22765nqxeZg', 'Error:', '/add-product', '2414970XYinkS', 'POST', 'You do not have permission to add a product.'];
    _0x3546 = function() {
        return _0x28d63d;
    };
    return _0x3546();
}

function addProduct2(_0x3ab3e0) {
    var _0x55d617 = _0x1b7a;
    if (!_0x3ab3e0) {
        alert(_0x55d617(0xa1));
        return;
    }
    alert(_0x55d617(0x99)), fetch(_0x55d617(0x9e), {
        'method': _0x55d617(0xa0),
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': JSON[_0x55d617(0x95)]({
            'isAdmin': _0x3ab3e0
        })
    })['then'](_0x3dccac => _0x3dccac.json())[_0x55d617(0x94)](_0x5e08ea => {
        var _0x294995 = _0x55d617;
        alert(_0x5e08ea.message), _0x5e08ea[_0x294995(0xa3)] && (window[_0x294995(0xa6)][_0x294995(0xa7)] = '/');
    })[_0x55d617(0x96)](_0x2fd5c5 => {
        var _0x30e8f2 = _0x55d617;
        console[_0x30e8f2(0x93)](_0x30e8f2(0x9d), _0x2fd5c5);
    });
}