var gulp = require('gulp');
var cleanCSS = require('gulp-clean-css');
var rename = require("gulp-rename");

// Minify CSS
gulp.task('css:minify', ['sass:compile'], function() {
  return gulp.src([
      'Swag/static/css/*.css',
      '!Swag/static/css/*.min.css'
    ])
    .pipe(cleanCSS())
    .pipe(rename({
      suffix: '.min'
    }))
    .pipe(gulp.dest('Swag/static/css'));
});
