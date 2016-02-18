import $ from 'jquery';
import foundation from 'foundation-sites';

$(document).foundation();

$('#add-experience').click(() => {
    $('#experiences-holder').append('\
            <label>Title<input type="text" name="title[]"></label>\
            <label>Company and Time<input type="text" name="companyAndTime[]"></label>');
});

$('#add-education').click(() => {
    $('#educations-holder').append('\
            <label>Place<input type="text" name="place[]"></label>\
            <label>Degree<input type="text" name="degree[]"></label>\
            <label>Time<input type="text" name="time[]"></label>');
});

const getKey = () => document.location.search.substr(1).split('=')[1];

const updateImage = () => {

    const titles = $('input[name="title[]"]').map(function () { return $(this).val(); }).get();
    const companiesAndTimes = $('input[name="companyAndTime[]"]').map(function () { return $(this).val(); }).get();

    let experiences = [];
    for (let i = 0; i < titles.length; ++i) {
        experiences.push({'title': titles[i], "companyAndTime": companiesAndTimes[i]});
    }

    const places = $('input[name="place[]"]').map(function () { return $(this).val(); }).get();
    const degrees = $('input[name="degree[]"]').map(function () { return $(this).val(); }).get();
    const times = $('input[name="time[]"]').map(function () { return $(this).val(); }).get();

    let educations = [];
    for (let i = 0; i < places.length; ++i) {
        educations.push({'place': places[i], "degree": degrees[i], 'time': times[i]});
    }

    let social = {};

    let email = $('input[name="email"]').val();
    Object.assign(social, email.length > 0 ? {'email': email} : {});

    let twitter = $('input[name="twitter"]').val();
    Object.assign(social, twitter.length > 0 ? {'twitter': twitter} : {});

    let linkedin = $('input[name="linkedin"]').val();
    Object.assign(social, linkedin.length > 0 ? {'linkedin': linkedin} : {});

    const key = getKey();
    return $.ajax('/cv?type=png&base64&key=' + key, {
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(
            {"keywords": $('input[name="keywords"]').val().split(',').map(s => s.trim()),
             "name": $('input[name="name"]').val(),
             "title": $('input[name="title"]').val(),
             "intro": $('#intro-text').val().split('\n\n'),
             "experiences": experiences,
             "educations": educations,
             "social": social
            })
    }).done((resp) => $("#preview").attr('src', 'data:image/png;base64,' + resp));
};

$('#update').click(updateImage);

$('#file-upload').change(function () {
    const file = this.files[0];
    let reader = new FileReader();
    const suffix = file.type === 'image/png' ? '.png' : (file.type === 'image/jpg' || file.type === 'image/jpeg') ? '.jpg' : '';
    if (suffix.length === 0) throw new Error("Only .png and .jpg are supported");

    reader.onloadend = () => {
        $.ajax('/upload?filename=' + getKey() + suffix + '&key=' + getKey(), {
            type: 'POST',
            contentType: file.type,
            data: reader.result,
            processData: false
        });
    };
    reader.readAsArrayBuffer(file);
});

updateImage();
