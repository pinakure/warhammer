function Project(id=-1, name="", author="", brief="", create_time=0, subtaxonomy=0, picture=false){
    this.id = id;
    this.name = name;
    this.author = author;   
    this.description = brief;
    this.create_time = create_time;
    this.subtaxonomy = subtaxonomy;
    this.picture = picture;
}

Project.prototype.widget = function(){
    console.log("DEPRECATED: This should be done from backend");
    return ``
}

Project.prototype.render = function(){ this.loadSteps('postLoadSteps(self)');
    console.log("DEPRECATED: This should be done from backend");
    return ``;
}

// REMOVE
Project.prototype.loadSteps = function(callback=';'){ eval(callback);    }
function postLoadSteps(project){}

function loadTaxonomy(){
    taxonomy = $('#taxonomy').val();
    api.loadTaxonomy(taxonomy);
}

function triggerCreateProject(){
    api.createProject($('#name').val(), $('#description').val(),$('#taxonomy').val(),$('#subtaxonomy').val());
}
function triggerEditProject(id){
    api.editProject(id, $('#name').val(), $('#description').val());
}

Project.prototype.summonCreateDialog = function(){
    head = `<button id="modal_caption" class="btn">Create Project</button>`;
    body = `
        <table style="height: calc(100% - 32px);border: 8px solid transparent; width:100%">
            ${ renderFormRow("Name","name", "text", '') }
            ${ renderFormRow("Description", "description", "text", ``) }
            ${ renderFormRowSelect("Category", "taxonomy", `<option value="" title="Select one.">--</option>`, "loadTaxonomy()") }
            ${ renderFormRowSelect("Subcategory", "subtaxonomy", `<option value="" title="Select category first.">--</option>`) }
            ${ renderFormRowButton("Create project", "submit", "triggerCreateProject()") }
        </table>
    `;
    modal_dialog.setBody(head+body);
    api.loadTaxonomies();
}

Project.prototype.load = function(id, callback=";"){
    this.id = id;
    self = this;
    $.post(`${api.root}getql/`,
    { 'query' : `{ project(id:${id}) }`}).done(function(graphql){
        project = graphql.response.project;
        self.name        = project.name;
        self.author      = project.author;
        self.brief       = project.brief;
        self.create_time = project.create_time;
        self.picture     = project.picture;
        self.subtaxonomy = project.subtaxonomy;
        self.steps       = []; // LAZY member: call loadSteps to load these
        eval(callback);
    });
}
