function color(data) {
    return "<span class='badge badge-" + data.toLowerCase() + "'>" + data + "</span>";
}

function image(data) {
    if (data != null) {
        return "<img class='img-thumbnail table' src='" + data + "'>";
    } else {
        return "<img class='img-thumbnail table' src='https://placehold.it/25x25'>";
    }
}

function member(data) {
    if (data != null) {
        return "<img class='img-thumbnail table' src='https://profiles.csh.rit.edu/image/" + data + "'>";
    } else {
        return "<img class='img-thumbnail table' src='https://placehold.it/25x25'>";
    }
}

function method(data) {
    if (data != null) {
        return "<span class='badge badge-" + data.toLowerCase() + "'>" + data + "&nbsp;<i class='fa fa-check'></i></span>";
    } else {
        return "<i class='fa fa-times' style='color: red'></i>";
    }
}

function cost(data) {
    return "$" + data;
}
