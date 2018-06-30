import $ from 'jquery';
import 'datatables';

export default function(data) {
  $('#students').DataTable({
    info: false,
    paging: false,
    searching: false
  });
}
