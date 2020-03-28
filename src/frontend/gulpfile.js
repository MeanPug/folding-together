const postcss = require('gulp-postcss');
const { src, dest, series, watch } = require('gulp');

function css() {
    return src('gateway/static/css/style.css')
        .pipe(postcss([
            require('tailwindcss'),
            require('autoprefixer'),
        ]))
        .pipe(dest('gateway/static/build/'));
}

exports.dev = function() {
    watch('gateway/static/css/*.css', css);
};
exports.default = series(css);
