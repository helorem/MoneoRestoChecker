function fixed_size(str, count, prefix)
{
    res = (prefix + str).slice(-count);
    return res;
}

function convert_datetime(dt, time)
{
    var res = ""
    var dt = new Date(dt);
    var weekdays = ["Dimanche", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"];
    var months = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre", "novembre", "décembre"];

    res = weekdays[dt.getDay()]
        + " " + dt.getDate()
        + " " + months[dt.getMonth()]
        + " " + dt.getFullYear()

    if (time)
    {
        res += " à " + fixed_size(dt.getHours(), 2, "0")
        + "h" + fixed_size(dt.getMinutes(), 2, "0");
    }

    return res;
}

function logout()
{
    var res = $.get("api/logout");
    res.done(function(data) { document.location.assign("login.htm"); });
    res.fail(function(data) { console.error(data.responseText); });
}

function show_message(msg, type)
{
    /**
      * Show a message after a validation.
      * @param msg the message displayed
      * @param type the type of message in (error, success). If not specified, the remaining message is cleared.
      */
    var $msg_box = $("#message_box");
    if (type == "error")
    {
        $msg_box.html('<div class="ui visible error message"><div class="header">Erreur</div><p>' + msg + '</p></div>');
    }
    else if (type == "success")
    {
        $msg_box.html('<div class="ui visible success message"><div class="header">Succes</div><p>' + msg + '</p></div>');
    }
    else
    {
        $msg_box.html('');
    }
}

function display_header(text, path_prefix)
{
    if (!path_prefix)
    {
        path_prefix = ".";
    }

    var $root = $('body');

    var $div;

    $div = $('<div class="ui menu" />');
    var page_name = location.pathname

    var pages = {
        "index.htm" : ["Accueil", "/moneoresto_checker/index.htm"],
        "transactions.htm" : ["Transactions", "/moneoresto_checker/transactions.htm"],
    };

    var $item;
    var p_item;
    for (href in pages)
    {
        p_item = pages[href];
        $item = $('<a class="blue item" />').text(p_item[0]).attr("href", href);
        if (location.pathname == p_item[1])
        {
            $item.addClass("active");
        }
        $div.append($item);
    }
    var $div2 = $('<div class="right menu" />');
    var $item = $('<div class="item" />');
    $item.append($('<div class="ui button" />').text("Deconnexion").attr("onclick", "logout()"));
    $div2.append($item);
    $div.append($div2);
    $root.prepend($div);

    $div = $('<div class="logo header" />');
    $div.append($('<h1 />').text(text));
    $root.prepend($div);
}

function test_logged()
{
    var res = $.ajax({
            url : "api/is_logged",
            dataType : "json",
            async : false
        });
    res.done(function(data) {
            if (!data)
            {
                document.location.assign("login.htm");
            }
        });
    res.fail(function(data) {
            switch (data.status)
            {
                case 403:
                    document.location.assign("login.htm");
                    break;
                default:
                    console.error(data.responseText);
                    document.location.assign("login.htm");
            }
        });
}

