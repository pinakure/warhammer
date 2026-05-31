const False = false;
const True  = true;
const None  = null;

function error_dialog(error, path, traceback){
    return `
    <div class="outset gray border-gray plate">
        <div class="errorcaption"><div class="errorcaptionicon"></div>Error</div>
        <div class="errormessage"><pre> ${ error } <br/><br/>${path} </pre></div>
        <div class="erroricon"></div>
        <div class="inset gray border-gray plate traceback">
            <textarea class="traceback-content fullwidth fullweight">${traceback}</textarea>
        </div>
        <div class="blackborder"><button onclick="modal_errors.dispose()" class="errorbutton">Close<div class="dashborder"></div></button></div>
    </div>
    `;    
}

function error_modal(data){
    try {
        data = data.responseText;
        parts = data.split('\n\n');
        error = parts.shift().trim();
        path  = parts.shift().split('Django')[0].trim();
        traceback = data.split('Traceback:\n')[1].trim();
    } catch(e){
        error = "Error";
        path  = "A error ocurred. See below.";
        traceback = data?data.responseText?data.responseText:data:e;
    }
    data = error_dialog(error, path, traceback);
    $('.loading').hide();
    $('.modal_dialog_content[id="errors"]').html(data); 
    $('.modal_dialog_content[id="errors"]').css('display', 'inline-block');
}

function default_callback(data){ 
    error_modal(data);    
}

var Scenia = {
    root            : '{{ root }}/scenia/',

    auth            : function() {
        return 0x0cabeca0;
    },

    post            : function(endpoint, data={}, callback=default_callback, error_handler=default_callback){
        $.post(`${ Scenia.root }${ endpoint }`, data).done(callback).fail(error_handler);
    },
    
    get             : function(endpoint, data={}, callback=default_callback, error_handler=default_callback){
        $.get(`${ Scenia.root }${ endpoint }`, data).done(callback).fail(error_handler);
    },

    Trigger : Trigger,
    Modal   : Modal,
    
    Latest : function(quantity){
        /* TODO: call Scenia api instead */
        array = [];
        $('.curtain').show();        
        $.post(`${Scenia.root}getql/`,
            { 'query': `{ latest }`}
        ).done(function(data){
            $('.curtain').hide();
            $('#articles').html('')
            try{
                latest = eval(data.response.latest);
                for(l_i in latest){
                    l = latest[l_i];
                    p = new Project(l.id, l.name, l.author, l.description, l.creation_time, l.subtaxonomy, l.picture);
                    $('#articles').append(p.widget());
                }
            } catch(e){
                error_modal(data.response.latest.error);
            }        
        });    
    },

    Taxonomy : {
        All : function(){
            Scenia.get(
                'api/', {
                    query : 'taxonomies'
                },
                function(data){
                    var taxonomies = data.response;
                    for(taxonomy_index in taxonomies){
                        taxonomy = taxonomies[taxonomy_index];
                        var html = `<option value="${ taxonomy.id }" title="${ taxonomy.description }">${ taxonomy.name }</option>`;
                        $('#taxonomy').append(html);
                    }
                }
            );
        },
        Load : function(id){
            Scenia.get(
                'api/',{ 
                    query   : 'subtaxonomies',
                    id      : id,
                },
                function(data){
                    obj = data.response;
                    if(obj.length > 0){
                        $('#subtaxonomy').html("");
                        for(obj_index in obj){
                            taxonomy = obj[obj_index];
                            node = `<option value="${taxonomy['id']}" title="${taxonomy['description']}">${taxonomy['name']}</option>`;            
                            $('#subtaxonomy').append(node);
                        }
                    }
                }
            );
        },
    },
};

