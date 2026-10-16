(function () {
    var isReady = false
    document.addEventListener('DOMContentLoaded', function () {
        isReady = true
    })

    initialize = function () {
        window['$id'] = function (id) { return document.getElementById(id) }
        window['$first'] = function (selector) { return document.querySelector(selector) }
        window['$all'] = function (selector) { return document.querySelectorAll(selector) }
    }

    if (isReady || document.readyState === 'complete') {
        initialize()
    } else {
        document.addEventListener('DOMContentLoaded', initialize)
    }
})()
