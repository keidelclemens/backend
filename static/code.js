var data = {};

Array.prototype.move = function(old_index, new_index) {
    if (new_index >= this.length) {
        var k = new_index - this.length;
        while ((k--) + 1) {
            this.push(undefined);
        }
    }
    this.splice(new_index, 0, this.splice(old_index, 1)[0]);
    return this; // for testing purposes
};

function changevalue(el) {
    var x = el.value;
    console.log(x);
    switch (el.id) {
        case 'owner':
            load_owner(x);
            break;
        case 'book':
            load_book(x);
            break;
        case 'chapters':
            load_chapter(x);
            break;
        case 'book_title':
            data[selected_owner()][selected_book_index()].title = x;
            document.getElementById('book').options[selected_book_index()].innerHTML = x;
            break;
        case 'book_url':
            data[selected_owner()][selected_book_index()].url = x;
            break;
        case 'book_description':
            data[selected_owner()][selected_book_index()].content = x;
            break;
        case 'redirect_url':
            data[selected_owner()][selected_book_index()].redirect_url = x;
            break;
        case 'chapter_title':
            data[selected_owner()][selected_book_index()].chapters[selected_chapter_index()].title = x
            document.getElementById('chapters').options[selected_chapter_index()].innerHTML = x;
            break;
        case 'chapter_url':
            data[selected_owner()][selected_book_index()].chapters[selected_chapter_index()].url = x;
            break;
        case 'chapter_contents':
            data[selected_owner()][selected_book_index()].chapters[selected_chapter_index()].content = x;
            break;
    }
}

function change_txt_value(el_id) {
  console.log(el_id);
  var new_value = CKEDITOR.instances[el_id].getData();
  console.log(new_value);
  switch(el_id) {
    case 'book_description':
      data[selected_owner()][selected_book_index()].content = new_value;
      break;
    case 'chapter_contents':
      data[selected_owner()][selected_book_index()].chapters[selected_chapter_index()].content = new_value;
      break;
  }
}

function load_owner(owner) {
    $('#book').empty();
    $('#chapters').empty();
    for (var i = 0; i < data[owner].length; i++) {
        $('#book').append($('<option>', {
            value: data[owner][i].url,
            text: data[owner][i].title
        }));
    }
    // clear everything else
    $("#book").val("");
    $("#book_title").val("");
    $("#book_url").val("");
    CKEDITOR.instances.book_description.setData("");
    $("#chapters").val("");
    $("#chapter_title").val("");
    $("#chapter_url").val("");
    CKEDITOR.instances.chapter_contents.setData("");
    load_book(0);
}

function load_book(book) {
    if (selected_book_index() == -1) {
        return;
    }
    $("#book_title").val(data[selected_owner()][selected_book_index()].title);
    $("#book_url").val(data[selected_owner()][selected_book_index()].url);
    CKEDITOR.instances.book_description.setData(data[selected_owner()][selected_book_index()].content);
    $("#redirect_url").val(data[selected_owner()][selected_book_index()].redirect_url);
    $('#chapters').empty();
    for (var i = 0; i < data[selected_owner()][selected_book_index()].chapters.length; i++) {
        $('#chapters').append($('<option>', {
            value: data[selected_owner()][selected_book_index()].chapters[i].url,
            text: data[selected_owner()][selected_book_index()].chapters[i].title
        }));
    }
    // clear everything else
    $("#chapters").val("");
    $("#chapter_title").val("");
    $("#chapter_url").val("");
    CKEDITOR.instances.chapter_contents.setData("");
}

function load_chapter(chapter) {
    $("#chapter_title").val(data[selected_owner()][selected_book_index()].chapters[selected_chapter_index()].title);
    $("#chapter_url").val(data[selected_owner()][selected_book_index()].chapters[selected_chapter_index()].url);
    CKEDITOR.instances.chapter_contents.setData(data[selected_owner()][selected_book_index()].chapters[selected_chapter_index()].content);
}

function selected_book_index() {
    return document.getElementById('book').selectedIndex;
}

function selected_owner() {
    return document.getElementById('owner').value;
}

function selected_chapter_index() {
    return document.getElementById('chapters').selectedIndex;
}

function add_a_book() {
    data[selected_owner()].push({
        "content": "",
        "url": "",
        "title": "Title",
        "chapters": []
    });
    $('#book').append($('<option>', {
        value: "",
        text: "Title"
    }));
}

function add_a_chapter() {
    data[selected_owner()][selected_book_index()].chapters.push({
        "content": "",
        "url": "",
        "chapters": [],
        "redirect_url": "",
        "title": "Title"
    });
    console.log('test');
    $('#chapters').append($('<option>', {
        value: "",
        text: "Title"
    }));
}

function delete_a_chapter() {
    data[selected_owner()][selected_book_index()].chapters.splice(selected_chapter_index(), 1);
    document.getElementById('chapters').remove(selected_chapter_index());
}

function delete_a_book() {
    data[selected_owner()].splice(selected_book_index(), 1);
    document.getElementById('book').remove(selected_book_index());
}

function moveUp(selectId) {
    var selectList = document.getElementById(selectId);
    var selectOptions = selectList.getElementsByTagName('option');
    for (var i = 1; i < selectOptions.length; i++) {
        var opt = selectOptions[i];
        if (opt.selected) {
            selectList.removeChild(opt);
            selectList.insertBefore(opt, selectOptions[i - 1]);
        }
    }
    switch (selectId) {
        case 'book':
            var place = selected_book_index();
            data[selected_owner()].move(place, place + 1);
            break;
        case 'chapters':
            var place = selected_chapter_index();
            data[selected_owner()][selected_book_index()].chapters.move(place, place + 1);
    }
}

function moveDown(selectId) {
    var selectList = document.getElementById(selectId);
    var selectOptions = selectList.getElementsByTagName('option');
    for (var i = selectOptions.length - 2; i >= 0; i--) {
        var opt = selectOptions[i];
        if (opt.selected) {
            var nextOpt = selectOptions[i + 1];
            opt = selectList.removeChild(opt);
            nextOpt = selectList.replaceChild(opt, nextOpt);
            selectList.insertBefore(nextOpt, opt);
        }
    }
    switch (selectId) {
        case 'book':
            var place = selected_book_index();
            data[selected_owner()].move(place, place - 1);
            break;
        case 'chapters':
            var place = selected_chapter_index();
            data[selected_owner()][selected_book_index()].chapters.move(place, place - 1);
    }
}

$(document).ready(function() {
    retrieve_data();
});

function save_data() {
  document.getElementById("submit").disabled = true; 
  console.log('test');
    $.ajax({
       url: '/save/',
       type: "POST",
       dataType: "json",
       data: {'data': JSON.stringify(data),
              'csrfmiddlewaretoken': window.csrf_token
       },
       statusCode: {
         200: function (your_Response_Data) {
            alert('Your changes are being uploaded.  They should appear on the site in a few minutes.');
            document.getElementById("submit").disabled = false; 
          },
          // ... handle errors if required
          404: function () {
             alert('There was an error.');
          }
       },
       complete: function (jqXHR, textStatus) {
          // Things to do after everything is completed
       }
    });
};

function retrieve_data() {
  $.ajax({
    url : '/retrieve/',
    dataType : 'json',
    type : 'GET',
    statusCode: {
      200: function(d) {
        console.log(d);
        data = d;
        // start with ruth loaded
        $("#owner").val("ruth");
        load_owner('ruth');
    }}
});
}
