$(document).ready(function () {

    let slips = {};

    // updateButton();

    $(window).resize(function () {
        updateButton();
    });

    const sidebarToggle = $('.sidebar-toggle');
    const sidebar = $('.sidebar');

    sidebarToggle.on('click', function (e) {
        sidebar.toggleClass('opened');
        e.stopPropagation();
    });

    $(document).on('click', function (e) {
        closeSidebar();
    });

    function closeSidebar() {
        sidebar.removeClass('opened');
    }


    function addSlip(id, slip) {
        slips[id] = slip;
        slip.addClass('active');
    }

    function removeSlip(id) {
        slips[id].removeClass('active');
        delete slips[id];
    }

    $('.btn-price').on('click', function (e) {
        const slip = $(e.target);
        toggleSlip(slip.attr('id'), slip);
        console.log(slips);
    })

    $('.btn-price').each(function (index, element) {
        $(element).attr('id', 'btn-price-' + index);
    });

    $('.bet-btn').on('click', function (e) {
        const slip = $(e.target);
        toggleSlip(slip.attr('id'), slip);
        console.log(slips);
    })

    $('.bet-btn').each(function (index, element) {
        $(element).attr('id', 'bet-btn-' + index);
    });

    function toggleSlip(id, slip) {
        if (slips[id]) {
            removeSlip(id);
        } else {
            addSlip(id, slip);
        }
        updateButton();
    }

    function updateButton() {
        const betSlipButton = $('.btn-bet-slip');
        const betCounter = $('#slips-counter');
        const length = Object.keys(slips).length;

        if (length > 0 && $(window).width() < 990) {
            betSlipButton.show();
            betCounter.text(length);
        } else {
            betSlipButton.hide();
            $('#betSlipModal').modal('hide');
        }

        betSlipButton.on('click', function () {
            $('#betSlipModal').modal('show');
        })
    }


});