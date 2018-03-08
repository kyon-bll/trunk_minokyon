import tooltip from './_tooltip';
import RowClickabler from './_row-clickabler';
import './_tooltip-click';

$(function() {
  if ($('.j-row-clickable').find('[data-href]').length) {
    new RowClickabler();
  }

  if ($('[data-toggle="tooltip"]').length) {
    tooltip();
  }
});
