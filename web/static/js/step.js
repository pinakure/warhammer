function Step(id=-1, materials = [], gear=[], pictures=[], brief="", update_time="", order=0, time_required=1){
    this.id = id;
    this.materials = materials;
    this.gear = gear;
    this.brief = brief;
    this.pictures = pictures;
    this.order = order;
    this.update_time = update_time;
    this.time_required = time_required;
}

function triggerCreateStep(project){
    api.createStep(project, $('#brief').val(), $('#time_required').val());
}


Step.prototype.summonCreateDialog = function(project){
    head = `<button id="modal_caption" class="btn">Create Step</button>`;
    body = `
        <table style="height: calc(100% - 32px);border: 8px solid transparent; width:100%">
            ${ renderFormRow("Hint","brief", "text", this.brief) }
            ${ renderFormRow("Minutes","time_required", "datetime", this.time_required) }
            ${ renderFormRowButton("Create project step", "submit", `triggerCreateStep(${ project })` ) }
        </table>
    `;
    modal_dialog.setBody(head+body);
}

Step.prototype.load = function(id, callback=";"){
    this.id = id;
    self = this;
    $.post(`${api.root}get/`,
    { 'query' : `{ step(id:${id}) }`}).done(function(data){
        step = data.response.step;
        self.brief = step.brief;
        self.update_time = step.update_time;
        self.materials = step.materials;
        self.gear =  step.gear;
        self.pictures = step.pictures;
        self.time_required = step.time_required;
        self.order = step.order;
        eval(callback);
    });
}
