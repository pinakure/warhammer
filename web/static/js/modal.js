function ModalDialog(parent_tag, container_tag) {
    this.ids                = [ parent_tag, container_tag ];
    this.node               = $(`#${parent_tag}`);
    this.content            = $(`#${container_tag}`);
    this.caption            = null;
    this.ok_callback        = '';
    this.cancel_callback    = '';
    this.dispose();
}

ModalDialog.prototype.addCaption = function(caption) {
    if (this.caption) return this.setCaption(caption);
    this.content.prepend(`<button id="modal_caption" class="btn" style="box-shadow: 0px 2px #8888;background: linear-gradient(-90deg, #002, #226);width: 100%; color:#fff;text-align: left;font-weight: 600;text-shadow: 1px 1px 0px #000;">${caption}</div>`);
    this.caption = $('#modal_caption');
}

ModalDialog.prototype.setCaption = function(caption){
    if(!this.caption)return this.addCaption(caption);
    this.caption.html(caption);
}

ModalDialog.prototype.triggerOkCallback = function(){
    eval(this.ok_callback);
    this.dispose();
}

ModalDialog.prototype.triggerCancelCallback = function(){
    eval(this.cancel_callback);
    this.dispose();
}

ModalDialog.prototype.dispose = function(){
    this.node.hide();
    this.content.hide();    
}

ModalDialog.prototype.setBody = function(body, node_tag) {
    self_dialog = this;
    this.content.html(body);
    this.content.show();
    $(`.modal_dialog#${ node_tag }`).show();
    $(`.modal_dialog_content#${ node_tag }`).show();
}

ModalDialog.prototype.setSubBody = function(body) {
    self_sdialog = this;
    this.content.html(body);
    this.content.show();
    this.node.show();
}

ModalDialog.prototype.initialize = function(parent_tag, container_tag){
    this.node       = $(`.modal_dialog#${parent_tag}`);
    this.content    = $(`.modal_dialog_content#${container_tag}`);
    this.dispose();
}

var Modal = {
    Template : function(payload, index=0){
        $('.curtain').show();
        Scenia.get('modal/', payload, function(data){
            $('.curtain').hide();
            switch(index){
                case 0: return modal_dialog.setBody(data.response, 'lv1');
                case 1: return modal_subdialog.setBody(data.response, 'lv2');
                case 2: return modal_confirm.setBody(data.response, 'lv3');
            }
        });
    },

    Config : {
        Summon : {
            General : function(){
                var payload = { 
                    operation   : 'template',
                    template    : 'config',
                };
                Scenia.Modal.Template(payload, 0);
            },
        },
    },

    Project : {
        Summon : {
            Update : function(id){
                var payload = { 
                    id          : id,
                    model       : 'Project',
                    operation   : 'update',
                    template    : 'project',
                };
                Scenia.Modal.Template(payload);
            },
            Insert : function(){
                var payload = { 
                    model       : 'Project',
                    operation   : 'insert',
                    template    : 'project',
                };
                Scenia.Modal.Template(payload);
            },
        },
    },

    Picture : {
        Summon : {
            Update : function(id){
                var payload = { 
                    id          : id,
                    model       : 'Picture',
                    operation   : 'update',
                    template    : 'picture',
                };
                Scenia.Modal.Template(payload,1);
            },
            Insert : function(foreign_key=''){
                var payload = { 
                    model       : 'Picture',
                    operation   : 'insert',
                    template    : 'picture',
                    foreign_key : foreign_key,
                };
                Scenia.Modal.Template(payload,2);
            },
        },
    },

    PictureStep : {
        Summon : {
            Update : function(id, step_id){
                var payload = { 
                    id          : id,
                    model       : 'PictureStep',
                    operation   : 'update',
                    template    : 'picture_step',
                    foreign_key : step_id,
                };
                Scenia.Modal.Template(payload,1);
            },
            Insert : function(step_id){
                var payload = { 
                    model       : 'PictureStep',
                    operation   : 'insert',
                    template    : 'picture_step',
                    foreign_key : step_id,
                };
                Scenia.Modal.Template(payload,1);
            },
        }
    },
    
    Material : {
        Summon : {
            Update : function(id){
                var payload = { 
                    id          : id,
                    model       : 'Material',
                    operation   : 'update',
                    template    : 'material',
                };
                Scenia.Modal.Template(payload,2);
            },
            Insert : function(){
                var payload = { 
                    model       : 'Material',
                    operation   : 'insert',
                    template    : 'material',
                };
                Scenia.Modal.Template(payload,2);
            },
        },
    },

    MaterialStep : {
        Summon : {
            Update : function(id,step_id){
                var payload = { 
                    id          : id,
                    model       : 'MaterialStep',
                    operation   : 'update',
                    template    : 'material_step',
                    foreign_key : step_id,
                };
                Scenia.Modal.Template(payload,1);
            },
            Insert : function(step_id){
                var payload = { 
                    model       : 'MaterialStep',
                    operation   : 'insert',
                    template    : 'material_step',
                    foreign_key : step_id,
                };
                Scenia.Modal.Template(payload,1);
            },
        }
    },
    
    Gear : {
        Summon : {
            Update : function(id){
                var payload = { 
                    id          : id,
                    model       : 'Gear',
                    operation   : 'update',
                    template    : 'gear',
                };
                Scenia.Modal.Template(payload,2);
            },
            Insert : function(){
                var payload = { 
                    model       : 'Gear',
                    operation   : 'insert',
                    template    : 'gear',
                };
                Scenia.Modal.Template(payload,2);
            },
        },
    },
    
    GearStep : {
        Summon : {
            Update : function(id, step_id){
                var payload = { 
                    id          : id,
                    model       : 'GearStep',
                    operation   : 'update',
                    template    : 'gear_step',
                    foreign_key : step_id,  
                };
                Scenia.Modal.Template(payload,1);
            },
            Insert : function(step_id){
                var payload = { 
                    model       : 'GearStep',
                    operation   : 'insert',
                    template    : 'gear_step',
                    foreign_key : step_id,
                };
                Scenia.Modal.Template(payload,1);
            },
        }
    },

    Step : {
        Summon : {
            Update : function(id, project_id){
                var payload = { 
                    id          : id,
                    model       : 'Step',
                    operation   : 'update',
                    template    : 'step',
                    foreign_key : project_id,
                };
                Scenia.Modal.Template(payload);
            },
            Insert : function(project_id){
                var payload = { 
                    model       : 'Step',
                    operation   : 'insert',
                    template    : 'step',
                    foreign_key : project_id,
                };
                Scenia.Modal.Template(payload);
            },
        },
    },
};