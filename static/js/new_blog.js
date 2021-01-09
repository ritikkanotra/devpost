$(document).ready(function() {
    $('#summernote').summernote({
        minHeight: 500
    });
    $('#summernote').summernote('fontSize', 20);
    $('#summernote').summernote('justifyLeft');
});

const inputImage = document.getElementById('input_cover_image');
const previewImage = document.getElementById('preview_cover_image');

inputImage.addEventListener("change", function() {
    const file = this.files[0];

    if (file) {
        const reader = new FileReader();

        reader.addEventListener("load", function() {
            previewImage.setAttribute("src", this.result);
        });
        reader.readAsDataURL(file);
    }
});
