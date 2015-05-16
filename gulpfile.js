var gulp = require('gulp')
  , uglify = require('gulp-uglifyjs')
  , minifyCss = require('gulp-minify-css')
  , rimraf = require('gulp-rimraf');

gulp.task('default', ['web-resources', 'uglify', 'minify-css']);

gulp.task('clean', function () {
  return gulp.src([
      destinationStatic('/'),
      destinationTemplates('/')],
    { read: false })
    .pipe(rimraf());
});

gulp.task('web-resources', ['clean'], function () {
  // served by Flask (static HTML+layouts)
  gulp.src(['web/html/index.html']).pipe(gulp.dest(destinationTemplates('/')));
  gulp.src(['web/html/layouts/*.html']).pipe(gulp.dest(destinationTemplates('/layouts/')));

  // served by AngularJS (on-demand templates)
  gulp.src(['web/html/partials/*.html']).pipe(gulp.dest(destinationStatic('/partials')));
});

gulp.task('uglify', ['uglify-bespoke', 'uglify-vendor']);

gulp.task('uglify-bespoke', ['clean'], function () {
  gulp.src(['web/js/**/*.js'])

    // don't minify bespoke sources during development; save that for later
    // .pipe(uglify('hipflask.min.js'))

    .pipe(gulp.dest(destinationStatic('/js')));
});

gulp.task('uglify-vendor', ['clean'], function () {
  gulp.src([
    source('/lodash/dist/lodash.js'),
    source('/jquery/dist/jquery.js'),
    source('/bootstrap-css/js/bootstrap.js'),
    source('/angular/angular.js'),
    source('/angular-ui-router/release/angular-ui-router.js')
  ])
    .pipe(uglify('vendor.min.js'))
    .pipe(gulp.dest(destinationStatic('/js/vendor')));
});

gulp.task('minify-css', ['clean'], function () {
  gulp.src([
    // vendor
    source('/bootstrap-css/css/bootstrap.css'),
    source('/bootstrap-css/css/bootstrap-theme.css'),
    // bespoke
    'web/css/rainbow.css'
  ])
    .pipe(minifyCss())
    .pipe(gulp.dest(destinationStatic('/css')));
});

function source (glob) {
  return 'bower_components' + glob;
}
function destinationStatic (glob) {
  return 'hipflask/static' + glob;
}
function destinationTemplates (glob) {
  return 'hipflask/templates' + glob;
}
