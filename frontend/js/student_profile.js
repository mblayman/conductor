import $ from 'jquery';
import 'datatables';

export default function(data) {
  $('#schools').DataTable({
    info: false,
    paging: false,
    searching: false
  });
}
