function Api(){
    this.root = '/';
}

var api = new Api();

var modal_dialog    = new ModalDialog('lv1');
var modal_subdialog = new ModalDialog('lv2');
var modal_confirm   = new ModalDialog('lv3');
var modal_errors    = new ModalDialog('errors');
