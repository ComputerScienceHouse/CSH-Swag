var gulp = require('gulp');

// Copy vendor files from /node_modules into /vendor
// NOTE: requires `npm install` before running!
gulp.task('copy', function() {
  gulp.src([
      'node_modules/bootstrap/dist/**/*',
      '!**/npm.js',
      '!**/bootstrap-theme.*',
      '!**/*.map'
    ])
    .pipe(gulp.dest('Swag/static/vendor/bootstrap'))

    gulp.src([
      'node_modules/select2-bootstrap-theme/dist/**/*'
    ])
    .pipe(gulp.dest('Swag/static/vendor/select2-bootstrap-theme'))

    gulp.src([
      'node_modules/chart.js/dist/*.js'
    ])
    .pipe(gulp.dest('Swag/static/vendor/chart.js'))

  gulp.src(['node_modules/jquery/dist/jquery.js', 'node_modules/jquery/dist/jquery.min.js'])
    .pipe(gulp.dest('Swag/static/vendor/jquery'))
})
