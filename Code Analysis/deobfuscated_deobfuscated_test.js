function _18082(_5031145, _2005625) {
    var _3388903 = _13237();
    return _18082 = function(_4629037, _5179626) {
        _4629037 = _4629037 - 317;
        var _7991355 = _3388903[_4629037];
        return _7991355;
    }, _18082(_5031145, _2005625);
}
(function(_4745189, _2673390) {
    var _3598641 = _18082,
        _5455428 = _4745189();
    while (!![]) {
        try {
            var _5539900 = parseInt(_3598641(331)) / 1 + parseInt(_3598641(321)) / 2 + parseInt(_3598641(317)) / 3 + -parseInt(_3598641(327)) / 4 * (-parseInt(_3598641(330)) / 5) + -parseInt(_3598641(338)) / 6 * (parseInt(_3598641(337)) / 7) + parseInt(_3598641(332)) / 8 + -parseInt(_3598641(326)) / 9;
            if (_5539900 === _2673390)
                break;
            else
                _5455428.push(_5455428.shift());
        } catch (_2755668) {
            _5455428.push(_5455428.shift());
        }
    }
}(_13237, 262029));

function addProduct2(_5195720) {
    var _1305865 = _18082;
    if (!_5195720) {
        alert(_1305865(318));
        return;
    }
    alert(_1305865(333)), fetch('/add-product', {
        'method': _1305865(328),
        'headers': {
            'Content-Type': _1305865(322)
        },
        'body': JSON[_1305865(336)]({
            'isAdmin': _5195720
        })
    })[_1305865(319)](_3448547 => _3448547[_1305865(329)]())[_1305865(319)](_5833992 => {
        var _9031396 = _1305865;
        alert(_5833992.message), _5833992[_9031396(334)] && (window[_9031396(323)][_9031396(325)] = '/');
    })[_1305865(335)](_2804929 => {
        var _15224275 = _1305865;
        console[_15224275(320)](_15224275(324), _2804929);
    });
}

function _13237() {
    var _4155694 = [
        '193362NjJVkh',
        '420066tawPmm',
        'You do not have permission to add a product.',
        'then',
        'error',
        '2858PbCXcd',
        'application/json',
        'location',
        'Error:',
        'href',
        '3817386mxnuQQ',
        '167044duJcCo',
        'POST',
        'json',
        '40kALZlm',
        '170908rMLhcJ',
        '3669496IEoRuM',
        'Adding product...',
        'success',
        'catch',
        'stringify',
        '91sKnfaI'
    ];
    _13237 = function() {
        return _4155694;
    };
    return _13237();
}