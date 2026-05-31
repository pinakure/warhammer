function readSelect2(id){
    var ret = [];
    var data = $(`select#${id}`).select2('data');
    for(i in data){
        var row = data[i];
        ret[ret.length] = row.id;
    }
    return ret;
}

var Trigger = {
    Upload : function(callback){
        formData = new FormData(document.getElementById("fileform"));
        $.ajax({
            url: `${Scenia.root}upload/`,
            type: 'POST',
            data: formData,
            contentType: false,
            cache:false,
            processData: false,
            success: function (data, status){
                callback(data.response)
                return false;
            },error: function (xhr, desc, err){
                error_modal(xhr);
                return false;
            }
        });
    },

    Step : {
        Insert : function(project_id){
            Scenia.post('api/',{
                insert      : 'step',
                project     : $('#project').val(),
                order       : '-1',
                time        : $('#time_required').val(),
                description : $('#brief').val(),
            },function(data){
                console.log("CREATE STEP RESPONSE: "+data)
                id = parseInt(data.response);
                if(id > 0){
                    project = $('#project').val();
                    modal_dialog.dispose();
                    modal_subdialog.dispose();                        
                    // return Scenia.Latest();
                    window.location = `${Scenia.root}?project=${project}`;
                    return;
                }
                error_modal(data.error);
                return false;
            });
        },

        Update : function(id){
            Scenia.post('api/',{
                update      : 'step',
                id          : id,
                project     : $('#project').val(),
                // order       : '-1',
                time        : $('#time_required').val(),
                description : $('#brief').val(),                    
                materials   : JSON.stringify(readSelect2('materials')),
                gears       : JSON.stringify(readSelect2('gears')),
                colors      : JSON.stringify(readSelect2('colors')),
            },function(data){
                console.log("UPDATE STEP RESPONSE: "+data)
                id = parseInt(data.response);
                if(id > 0){
                    project = $('#project').val();
                    modal_dialog.dispose();
                    modal_subdialog.dispose();                        
                    // return Scenia.Latest();
                    window.location = `${Scenia.root}?project=${project}`;
                    return;
                }
                error_modal(data.error);
                return false;
            });
        },

        Delete : function(id){
            if(confirm("¿ Are your sure ? This action cannot be undone.")){
                Scenia.post('api/',{
                    delete      : 'step',
                    id          : id,                        
                },function(data){
                    modal_dialog.dispose();
                    modal_subdialog.dispose();
                    window.location = `${Scenia.root}?project=${$('#project').val()}`;
                });
            }
        },            
    },

    Project : {

        Insert : function(){
            Scenia.post('api/',{
                insert      : 'project',
                name        : $('#name').val(),
                description : $('#description').val(),
                subtaxonomy : $('#subtaxonomy option:selected').val(),
            },function(data){
                console.log("CREATE RESPONSE: "+data)
                id = parseInt(data.response);
                if(id > 0){
                    modal_dialog.dispose();
                    modal_subdialog.dispose();                        
                    location.reload();
                    return true;
                }
                error_modal(data.error);
                return false;
            });                
        },

        Update : function(id){
            Scenia.post('api/',{
                update      : 'project',
                id          : id,
                name        : $('#name').val(),
                description : $('#description').val(),                    
            },function(data){
                modal_dialog.dispose();
                modal_subdialog.dispose();                        
                window.location = `${Scenia.root}?project=${id}`;
            });                
        },

        Delete : function(id){
            if(confirm("¿ Are your sure ? This action cannot be undone.")){
                Scenia.post('api/',{
                    delete      : 'project',
                    id          : id,                        
                },function(data){
                    modal_dialog.dispose();
                    modal_subdialog.dispose();
                    window.location = `${Scenia.root}`;
                });
            }
        },
    },

    Material : {
        Insert : function(filename=null){
            var name        = $('#name').val();
            var description = $('#description').val();
            var filename    = filename || $('#picture').val();
            var buy_link    = $('#buy_link').val();
            var price       = $('#price').val();
            if(
                (name == '') ||
                (description == '')                
            ){
                alert("Please fill all required fields");
                return;
            }
            Scenia.post('api/',{
                insert      : 'material',
                name        : name,
                description : description,
                filename    : filename,
                buy_link    : buy_link,
                price       : price == '' ? 0 : parseFloat(price),
            },function(data){
                console.log(`INSERT MATERIAL RESPONSE:`, data);
                id = parseInt(data.response);
                if(id > 0){
                    modal_confirm.dispose();
                    return ;
                }
                error_modal(data.error);
                return false;
            });                
        },

        Upload : function(){
            Trigger.Upload(Scenia.Trigger.Material.Insert);
        },

        Update : function(id){
            Scenia.post('api/',{
                update      : 'material',
                id          : id,
                /*
                name        : $('#name').val(),
                description : $('#description').val(),                    
                */
            },function(data){
                modal_confirm.dispose();
                //window.location = `${Scenia.root}?project=${id}`;
            });                
        },

        Delete : function(id){
            console.log(`TBI: Call to Scenia.Trigger.Material.Delete(${id})`);
        },
    },

    Picture : {
        Insert : function(filename=null){
            var name        = $('#name').val();
            var description = $('#description').val();
            var filename    = filename || $('#picture').val();
            var buy_link    = $('#buy_link').val();
            var price       = $('#price').val();
            if(
                (name == '') ||
                (description == '')                
            ){
                alert("Please fill all required fields");
                return;
            }
            Scenia.post('api/',{
                insert      : 'picture',
                filename    : filename,
                description : description,
                step        : $('#step_id').val(),
            },function(data){
                console.log(`INSERT PICTURE RESPONSE:`, data);
                id = parseInt(data.response);
                if(id > 0){
                    modal_confirm.dispose();
                    return ;
                }
                error_modal(data.error);
                return false;
            });                
        },

        Upload : function(){
            Trigger.Upload(Scenia.Trigger.Picture.Insert);
        },

        Update : function(id){
            Scenia.post('api/',{
                update      : 'picture',
                id          : id,
                description : description,
            },function(data){
                modal_confirm.dispose();
            });                
        },

        Delete : function(id){
            error_modal(`TBI: Call to Scenia.Trigger.Picture.Delete(${id})`);
        },
    },

    Gear : {
        Insert : function(filename=null){
            var name        = $('#name').val();
            var description = $('#description').val();
            var filename    = filename || $('#picture').val();
            var buy_link    = $('#buy_link').val();
            var price       = $('#price').val();
            if(
                (name == '') ||
                (description == '')                
            ){
                alert("Please fill all required fields");
                return;
            }
            Scenia.post('api/',{
                insert      : 'gear',
                name        : name,
                description : description,
                filename    : filename,
                buy_link    : buy_link,
                price       : price == '' ? 0 : parseFloat(price),
            },function(data){
                console.log(`INSERT GEAR RESPONSE:`, data);
                id = parseInt(data.response);
                if(id > 0){
                    modal_confirm.dispose();
                    return ;
                }
                error_modal(data.error);
                return false;
            });                
        },

        Upload : function(callback){
            Trigger.Upload(Scenia.Trigger.Gear.Insert);
        },

        Update : function(id){
            Scenia.post('api/',{
                update      : 'gear',
                id          : id,
                /*
                name        : $('#name').val(),
                description : $('#description').val(),                    
                */
            },function(data){
                modal_confirm.dispose();
                //window.location = `${Scenia.root}?project=${id}`;
            });                
        },

        Delete : function(id){
            error_modal(`TBI: Call to Scenia.Trigger.Gear.Delete(${id})`);
        },
    },
};
