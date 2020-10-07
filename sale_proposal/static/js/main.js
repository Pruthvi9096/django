
function removeItem(btn,type){
    var total = $('#id_' + type + '-TOTAL_FORMS').val();
    total--;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
    var siblings = $(btn).closest('.added-row').nextAll('.added-row')
    siblings.each(function (index,el){
        $(el).find('.form-control').each(function (i,input){
            var num = parseInt($(this).attr('id').split('-')[1])
            var name = $(this).attr('name').replace('-' + num + '-','-' + (num-1) + '-');
            var id = 'id_' + name;
            $(this).attr({'name': name, 'id': id});
        })
    })
    var item = btn.closest('.added-row').remove()
}

function cloneMore(selector, type) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + type + '-TOTAL_FORMS').val();
    newElement.find(':input').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    newElement.find('label').each(function() {
        var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
        $(this).attr('for', newFor);
    });
    total++;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    newElement.find('.delete-line').removeClass('d-none');
    newElement.find('.delete-line').html('<span id="remove-line"><i  class="fa fa-trash custom-delete"/></span>')
}