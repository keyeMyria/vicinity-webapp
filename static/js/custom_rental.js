var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var ws_path = ws_scheme + '://' + window.location.host + "/chat/stream/";
var ws_notif = ws_scheme + '://' + window.location.host + "/notify/";
var ws_message = ws_scheme + '://' + window.location.host + "/message/";


if (window.location.href.search(/login/gi) < 0) {
	if (sessionStorage.getItem('userID') == 'true'){	
	socket_notif = new ReconnectingWebSocket(ws_notif);
	socket_message = new ReconnectingWebSocket(ws_message);

	socket_chat = new ReconnectingWebSocket(ws_path);
	socketsend(socket_chat);

	}

}


$( document ).ready(function() {
	if (sessionStorage.getItem('userID') == 'true'){
	notificationalert();
	 messagealert();
	}
	
	
	$('button.close_chat').on('click',function(){

		$('.msg_container').html('')
		$('.msg_container').removeAttr('id')
		$('.messagechat').val('')
		$('.send-message').unbind()
		$('.small-chat-box').toggleClass('active');
	})
	
	$('.sort-by-filter').on('change',function(){
		var self = $(this);
		$('#sorttype').val(self.val());
		$('.submit-form').click();
	}) 
	$('#payment0').on('click', function(){
		$('#payment1').prop('checked',false)
		$(this).prop('checked',true)
	})
	$('#payment1').on('click', function(){
		$('#payment0').prop('checked',false)
		$(this).prop('checked',true)
	})
	$('.btn-sort').on('click',function(){
		var self = $(this);
		$('#sorttype').val(self.attr('data-value'));
		self.parent().find('.btn-sort').each(function(){
			$(this).removeClass('active');
		})
		self.addClass('active');
	}) 
	$('#agreecheckbox').click(function(){
		$('.agreecheckbox').removeClass('fa-square-o').addClass('fa-check-square-o')
		
		$('.submit_date').attr('type','submit')		
	})

	  $(".js-upload-photos").click(function () {
    $("#fileupload").click();
  });
	$('[data-toggle="popover"]').popover();
	
	var defaultDiacriticsRemovalMap = [
        {'base':'A', 'letters':/[\u0041\u24B6\uFF21\u00C0\u00C1\u00C2\u1EA6\u1EA4\u1EAA\u1EA8\u00C3\u0100\u0102\u1EB0\u1EAE\u1EB4\u1EB2\u0226\u01E0\u00C4\u01DE\u1EA2\u00C5\u01FA\u01CD\u0200\u0202\u1EA0\u1EAC\u1EB6\u1E00\u0104\u023A\u2C6F]/g},
        {'base':'AA','letters':/[\uA732]/g},
        {'base':'AE','letters':/[\u00C6\u01FC\u01E2]/g},
        {'base':'AO','letters':/[\uA734]/g},
        {'base':'AU','letters':/[\uA736]/g},
        {'base':'AV','letters':/[\uA738\uA73A]/g},
        {'base':'AY','letters':/[\uA73C]/g},
        {'base':'B', 'letters':/[\u0042\u24B7\uFF22\u1E02\u1E04\u1E06\u0243\u0182\u0181]/g},
        {'base':'C', 'letters':/[\u0043\u24B8\uFF23\u0106\u0108\u010A\u010C\u00C7\u1E08\u0187\u023B\uA73E]/g},
        {'base':'D', 'letters':/[\u0044\u24B9\uFF24\u1E0A\u010E\u1E0C\u1E10\u1E12\u1E0E\u0110\u018B\u018A\u0189\uA779]/g},
        {'base':'DZ','letters':/[\u01F1\u01C4]/g},
        {'base':'Dz','letters':/[\u01F2\u01C5]/g},
        {'base':'E', 'letters':/[\u0045\u24BA\uFF25\u00C8\u00C9\u00CA\u1EC0\u1EBE\u1EC4\u1EC2\u1EBC\u0112\u1E14\u1E16\u0114\u0116\u00CB\u1EBA\u011A\u0204\u0206\u1EB8\u1EC6\u0228\u1E1C\u0118\u1E18\u1E1A\u0190\u018E]/g},
        {'base':'F', 'letters':/[\u0046\u24BB\uFF26\u1E1E\u0191\uA77B]/g},
        {'base':'G', 'letters':/[\u0047\u24BC\uFF27\u01F4\u011C\u1E20\u011E\u0120\u01E6\u0122\u01E4\u0193\uA7A0\uA77D\uA77E]/g},
        {'base':'H', 'letters':/[\u0048\u24BD\uFF28\u0124\u1E22\u1E26\u021E\u1E24\u1E28\u1E2A\u0126\u2C67\u2C75\uA78D]/g},
        {'base':'I', 'letters':/[\u0049\u24BE\uFF29\u00CC\u00CD\u00CE\u0128\u012A\u012C\u0130\u00CF\u1E2E\u1EC8\u01CF\u0208\u020A\u1ECA\u012E\u1E2C\u0197]/g},
        {'base':'J', 'letters':/[\u004A\u24BF\uFF2A\u0134\u0248]/g},
        {'base':'K', 'letters':/[\u004B\u24C0\uFF2B\u1E30\u01E8\u1E32\u0136\u1E34\u0198\u2C69\uA740\uA742\uA744\uA7A2]/g},
        {'base':'L', 'letters':/[\u004C\u24C1\uFF2C\u013F\u0139\u013D\u1E36\u1E38\u013B\u1E3C\u1E3A\u0141\u023D\u2C62\u2C60\uA748\uA746\uA780]/g},
        {'base':'LJ','letters':/[\u01C7]/g},
        {'base':'Lj','letters':/[\u01C8]/g},
        {'base':'M', 'letters':/[\u004D\u24C2\uFF2D\u1E3E\u1E40\u1E42\u2C6E\u019C]/g},
        {'base':'N', 'letters':/[\u004E\u24C3\uFF2E\u01F8\u0143\u00D1\u1E44\u0147\u1E46\u0145\u1E4A\u1E48\u0220\u019D\uA790\uA7A4]/g},
        {'base':'NJ','letters':/[\u01CA]/g},
        {'base':'Nj','letters':/[\u01CB]/g},
        {'base':'O', 'letters':/[\u004F\u24C4\uFF2F\u00D2\u00D3\u00D4\u1ED2\u1ED0\u1ED6\u1ED4\u00D5\u1E4C\u022C\u1E4E\u014C\u1E50\u1E52\u014E\u022E\u0230\u00D6\u022A\u1ECE\u0150\u01D1\u020C\u020E\u01A0\u1EDC\u1EDA\u1EE0\u1EDE\u1EE2\u1ECC\u1ED8\u01EA\u01EC\u00D8\u01FE\u0186\u019F\uA74A\uA74C]/g},
        {'base':'OI','letters':/[\u01A2]/g},
        {'base':'OO','letters':/[\uA74E]/g},
        {'base':'OU','letters':/[\u0222]/g},
        {'base':'P', 'letters':/[\u0050\u24C5\uFF30\u1E54\u1E56\u01A4\u2C63\uA750\uA752\uA754]/g},
        {'base':'Q', 'letters':/[\u0051\u24C6\uFF31\uA756\uA758\u024A]/g},
        {'base':'R', 'letters':/[\u0052\u24C7\uFF32\u0154\u1E58\u0158\u0210\u0212\u1E5A\u1E5C\u0156\u1E5E\u024C\u2C64\uA75A\uA7A6\uA782]/g},
        {'base':'S', 'letters':/[\u0053\u24C8\uFF33\u1E9E\u015A\u1E64\u015C\u1E60\u0160\u1E66\u1E62\u1E68\u0218\u015E\u2C7E\uA7A8\uA784]/g},
        {'base':'T', 'letters':/[\u0054\u24C9\uFF34\u1E6A\u0164\u1E6C\u021A\u0162\u1E70\u1E6E\u0166\u01AC\u01AE\u023E\uA786]/g},
        {'base':'TZ','letters':/[\uA728]/g},
        {'base':'U', 'letters':/[\u0055\u24CA\uFF35\u00D9\u00DA\u00DB\u0168\u1E78\u016A\u1E7A\u016C\u00DC\u01DB\u01D7\u01D5\u01D9\u1EE6\u016E\u0170\u01D3\u0214\u0216\u01AF\u1EEA\u1EE8\u1EEE\u1EEC\u1EF0\u1EE4\u1E72\u0172\u1E76\u1E74\u0244]/g},
        {'base':'V', 'letters':/[\u0056\u24CB\uFF36\u1E7C\u1E7E\u01B2\uA75E\u0245]/g},
        {'base':'VY','letters':/[\uA760]/g},
        {'base':'W', 'letters':/[\u0057\u24CC\uFF37\u1E80\u1E82\u0174\u1E86\u1E84\u1E88\u2C72]/g},
        {'base':'X', 'letters':/[\u0058\u24CD\uFF38\u1E8A\u1E8C]/g},
        {'base':'Y', 'letters':/[\u0059\u24CE\uFF39\u1EF2\u00DD\u0176\u1EF8\u0232\u1E8E\u0178\u1EF6\u1EF4\u01B3\u024E\u1EFE]/g},
        {'base':'Z', 'letters':/[\u005A\u24CF\uFF3A\u0179\u1E90\u017B\u017D\u1E92\u1E94\u01B5\u0224\u2C7F\u2C6B\uA762]/g},
        {'base':'a', 'letters':/[\u0061\u24D0\uFF41\u1E9A\u00E0\u00E1\u00E2\u1EA7\u1EA5\u1EAB\u1EA9\u00E3\u0101\u0103\u1EB1\u1EAF\u1EB5\u1EB3\u0227\u01E1\u00E4\u01DF\u1EA3\u00E5\u01FB\u01CE\u0201\u0203\u1EA1\u1EAD\u1EB7\u1E01\u0105\u2C65\u0250]/g},
        {'base':'aa','letters':/[\uA733]/g},
        {'base':'ae','letters':/[\u00E6\u01FD\u01E3]/g},
        {'base':'ao','letters':/[\uA735]/g},
        {'base':'au','letters':/[\uA737]/g},
        {'base':'av','letters':/[\uA739\uA73B]/g},
        {'base':'ay','letters':/[\uA73D]/g},
        {'base':'b', 'letters':/[\u0062\u24D1\uFF42\u1E03\u1E05\u1E07\u0180\u0183\u0253]/g},
        {'base':'c', 'letters':/[\u0063\u24D2\uFF43\u0107\u0109\u010B\u010D\u00E7\u1E09\u0188\u023C\uA73F\u2184]/g},
        {'base':'d', 'letters':/[\u0064\u24D3\uFF44\u1E0B\u010F\u1E0D\u1E11\u1E13\u1E0F\u0111\u018C\u0256\u0257\uA77A]/g},
        {'base':'dz','letters':/[\u01F3\u01C6]/g},
        {'base':'e', 'letters':/[\u0065\u24D4\uFF45\u00E8\u00E9\u00EA\u1EC1\u1EBF\u1EC5\u1EC3\u1EBD\u0113\u1E15\u1E17\u0115\u0117\u00EB\u1EBB\u011B\u0205\u0207\u1EB9\u1EC7\u0229\u1E1D\u0119\u1E19\u1E1B\u0247\u025B\u01DD]/g},
        {'base':'f', 'letters':/[\u0066\u24D5\uFF46\u1E1F\u0192\uA77C]/g},
        {'base':'g', 'letters':/[\u0067\u24D6\uFF47\u01F5\u011D\u1E21\u011F\u0121\u01E7\u0123\u01E5\u0260\uA7A1\u1D79\uA77F]/g},
        {'base':'h', 'letters':/[\u0068\u24D7\uFF48\u0125\u1E23\u1E27\u021F\u1E25\u1E29\u1E2B\u1E96\u0127\u2C68\u2C76\u0265]/g},
        {'base':'hv','letters':/[\u0195]/g},
        {'base':'i', 'letters':/[\u0069\u24D8\uFF49\u00EC\u00ED\u00EE\u0129\u012B\u012D\u00EF\u1E2F\u1EC9\u01D0\u0209\u020B\u1ECB\u012F\u1E2D\u0268\u0131]/g},
        {'base':'j', 'letters':/[\u006A\u24D9\uFF4A\u0135\u01F0\u0249]/g},
        {'base':'k', 'letters':/[\u006B\u24DA\uFF4B\u1E31\u01E9\u1E33\u0137\u1E35\u0199\u2C6A\uA741\uA743\uA745\uA7A3]/g},
        {'base':'l', 'letters':/[\u006C\u24DB\uFF4C\u0140\u013A\u013E\u1E37\u1E39\u013C\u1E3D\u1E3B\u017F\u0142\u019A\u026B\u2C61\uA749\uA781\uA747]/g},
        {'base':'lj','letters':/[\u01C9]/g},
        {'base':'m', 'letters':/[\u006D\u24DC\uFF4D\u1E3F\u1E41\u1E43\u0271\u026F]/g},
        {'base':'n', 'letters':/[\u006E\u24DD\uFF4E\u01F9\u0144\u00F1\u1E45\u0148\u1E47\u0146\u1E4B\u1E49\u019E\u0272\u0149\uA791\uA7A5]/g},
        {'base':'nj','letters':/[\u01CC]/g},
        {'base':'o', 'letters':/[\u006F\u24DE\uFF4F\u00F2\u00F3\u00F4\u1ED3\u1ED1\u1ED7\u1ED5\u00F5\u1E4D\u022D\u1E4F\u014D\u1E51\u1E53\u014F\u022F\u0231\u00F6\u022B\u1ECF\u0151\u01D2\u020D\u020F\u01A1\u1EDD\u1EDB\u1EE1\u1EDF\u1EE3\u1ECD\u1ED9\u01EB\u01ED\u00F8\u01FF\u0254\uA74B\uA74D\u0275]/g},
        {'base':'oi','letters':/[\u01A3]/g},
        {'base':'ou','letters':/[\u0223]/g},
        {'base':'oo','letters':/[\uA74F]/g},
        {'base':'p','letters':/[\u0070\u24DF\uFF50\u1E55\u1E57\u01A5\u1D7D\uA751\uA753\uA755]/g},
        {'base':'q','letters':/[\u0071\u24E0\uFF51\u024B\uA757\uA759]/g},
        {'base':'r','letters':/[\u0072\u24E1\uFF52\u0155\u1E59\u0159\u0211\u0213\u1E5B\u1E5D\u0157\u1E5F\u024D\u027D\uA75B\uA7A7\uA783]/g},
        {'base':'s','letters':/[\u0073\u24E2\uFF53\u00DF\u015B\u1E65\u015D\u1E61\u0161\u1E67\u1E63\u1E69\u0219\u015F\u023F\uA7A9\uA785\u1E9B]/g},
        {'base':'t','letters':/[\u0074\u24E3\uFF54\u1E6B\u1E97\u0165\u1E6D\u021B\u0163\u1E71\u1E6F\u0167\u01AD\u0288\u2C66\uA787]/g},
        {'base':'tz','letters':/[\uA729]/g},
        {'base':'u','letters':/[\u0075\u24E4\uFF55\u00F9\u00FA\u00FB\u0169\u1E79\u016B\u1E7B\u016D\u00FC\u01DC\u01D8\u01D6\u01DA\u1EE7\u016F\u0171\u01D4\u0215\u0217\u01B0\u1EEB\u1EE9\u1EEF\u1EED\u1EF1\u1EE5\u1E73\u0173\u1E77\u1E75\u0289]/g},
        {'base':'v','letters':/[\u0076\u24E5\uFF56\u1E7D\u1E7F\u028B\uA75F\u028C]/g},
        {'base':'vy','letters':/[\uA761]/g},
        {'base':'w','letters':/[\u0077\u24E6\uFF57\u1E81\u1E83\u0175\u1E87\u1E85\u1E98\u1E89\u2C73]/g},
        {'base':'x','letters':/[\u0078\u24E7\uFF58\u1E8B\u1E8D]/g},
        {'base':'y','letters':/[\u0079\u24E8\uFF59\u1EF3\u00FD\u0177\u1EF9\u0233\u1E8F\u00FF\u1EF7\u1E99\u1EF5\u01B4\u024F\u1EFF]/g},
        {'base':'z','letters':/[\u007A\u24E9\uFF5A\u017A\u1E91\u017C\u017E\u1E93\u1E95\u01B6\u0225\u0240\u2C6C\uA763]/g}
        ];
        var changes;
        function removeDiacritics (str) {
            if(!changes) {
                changes = defaultDiacriticsRemovalMap;
            }
            for(var i=0; i<changes.length; i++) {
                str = str.replace(changes[i].letters, changes[i].base);
            }
            return str;
        }
        jQuery.fn.nl2br = function() {
            return this.each(function() {
                var that = jQuery(this);
                that.hide();
                var div = $('<div/>')
                .attr('contenteditable', true);
                div.attr('data-placeholder', that.attr('placeholder'))
                div.attr('name', that.attr('name') + '_data')
                div.attr('required', true)
                div.html(that.val());
                div.addClass("form-control textarea")
                div.on('paste',function(e) {
                    e.preventDefault();
                    var text = (e.originalEvent || e).clipboardData.getData('text/plain');
                    var testinput = text.replace(/  /g, ' ').replace(/\\r\\n|\\n/g, '\n').replace(/<br[^>]*>/gi,'\n').replace(/‘/g,"'").replace(/’/g,"'").replace(/“/g,'"').replace(/”/g,'"').replace(/\u2013|\u2014/g, "-").replace(/&nbsp;/g, ' ');
                    window.document.execCommand('insertText', false, testinput);  
                    var self = $(this);
                    var data2 = self.html().replace(/<div><br><\/div>/g,'<br>').replace(/<div>/g,'<br>').replace(/<\/div>/g,'').replace(/\\r\\n|\\n/g, '<br>').replace(/\u2013|\u2014/g, "-").replace(/&nbsp;/g, ' ').replace(/<br[^>]*>/gi,'<br>');
                    var replacetext2 = data2.replace(/‘/g,"'").replace(/’/g,"'").replace(/“/g,'"').replace(/”/g,'"')
                    var replacedd = removeDiacritics(replacetext2);
                    div.next('textarea').html(replacedd);
                });
                div.on('input', function() {
                    var self = $(this);
                    var data = self.html().replace(/<div><br><\/div>/g,'<br>').replace(/<div>/g,'<br>').replace(/\\r\\n|\\n/g, '<br>').replace(/<\/div>/g,'').replace(/\u2013|\u2014/g, "-").replace(/&nbsp;/g, ' ').replace(/<br[^>]*>/gi,'<br>');
                    div.next('textarea').html(data);
                    div.next('textarea').html(removeDiacritics(div.next('textarea').val()));
                    div.next('textarea').html(div.next('textarea').val().replace(/‘/g,"'").replace(/’/g,"'").replace(/“/g,'"').replace(/”/g,'"'));                    

                    if($(this).val().length > 1){
                    	that.attr('required', false)
                    }
                    else{
                    	that.attr('required', true)
                    }
                });
                div.insertBefore(that);
            });
        };


       

	  var filesInput = document.getElementById("fileupload");
	if (filesInput != null){
        
        filesInput.addEventListener("change", function(event){
        	
        	$(".uploading-content").removeClass('hidden');
      	  var progress = parseInt($(this).length * 100, 10);
            var strProgress = progress + "%";
            $(".progress-bar").css({"width": strProgress});
            $(".progress-bar").text(strProgress);

            $(".uploading-content").addClass('hidden');
            
            var files = event.target.files; 
            var output = document.getElementById("gallery");
            
            
            for(var i = 0; i< files.length; i++)
            {
                var file = files[i];
                
                if(!file.type.match('image'))
                  continue;
                
                var picReader = new FileReader();
                
                picReader.addEventListener("load",function(event){
                    
                    var picFile = event.target;
                    
                    var div = document.createElement("td");
                    div.className = "gallery";
                    
                    div.innerHTML = "<img class='img-thumbnail'  src='" + picFile.result + "'" +
                            "title='" + picFile.name + "'/>";
                    
                    output.insertBefore(div,null);            
                
                });
                $('.photos-box').removeClass('hidden');
                
                picReader.readAsDataURL(file);
            }                               
           
        });
	}
        $('.remove-pic').on('click', function(){
      	var self = $(this)      	 
          	 self.closest('.gallery').remove();          	 
             
      })
   
  $.validator.setDefaults({

    highlight: function(element) {
        $(element).closest('.form-group').addClass('has-error');
    },
    unhighlight: function(element) {
        $(element).closest('.form-group').removeClass('has-error');
    },
    errorElement: 'span',
    errorClass: 'help-block',
    errorPlacement: function(error, element) 
    {
    	error['prevObject'][0]['innerHTML'] = element[0]['attributes']['placeholder'].value + ' is required.'
        if (element.parent('.input-group').length) {
            error.insertAfter(element.parent());
        } else {
            error.insertAfter(element);
        }
    }
});


        $('form').each(function(){$(this).validate({ignore: [],
        	wrapper: 'span',
      	  rules: {
      		username:{
	            required: true},
      		  email: {
	            required: true
  	        },
      		    password: {
      	            required: true,
      	            minlength: 8
      	        },
      		    password_confirm: {
      		      equalTo: "#id_password",
      		            required: true,
      		            minlength: 8
      		    },
      		    password_confirm_business: {
        		      equalTo: "#id_password_business",
        		            required: true,
        		            minlength: 8
        		    },
      		    new_password1: {
      	            required: true,
      	            minlength: 8
      	        },
      	        new_password2: {
      		      equalTo: "#id_new_password1",
      		            required: true,
      		            minlength: 8
      		    },
      		    contact_no: {
      	            required: true,
      	            digits: true,
      	            minlength: 5,
      	            maxlength: 15
      	        },
      	      message_request_data: {
      	        required: true
      	      },
      	    attendnumber:{
  	            digits: true,
      	    	
      	    }
      	        
      		  },  messages: {
      		    email: {
      		      required: "Email address is required."
      		    },first_name: {
      		      required: "First name is required."
      		    },last_name: {
      		      required: "Last name is required."
      		    },password: {
      		      required: "Password is required."
      		    },password_confirm: {
      		      required: "Password (again) is required."
      		    },contact_no: {
      		      required: "Contact no is required."
      		    },
      		CompanyName:{
      			required: "Name is required."
      		  },
      		CompanyEmail:{
          			required: "Email is required."
          		  },
          		HQAddress:{
              			required: "Address is required."
              		  },
              		city:{
                  			required: "City is required."
                  		  },
                  		state:{
                      			required: "State is required."
                      		  },
                      		zipcode:{
                          			required: "Zip code is required."
                          		  },
                          		location: {
                          			required: "Destination, landmark, address or zipcode is required."
                          		  },
      		  },
      		showErrors: function(errorMap, errorList) {
      	      errorList.forEach(function(error) {
      	        if ($(error.element).is('[contenteditable][name]')) {
      	          error.message = validate_messages[error.element.getAttribute('name')];
      	        }
      	      });

      	      this.defaultShowErrors();
      	    },

      	
      });
        })
 
      
      $(".search-button").on('click',function(){
    	  $('.error-msg').each(function(){
    		  $(this).remove();
    	  })
    	  
      })
      $('.date-picker').each(function(){
    	  
      
      
      $(this).find('input').datetimepicker({
        format: "dd/mm/yyyy",
        autoclose: true,
        todayBtn: true,
        startDate: new Date(),
        minuteStep: 60,
        autoclose: true,
        todayBtn: true,
        startView: 2,
        minView: 2,
        maxView: 1,
        minDate: 0,
    })
      })
      
      $('.datePicker').find('input').datetimepicker({
    	  format: "dd/mm/yyyy",
          autoclose: true,
          todayBtn: true,
          minuteStep: 60,
          autoclose: true,
          todayBtn: true,
          startView: 2,
          minView: 2,
          maxView: 1,
          minDate: 0,
	endDate: new Date()
	})
      $('.has-error').each(function(){
	$(this).find('input').on('keyup input', function(){
		$(this).closest('.form-group').removeClass('has-error');
		$(this).closest('.form-group').find('p.error').each(function(){
			$(this).remove();
		})
		if($(this).attr('type')=='password'){
			$(this).closest('form').find('input[type="password"]').closest('.form-group').removeClass('has-error');
		$(this).closest('form').find('p.error[data-label="Password"]').remove();
		}
	})
	})
      
        $('.attendees-dialog').on('keydown click',function(e) {
        	   $(this).focusout();
        	});
        $(".attendees-dialog").on("click", function(){
        	$(this).parent().parent().find(".popup, .popup-content").show();
        	$(this).parent().parent().find(".popup, .popup-content").on('focusout',function(){
   			// $(this).parent().parent().find(".popup, .popup-content").hide();
   		})
        	});
        $('.cost-dialog').on('keydown click',function(e) {
     	 $(this).focusout();
     	});
        

        $(".nav-tabs a").click(function() {
        	  var position = $(this).parent().position();
        	  var width = $(this).parent().width();
        	    $(".slider").css({"left":+ position.left,"width":width});
        	});
        	var actWidth = $(".nav-tabs").find(".active").parent("li").width();
        	var actPosition = $(".nav-tabs .active").position();
        	if(typeof actPosition != 'undefined'){
        	$(".slider").css({"left":+ actPosition.left,"width": actWidth});
        	}
        	
        	$(document).on('click', '.register-modal' , function() {
        		var modalframe = $(this)
        		modalframe.parent().addClass('active');
        		$('#myModalsignup').find('form').each(function(){
        			$(this).find('.form-group').each(function(){
        				$(this).find('input,select').val('')
        				$(this).find('span.help-block').hide()
        			})
        		})
        		
            	$('#myModalsignup').modal('show');
            	$('#myModalsignup').on('hide.bs.modal',function(){
            		modalframe.parent().removeClass('active');	
            		$('.error-view').hide();
            		$('#myModalsignup').find('form').each(function(){
            			$(this).find('.form-group').each(function(){
            				$(this).find('input,select').val('')
            				$(this).find('span.help-block').hide()
            			})
            		})
            		$('.modal-open').css({'padding-right':'0px','overflow':'hidden'})
            		
            	})
        	
        	})
        		
$('.signupuser').on('click',function(){
	$('.businessuserpanel').find('.form-group').each(function(){
		$(this).find('input,select').val('')
		$(this).find('span.help-block').hide()
	})
})	 
	 $('.businessuser').on('click',function(){
	$('.userpanel').find('.form-group').each(function(){
		$(this).find('input,select').val('')
		$(this).find('span.help-block').hide()
	})
})
        	$(document).on('click', '.login-modal' , function() {
        		var modalframe = $(this)
        		modalframe.parent().addClass('active');
        		$('.error-view').hide();
        		$('#myModallogin').find('form .form-group').each(function(){
        			$(this).find('input').val('')
    				$(this).find('span.help-block').hide()
        		})

            	$('#myModallogin').modal('show');
            	$('#myModallogin').on('hide.bs.modal',function(){
            		modalframe.parent().removeClass('active');	
            		$('.error-view').hide();
            		$('#myModallogin').find('form .form-group').each(function(){
            			$(this).find('input').val('')
        				$(this).find('span.help-block').hide()
            		})
            		
            		$('.modal-open').css({'padding-right':'0px','overflow':'auto'})
            	})
        	
        	})
        
        	var changes_made = false;
        $('.form-control, select, input, textarea').each(function() {
            var elem = $(this);
            elem.data('oldVal', elem.val());
            elem.bind("propertychange change click keyup input paste", function(event) {
                if (elem.data('oldVal') != elem.val()) {
                    changes_made = true;
                }
            });
        });
        
        $("form").bind('submit', function() {
            changes_made = false;
        });
        
        	
        	
        /**/
    var csrfmiddlewaretoken = getCookie('csrftoken');
        
        
     $(".cost-dialog").on("click", function(){
    	 $(this).parent().parent().find(".popup, .popup-content").show();
    	 

    	 $(this).parent().parent().find(".popup, .popup-content").on('focusout',function(){
    			 //$(this).parent().parent().find(".popup, .popup-content").hide();
    		})
     	});
        
        
        $(".popup-content .closepopup").on("click", function(){
        	
        	$(this).closest(".popup, .popup-content").hide();
        	});
        
        $('.pay_button').on('click',function(){
        	
        	if($('.get_date_form').val() != ''){
            	
            	$('.bkChkDetails').hide();
            	$('.bkchg').hide();
            	$('.booking-content').hide();
            	$('.booking-form').find('.tabbable-panel').hide();
            	$('.payment-deatil').show();
        		
        	}
        	else{
    			if($('.get_date_form').parent().find('.text-danger').length < 1){
    				$('.get_date_form').parent().append('<p class="text-danger">please select arrival time</p>');	
    			}
    			
    			$('.get_date_form').closest('.form-group').addClass('has-error')
        		$('.get_date_form').on('changeDate input keyup', function(){
        			$('.get_date_form').parent().find('.text-danger').remove();	
        			$('.get_date_form').closest('.form-group').removeClass('has-error');
        			});
        	}
        })

            
    $('.get_date_form').datetimepicker({
        format: "dd/mm/yyyy - hh:ii",
        autoclose: true,
        todayBtn: true,
        startDate: new Date(),
    }).on('changeDate', function(ev){
    	var updateddate = $(this).val()
    	$('#check_date_form').val(updateddate);
	
});
    
    
$('.login-form').find('input').each(function(){
	$(this).on('input',function(){
		$('.error-msg').remove();
	})
})
  
	$(".start_date").datetimepicker({
        format: "dd/mm/yyyy",
        autoclose: true,
        todayBtn: true,
        startDate: new Date(),
        minuteStep: 60,
        autoclose: true,
        todayBtn: true,
        startView: 2,
        minView: 2,
        maxView: 1,
        minDate: 0,
    }).on('changeDate',function(){
    	var updateddate = $(this).data("datetimepicker").getDate()
    	var newDate = updateddate
	     newDate.setDate(newDate.getDate()+1);
    	$(this).closest('form').find(".end_date").closest('.form-group').removeClass('hidden').find('span.help-block').remove()
    $(this).closest('form').find(".end_date").val('')
    $(this).closest('form').find(".end_date").datetimepicker('remove')
	
	
  	$(this).closest('form').find(".end_date").datetimepicker({
  		format: "dd/mm/yyyy",
        autoclose: true,
        todayBtn: true,
        startDate: newDate,
        minuteStep: 60,
        autoclose: true,
        todayBtn: true,
        startView: 2,
        minView: 2,
        maxView: 1,
        minDate: 0,
	    setDate: newDate,
      })
      $(this).closest('form').find(".end_date").datetimepicker('setDate',newDate)
  	$(this).closest('form').find(".end_date").datetimepicker('update');
    	
    })
    $(".end_date").datetimepicker({
        format: "dd/mm/yyyy",
        autoclose: true,
        todayBtn: true,
        startDate: new Date(),
        minuteStep: 60,
        autoclose: true,
        todayBtn: true,
        startView: 2,
        minView: 2,
        maxView: 1,
        minDate: 0,
    })


  
    
	
	if (!Array.prototype.remove) {
  Array.prototype.remove = function(val) {
    var i = this.indexOf(val);
         return i>-1 ? this.splice(i, 1) : [];
  };
}
  

    
   
	$('body').on('click', '.readstate', function() {
		 $.ajax({
		    	url : "/notification/all",
		    	success : function (response) {
		    		$('#Notification__Count').html('0');

		    		var Nonotifyresult = '<div class="text-center link-block"><a class="dropdown-item notify-item notify-all">\
		                    <strong>No notifications</strong>\
		                    </a></div>'	
		    			

		    			$("#Notification__Count").html(0);
		    			$("#Notification__Container").html('');
		    			if (typeof response.count == 'undefined'){
			    			$("#Notification__Count__alert").html('You have 0 New Notification');
			    			}
		    			else{
		    			$("#Notification__Count__alert").html('You have '+response.count+' New Notification');
		    			}
		    			$("#Notification__Container").prepend(Nonotifyresult);
		    			$('.notification-list-scroll').addClass('hidden');
		    		
		    	}
		 })
	})

	$(".submit_date").bind('click', function(){
		$('#agreecheckbox').unbind();
		$('.start_date_book').unbind();
		$('.end_date_book').unbind();
		if($('.start_date_book').val() == ''){
			if($('.start_date_book').parent().find('.text-danger').length < 1){
				$('.start_date_book').parent().append('<p class="text-danger">please select start date</p>');	
			}
			
			$('.start_date_book').closest('.form-group').addClass('has-error')
		}
		
			$('.start_date_book').on('changeDate input keyup', function(){

				$('.start_date_book').parent().find('.text-danger').remove();	
				$('.start_date_book').closest('.form-group').removeClass('has-error');
			})
		
		if($('.end_date_book').val() == ''){
			if($('.end_date_book').parent().find('.text-danger').length < 1){
				$('.end_date_book').parent().append('<p class="text-danger">please select end date</p>');	
			}
			
			$('.end_date_book').closest('.form-group').addClass('has-error')
		}
			$('.end_date_book').on('changeDate input keyup', function(){
			$('.end_date_book').parent().find('.text-danger').remove();	
			$('.end_date_book').closest('.form-group').removeClass('has-error');
			})
		
		if($('#payment0').prop('checked') == false && $('#payment1').prop('checked') == false){
			if($('#payment0,#payment1').parent().find('.text-danger').length < 1){
				$('#payment0,#payment1').parent().append('<p class="text-danger">please select payment method</p>');	
			}
			
			$('#payment0,#payment1').closest('.form-group').addClass('has-error')
			
		}
		else{
			$('#payment0,#payment1').parent().find('.text-danger').remove();	
			$('#payment0,#payment1').closest('.form-group').removeClass('has-error');
		}
		if(!$('.agreecheckbox').hasClass('fa-check-square-o')){
			if($('.agreecheckbox').parent().find('.text-danger').length < 1){
				$('.agreecheckbox').parent().append('<p class="text-danger">please agree Vicinity Customer Agreement</p>');	
			}
			
			$('.agreecheckbox').closest('.form-group').addClass('has-error')
		}
			$('#agreecheckbox').on('click',function(){
				$('.agreecheckbox').parent().find('.text-danger').remove();	
				$('.agreecheckbox').closest('.form-group').removeClass('has-error');
				
			})
		if($('.noofattendees').val() == ''){
			if($('.noofattendees').parent().find('.text-danger').length < 1){
				$('.noofattendees').parent().append('<p class="text-danger">please enter no. of attendees</p>');	
			}
			
			$('.noofattendees').closest('.form-group').addClass('has-error')
		}
			$('.noofattendees').on('input keyup', function(){
			$('.noofattendees').parent().find('.text-danger').remove();	
			$('.noofattendees').closest('.form-group').removeClass('has-error');
			});
		
		
		var hourrent = 2
		if (hourrent < 1){
			hourrent = 1
		}
		
		  $(this).closest('form').find('#pricevalue').val(parseInt($(this).closest('form').find('#priceset').val())*parseInt(hourrent))
		
	})
    // Open close small chat
	if (sessionStorage.getItem('userID') == 'true'){
		$('#small-chat').show();
		if (sessionStorage.getItem('usernotitifID') == 'true'){
			$('#small-chat').hide();
			}
    $('.open-small-chat').on('click', function () {
        $(this).children().toggleClass('fa-comments').toggleClass('fa-remove');
        $('.small-chat-box').toggleClass('active');
		var user = $('#userdata').attr('data-id');
        //msgs_logs_update(user)
		$('.msg_container').html('')
		$('.msg_container').removeAttr('id')
		$('.messagechat').val('')
		$('.send-message').unbind()
        chat_list(user)

//	 	socket_chat.send(JSON.stringify({
//	         "command": "join",
//	         "room": $('.open-small-chat').attr("data-room-id")
//	     }));
    });
    
	
    
    function chatmodel(){
     $('.sendmssge').on('click', function() {
    	 var usersender = $(this).attr('data-id');
    		var usersender = $('#userdata').attr('data-id');
    		$('#user__fullname').attr('data-id');
    		$('.send__user').html($(this).attr('data-name'))
            roomId = $(this).attr("data-room-id");;
    		
            $(this).addClass("joined");
    if (!$('.small-chat-box').hasClass('active')){

    	$('#small-chat').show();
    	$('.chat-link').trigger('click');
    	
    }
        })
    }
        chatmodel();
        $('.messagechat').on('input', function(){
        	$(this).attr('value', $(this).val())
        })
	}

if (sessionStorage.getItem('userID') == 'true'){
socket_notif.onmessage = function (event) {
	data = JSON.parse(event.data)
	if (data.event=='notificationupdate'){
		notificationalert();

	}
	    };
	    socket_message.onmessage = function (event) {
	    	data = JSON.parse(event.data)
	    	if (data.event=='messageupdate'){

	    		 messagealert();
	    		
	    	}

	    	    };

		
		$(document).on('click', '.getmsglogs',function () {
			var user = $(this).attr('data-id');
			$(this).parent().find('.getmsglogs').removeClass('activechat')
			$(this).addClass('activechat')
			msgs_logs_update(user);
			$('.add-message').removeClass('hidden');
			$('.send-message').attr('data-id',$(this).attr('data-id'));
			$(this).find('.bullet-icon').removeClass('bullet-icon');
			
			var roomId = $(this).attr("data-room-id")
			$('.msg_container').attr('id','msg_container-'+roomId)

		 	socket_chat.send(JSON.stringify({
		         "command": "join",
		         "room": roomId,
                 "userreceiver": user
		     }));
		 	$('.send-message').unbind();
			   $('.send-message').on('click', function() {
			    	 var userreceiver = $(this).attr('data-id');
			    		var usersender = $('#userdata').attr('data-id');
			    		socket_chat.send(JSON.stringify({
		                    "command": "send",
		                    "room": roomId,
		                    "message": $(".messagechat").val(),
		                    "userreceiver": userreceiver
		                }));
			    		
			            $(this).addClass("joined");
			        		handle_post_msg(userreceiver, usersender)
			        })
		})
}

$('.availability').each(function(){
	$(this).find('input').on('click',function(){
	    var csrfmiddlewaretoken = getCookie('csrftoken');
		$.ajax({
	        type: 'POST',
	        url: '/managerooms/yourrooms/'+ $(this).attr('data-id') +'/availability',
	        data: {    	        
	            "csrfmiddlewaretoken": csrfmiddlewaretoken,
	        },
	        datatype: "json",
	        success: function(data){
	        	
	        }
		})
	})
})
});



function notificationalert() {
    var csrfmiddlewaretoken = getCookie('csrftoken');
    $.ajax({
    	type: 'POST',
    	url : "/notification/new",
    	data:{
    		'userid': $('#request_user').val(),
            "csrfmiddlewaretoken": csrfmiddlewaretoken,
    	},
    	 datatype: "json",
    	success : function (response) {
    		if( response.status == 200 ) {
				if(response.data[0].to_user_id == $('#request_user').val()){
    			var html = "";
    			if( response.data != '' && typeof response.data != 'undefined' ) {
    				$.each( response.data, function (key, value) {
                        var options = {weekday: 'short', month: 'long', day: 'numeric', minute: 'numeric', hour: 'numeric'};
    	                d = new Date(value.time);
    	                if (value.link = ''){
    	                	href = value.link
    	                }
    	                else{
    	                	href = 'javascript:void(0);'
    	                }
    					html += `<a href="`+href+`" class="single-mail">
                                    <span class="icon bg-primary">
                                        <i class="fa fa-envelope-o"></i>
                                    </span>
                                    <strong>`+value.message+`</strong>

                                    <p>
                                        <small>`+ d.toLocaleString('en-US', options) +`</small>
                                    </p>
                                    
                                </a>`;
    				} );
    			}
    			var notifyresult = ''
    			if(response.count>0){html += notifyresult;

    			$('.notifybullet').addClass('notif-bullet');}
    			$("#Notification__Count").html(response.count);
    			$("#Notification__Count__alert").html('You have '+response.count+' New Notification');
    			$("#Notification__Container").html('');
    			$("#Notification__Container").prepend(html);
    			$('.notification-list-scroll').removeClass('hidden');
    			
    			if( typeof response.latest.message != 'undefined' && typeof response.latest.modelid != 'undefined' ) {
    				if(response.latest.link != ''){
    					href = response.latest.link
    				}
    				else{
    					href = 'javascript:void(0);'
    				}
    				if(response.latest.to_user_id == $('#request_user').val()){
    				$.amaran({
        				
        			    'position'  :'top right',
        			    'content'   :{
        			           bgcolor:'#257D7D',
        			           color:'#fff',
        			           message   :'<a href="'+ href +'" style="color:#fff;">'+response.latest.message+'</a>'
        			        },
        		        'closeOnClick'  :true,
        		        'cssanimationIn':'bounceInRight',
        		        'cssanimationOut':'fadeOutRight',
        		        'outEffect':'slideRight',
        		        'closeButton'   :true,
        		        'delay':4000,
        		        'theme'     :'colorful'
        			});
    			}
    		}
    		}
     	}
    		}
    });
}


function messagealert() {
    $.ajax({
    	url : "/message/new",
    	success : function (response) {
    		if( response.status == 200 ) {

    			var html = "";
    			if( response.data != '' && typeof response.data != 'undefined' ) {
    				$.each( response.data, function (key, value) {
                        var options = {weekday: 'short', month: 'long', day: 'numeric', minute: 'numeric', hour: 'numeric'};
    	                d = new Date(value.time);
    					html += `<a href="/booking/user/" class="single-mail">
                                    <span class="icon bg-primary">
                                        <i class="fa fa-envelope-o"></i>
                                    </span>
                                    <strong>`+value.message+`</strong>

                                    <p>
                                        <small>`+ d.toLocaleString('en-US', options) +`</small>
                                    </p>
                                    
                                </a>`;
    				} );
    			}
    			var notifyresult = ''
    			if( typeof response.latest.message != 'undefined' && typeof response.latest.modelid != 'undefined' && response.latest.pk != $('#userdata').attr('data-id') ) {
    				
    				href = 'javascript:void(0);'
    				
    				$.amaran({
        				
        			    'position'  :'top right',
        			    'content'   :{
        			           bgcolor:'#257D7D',
        			           color:'#fff',
        			           message   :'<a href="'+ href +'" style="color:#fff;">'+response.latest.message+'</a>'
        			        },
        			        'closeOnClick'  :true,
            		        'cssanimationIn':'bounceInRight',
            		        'cssanimationOut':'fadeOutRight',
            		        'outEffect':'slideRight',
            		        'closeButton'   :true,
            		        'delay':4000,
            		        'theme'     :'colorful'
        			});
    				if($('[data-room-id="'+ response.latest.roomId +'"]').find('.bullet-icon').length < 1 && typeof $('#msg_container-'+response.latest.roomId).html() == 'undefined'){
    				 $('<span class="bullet-icon"></span>').insertAfter($('[data-room-id="'+ response.latest.roomId +'"]').find('label'));
    				}
    				
    				
    			}

    		}
     	}
    });
}


function showDays(firstDate,secondDate){
    
    

    var startDay = new Date(firstDate);
    var endDay = new Date(secondDate);
    var millisecondsPerDay = 1000 * 60 * 60 * 60 * 60;

    var millisBetween = startDay.getTime() - endDay.getTime();
    var days = millisBetween / millisecondsPerDay;

    return Math.floor(days);

}


function socketsend(socket_chat) {
    socket_chat.onmessage = function (message) {

	        var data = JSON.parse(message.data);
	        

	        if (data.error) {
	            console.log(data.error);
	            return;
	        }

	        if (data.join) {
	            $('.sendmssge').unbind();
	            $(".sendmssge").on("click", function () {	            	
	            	socket_chat.send(JSON.stringify({
	                    "command": "send",
	                    "room": data.join,
	                    "message": $(".messagechat").val()
	                }));

	        		var usersender = $('#userdata').attr('data-id');
	        		var userreceiver = $(this).attr('data-id');
			        		handle_post_msg(userreceiver, usersender)
	                return false;
	            });		    
	            

	        } else if (data.leave) {
	            $("#room-" + data.leave).remove();

	        } else if (data.message || data.msg_type != 0) {
	            var msgdivchat = $("#msg_container-" + data.room);
	            var ok_msg_chat = "";

	            switch (data.msg_type) {
	                case 0:
	                	var direction= 'left'
	                	var classname = ''
	                		var fullname = data.userreceiver;
	                	if ($('#usernamedata').attr('data-id') == data.username){
	                		direction= 'right'
	                			classname = 'sender'
	                				fullname = data.fullname
	                	}
	                	var now = new Date().getTime();
	                	ok_msg_chat = '<hr><div class="'+direction+'">\
	                    <div class="author-name">'+fullname+' <small class="chat-date chat-time" data-now="'+ now +'">now</small>\
	                    </div> <div class="chat-message active '+ classname +'"> '+data.message+'</div></div>';

	                    break;
	                case 1:

	                	ok_msg_chat = "";
	                    socketsend(socket_chat);
	                    break;
	                case 2:

	                	ok_msg_chat = "";
	                    socketsend(socket_chat);
	                    break;
	                case 3:

	                	ok_msg_chat = "";
	                    socketsend(socket_chat);
	                    break;
	                case 4:

	                	ok_msg_chat = "";
	                    socketsend(socket_chat);
	                    break;
	                case 5:

	                    ok_msg = "";
	                    socketsend(socket_chat);
	                    break;
	                default:
	                    console.log("Unsupported message type!");
	                	socketsend(socket_chat);
	                    return;
	            }
	            
	            msgdivchat.append(ok_msg_chat);
	            var x = setInterval(function() {
	                var now = new Date().getTime();
	                
	                msgdivchat.find('.chat-time').each(function(){
	                	var current = $(this).attr('data-now')
		                var distance = now - current
		                var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
		                var seconds = Math.floor((distance % (1000 * 60)) / 1000);
	                	
	                	if(minutes > 0){
	                		$(this).html(minutes + "m " + seconds + "s ago");	
	                	}
	                	else{
	                		if(seconds > 0){
	                		$(this).html(seconds + "s ago");
	                		}
	                	}
	                })
	                
	            }, 1000);
	            msgdivchat.scrollTop(msgdivchat.prop("scrollHeight"));
	        } else {
	        	
	        }
	        $(".messagechat").val("");
            $(".messagechat").attr("value","");
	    };
	    socket_chat.onclose = function () {
	    	socketsend(socket_chat);
	    }
}

function msgs_logs_update(fromId){
    var msg_container = $('.msg_container');
    msg_container.empty();
    $.ajax({
        type: 'GET',
        url: '/chat/msgslogsget/',
        data: {fromId},
        datatype: "json",
        success: function(data){
            var item = "";
            var d,direction;
            var options = {weekday: 'short', month: 'long', day: 'numeric', minute: 'numeric', hour: 'numeric'};
            if(data != ""){
                $.each(data, function(key, value) {
                	if(key == 'data'){
                		$.each(value, function(key, element) {
                			var classname = ''
                			if(element.receiver_id == $('#userdata').attr('data-id'))
                				{direction= 'left'
                					name=element.sender_name}
                			if(element.sender_id == $('#userdata').attr('data-id'))
            				{direction= 'right'
            					name=element.sender_name
            					classname='sender'}
                    d = new Date(element.created_on);
                    item +='<hr><div class="'+direction+'">\
                    <div class="author-name">'+name+' <small class="chat-date"> '+d.toLocaleString('en-US', options)+'</small>\
                    </div> <div class="chat-message active '+ classname +'"> '+element.message+'</div></div>';
 
                		})
                	}
                    	
                });
            } 
else{
item = '<p>No messages yet ! send first msg ?</p>';
 }
            msg_container.html(item);
            
            msg_container.scrollTop(msg_container.prop("scrollHeight"));
        }
    });
    return true
}


function handle_post_msg(fromId, toId){
    var csrfmiddlewaretoken = getCookie('csrftoken');
    var msg = $(".messagechat").attr('value')
    if (msg != "" && fromId && fromId != toId){
        
            $.ajax({
                type: 'POST',
                url: '/chat/msgslogspost/',
                data: {
                    "fromId": fromId,
                    "toId": toId,
                    "msg": msg,
                    "csrfmiddlewaretoken": csrfmiddlewaretoken,
                },
                datatype: "json",
                success: function(data){
                    $(".messagechat").val("");
                    $(".messagechat").attr("value","");
                }
            });
    } else{
    }
}

function msg_update_state(fromId, toId){
    var csrfmiddlewaretoken = getCookie('csrftoken');
    if (fromId && fromId != toId){
        
            $.ajax({
                type: 'POST',
                url: '/message/read',
                data: {
                    "fromId": fromId,
                    "toId": toId,
                    "csrfmiddlewaretoken": csrfmiddlewaretoken,
                },
                datatype: "json",
                success: function(data){
                    
                }
            });
    } else{
    }
}


function addwishlist(self, Id, result){
    var csrfmiddlewaretoken = getCookie('csrftoken');
    
            $.ajax({
                type: 'POST',
                url: '/room-wish-list/',
                data: {
                    "Id": Id,
                    "csrfmiddlewaretoken": csrfmiddlewaretoken,
                },
                datatype: "json",
                success: function(data){
                	if(data=='saved' && result){
                		self.html('<i class="fa fa-heart text-red"></i>');
                		self.attr('data-content', 'Remove from favorites')
                		self.popover("show")
                	}
                	if(data=='delete' && result){
                    	self.html('<i class="fa fa-heart-o"></i>');
                    	self.attr('data-content', 'Save to favorites')
                    	self.popover("show")
                    }
                    if(data=='saved' && !result){
                    	self.html('<i class="fa fa-heart text-red"></i> Saved ');
                    }
                    if(data=='delete' && !result){
                    	self.html('<i class="fa fa-heart-o"></i>  Save to favorites ');                    	
                    }
                }
            });
}

function getreviews(Id, count){
        
            $.ajax({
                type: 'GET',
                url: '/get-reviews/',
                data: {
                    "Id": Id,
                    "count": count,
                },
                datatype: "json",
                success: function(data){
                    
                    	$('.comments').find('li:last-child').append(data)
                    
                }
            });
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);

            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function quotecheck (self,e, message) {

	var validator = self.closest('form').validate();
	validator.resetForm();
/*e.preventDefault()*/
    var csrfmiddlewaretoken = getCookie('csrftoken');
	var dateArry = []
	$('.date_extend').find('.row').each(function(){
		var self = $(this);
		if(self.find(".start_time_book").val() != '' && self.find(".end_time_book").val() != ''){
			var start_time_book = self.find(".start_time_book").data("datetimepicker").getDate().toString()
			var end_time_book = self.find(".end_time_book").data("datetimepicker").getDate().toString()
			dateArry.push({'start_time_book':start_time_book,
				'end_time_book':end_time_book})
		}
	
    
	});
	 $.ajax({
	    	url : "/get-quote-booking/",
	    	type: 'POST',
	    	datatype: "json",
	    	data: {
	    		'Id':$('#roomId').val(),
	    		'dateArry': JSON.stringify(dateArry),
                "csrfmiddlewaretoken": csrfmiddlewaretoken,
	    		},
    	success : function (response) {
    		if(response){
    			$('.errornotebooking').html(response)
    			if(self.closest('form').valid() && !response){
    				self.attr('type','submit');
        			}
    			else{
    				self.attr('type','button');
    			}
    			$('.quote-get-result').addClass('hidden')
    			
    		}
    		else{
    			$('.errornotebooking').html('')
    			if(!message){
    			pricearry=[]
    			
    			$('.date_extend').find('.row').each(function(){
		var self = $(this);
		if(self.find(".start_time_book").val() != '' && self.find(".end_time_book").val() != ''){
			var start_time_book = self.find(".start_time_book").data("datetimepicker").getDate().toString()
			var end_time_book = self.find(".end_time_book").data("datetimepicker").getDate().toString()
			pricearry.push({'start_time_book':start_time_book,
				'end_time_book':end_time_book})
		}
	
    
	});
    			var hours = 0

    			for (var i = 0; i < pricearry.length; i++) {

    				hours += parseInt(Math.abs(new Date(pricearry[i]['end_time_book']) - new Date(pricearry[i]['start_time_book'])) / 36e5);

       
    			}
    			$('.hours-quote').html(hours);
    			$('.total-hours-price').html(parseFloat($('.price-quote').html()) * hours)
    			var total_quote = parseFloat('0.00')
    			$('.total-quote').each(function(){
        			total_quote += parseFloat($(this).html())
    			})
    			$('.sub-total-quote').html(total_quote)
    			$('#pricevalue').val(total_quote)
    			if(pricearry.length > 0 && self.closest('form').valid()){
    			$('.quote-get-result').removeClass('hidden')
    			}

    			if(self.closest('form').valid()){
    			self.attr('type','submit');
    			}
    		}
    			else{

    				if(self.closest('form').valid()){
    	    			self.closest('form').submit();
    	    			}	
    			}
    	}
    	}
	 })
	 
	 
    }

function getdetail(model, id, update,board){
	$.ajax({
        type: 'GET',
        url: '/contentdetail/',
        data: {
            "model": model,
            "id":id,
            "update":update,
            "board":board,
            "next": window.location.pathname
        },
        datatype: "json",
        success: function(data){
        	$('.content-form').html(data);
        	if(update != true){
    		$('#update-modal').modal('show');
        	}
        	      	
        }
    });
}

function verifyUserEmail(model){
	$.ajax({
        type: 'GET',
        url: '/contentdetail/',
        data: {
            "model": model,
            "email":true,
            "next": window.location.pathname
        },
        datatype: "json",
        success: function(data){
        	$('.content-email-form').html(data);
    		$('#update-email-modal').modal('show');
        	      	
        }
    });
}

function verifyEmailVerificationCode(self){
	self.closest('form').validate({
		 rules: {
		verify_input: {
	            required: true,
	            maxlength: 4
	        },
		 },  messages: {
			 verify_input: {
    		      required: "Verification code is required."
    		    }
    		  },
	})
	if(self.closest('form').valid()){
	    var csrfmiddlewaretoken = getCookie('csrftoken');
	   
	$.ajax({
        type: 'POST',
        url: '/verifyemail/',
        data: {
            "verify_input": self.closest('form').find('#email_verify').val(),
            "csrfmiddlewaretoken": csrfmiddlewaretoken,
        },
        datatype: "json",
        success: function(data){
        	if(data == 'verified'){
        		window.location.reload();
        	}
        	if(data == 'error'){
        		$('.errorverified').removeClass('hidden');
        	}
    		
        	      	
        }
    });
	}
}

function sendEmailVerificationCode(model){
    var csrfmiddlewaretoken = getCookie('csrftoken');
	$.ajax({
        type: 'GET',
        url: '/resend-email/',
        data: {
            "next": window.location.pathname,
            "csrfmiddlewaretoken": csrfmiddlewaretoken,
        },
        datatype: "json",
        success: function(data){
        	window.location.reload();        	      	
        }
    });
}

function loginsubmit(self){

	if(self.closest('form').valid()){
	self.closest('form').submit(function(event) {
		event.preventDefault();
		$.ajax({
	        type: $(this).attr('method'), 
	        url: $(this).attr('action'),
	        data: $(this).serialize(),
	        datatype: "json",
	        success: function(data){
	        },
	        statusCode: {
	            202: function(data) {
	            	$('#myModallogin').modal('hide');
	            	$('.modal-backdrop').remove();
    	        	$('.header-update').html(data);
    	        	$('.message-data-update').hide();
    	        	notificationalert();
    	       	 messagealert();
    	     	socket_notif = new ReconnectingWebSocket(ws_notif);
    	    	socket_chat = new ReconnectingWebSocket(ws_path);
    	    	socket_message = new ReconnectingWebSocket(ws_message);
    	    	socketsend(socket_chat);
    	    	
    	    	
    	       	if (sessionStorage.getItem('userID') == 'true'){
    	    		$('#small-chat').show();
    	    		if (sessionStorage.getItem('usernotitifID') == 'true'){
    	    			$('#small-chat').hide();
    	    			}
    	        $('.open-small-chat').on('click', function () {
    	            $(this).children().toggleClass('fa-comments').toggleClass('fa-remove');
    	            $('.small-chat-box').toggleClass('active');
    	    		var user = $('#userdata').attr('data-id');
//    	            msgs_logs_update(user)
    	    		$('.msg_container').html('')
    	    		$('.msg_container').removeAttr('id')
    	    		$('.messagechat').val('')
    	    		$('.send-message').unbind()
    	    		chat_list(user)

//    	    	 	socket_chat.send(JSON.stringify({
//    	    	         "command": "join",
//    	    	         "room": $('.open-small-chat').attr("data-room-id")
//    	    	     }));
    	        });
    	        
    	    	
    	        
    	        function chatmodel(){
    	         $('.sendmssge').on('click', function() {
    	        	 var usersender = $(this).attr('data-id');
    	        		var usersender = $('#userdata').attr('data-id');
    	        		$('#user__fullname').attr('data-id');
    	        		$('.send__user').html($(this).attr('data-name'))
    	                roomId = $(this).attr("data-room-id");;
    	        		
    	                $(this).addClass("joined");
    	        if (!$('.small-chat-box').hasClass('active')){

    	        	$('#small-chat').show();
    	        	$('.chat-link').trigger('click');
    	        	
    	        }
    	            })
    	        }
    	            chatmodel();
    	            $('.messagechat').on('input', function(){
    	            	$(this).attr('value', $(this).val())
    	            })
    	    	}
    	       	 
    	       	if (sessionStorage.getItem('userID') == 'true'){
    	       		socket_notif.onmessage = function (event) {
    	       			data = JSON.parse(event.data)
    	       			if (data.event=='notificationupdate'){
    	       				notificationalert();

    	       			}
    	       			    };
    	       			    socket_message.onmessage = function (event) {
    	       			    	data = JSON.parse(event.data)
    	       			    	if (data.event=='messageupdate'){

    	       			    		 messagealert();
    	       			    		
    	       			    	}

    	       			    	    };

    	       				
    	       				$(document).on('click','.getmsglogs', function () {
    	       					var user = $(this).attr('data-id');
    	       					$(this).parent().find('.getmsglogs').removeClass('activechat')
    	       					$(this).addClass('activechat')
    	       					msgs_logs_update(user);
    	       					$('.add-message').removeClass('hidden');
    	       					$('.send-message').attr('data-id',$(this).attr('data-id'));
    	       					$(this).find('.bullet-icon').removeClass('bullet-icon');
    	       					
    	       					var roomId = $(this).attr("data-room-id")
    	       					$('.msg_container').attr('id','msg_container-'+roomId)

    	       				 	socket_chat.send(JSON.stringify({
    	       				         "command": "join",
    	       				         "room": roomId,
    				                    "userreceiver": user
    	       				     }));
    	       				 	$('.send-message').unbind();
    	       					   $('.send-message').on('click', function() {
    	       					    	 var userreceiver = $(this).attr('data-id');
    	       					    		var usersender = $('#userdata').attr('data-id');
    	       					    		socket_chat.send(JSON.stringify({
    	       				                    "command": "send",
    	       				                    "room": roomId,
    	       				                    "message": $(".messagechat").val(),
    	       				                    "userreceiver": userreceiver
    	       				                }));
    	       					    		
    	       					            $(this).addClass("joined");
    	       					        		handle_post_msg(userreceiver, usersender)
    	       					        })
    	       				})
    	       		}
    	       	$('.show_login_auth').each(function(){
    	       		$(this).addClass('hidden')
    	       		$(this).parent().find('.hidden_login_auth').removeClass('hidden')
    	       	})
    	       	 
	            },
	            201: function(data) {
	        	$('.login-update').html(data)
            }
	        },
		})
    })
}
}

function loginmodal(){

	$('#myModalsignup').modal('hide');
	$('.modal-backdrop').remove();
	$('.login-modal').trigger('click');
}

function signupmodal(){

	$('#myModallogin').modal('hide');
	$('.modal-backdrop').remove();
	$('.register-modal').trigger('click');
		//loginmodal();
}




function signupsubmit(self){
	 $('form').each(function(){$(this).validate({ignore: [],
     	wrapper: 'span',
   	  rules: {
   		username_user:{
	            required: true},
   		username_business:{
	            required: true},
   		  email: {
	            required: true
	        },
   		    password: {
   	            required: true,
   	            minlength: 8
   	        },
   		    password_business: {
   	            required: true,
   	            minlength: 8
   	        },
   		    password_confirm: {
   		      equalTo: "#id_password",
   		            required: true,
   		            minlength: 8
   		    },
   		    password_confirm_business: {
     		      equalTo: "#id_password_business",
     		            required: true,
     		            minlength: 8
     		    },
   		    contact_no: {
   	            required: true,
   	            digits: true,
   	            minlength: 5,
   	            maxlength: 15
   	        },
   	        
   		  },  messages: {
   		    email: {
   		      required: "Email address is required."
   		    },username_user: {
   		      required: "Username is required."
   		    },username_business: {
   		      required: "Username is required."
   		    },username: {
   		      required: "Email / Username is required."
   		    },first_name: {
   		      required: "First name is required."
   		    },last_name: {
   		      required: "Last name is required."
   		    },password: {
   		      required: "Password is required."
   		    },password_business: {
   		      required: "Password is required."
   		    },password_confirm: {
   		      required: "Password (again) is required."
   		    },contact_no: {
   		      required: "Contact no is required."
   		    },
           		city:{
               			required: "City is required."
               		  },
               		state:{
                   			required: "State is required."
                   		  },
                   		zipcode:{
                       			required: "Zip code is required."
                       		  },
   		  },
   		showErrors: function(errorMap, errorList) {
   	      errorList.forEach(function(error) {
   	        if ($(error.element).is('[contenteditable][name]')) {
   	          error.message = validate_messages[error.element.getAttribute('name')];
   	        }
   	      });

   	      this.defaultShowErrors();
   	    },

   	
   });
     })
	if(self.closest('form').valid()){
	self.closest('form').submit(function(event) {
		event.preventDefault();
		$('.spinner-absolute').show();
		$.ajax({
	        type: $(this).attr('method'), 
	        url: $(this).attr('action'),
	        data: $(this).serialize(),
	        datatype: "json",
	        success: function(data){
	        	$('.spinner-absolute').hide();
	        },
	        statusCode: {
	        	 202: function(data) {
	    	        	$('.register-buisness-update').html(data);
	    	        	
		            },
	            201: function(data) {
	        	$('.register-user-update').html(data);
            },
	            200: function(data) {
	            	$('#myModalsignup').modal('hide');
	            	$('.modal-backdrop').remove();
    	        	$('.message-data-update').html(data);
            }
	        },
		})
    })
	}
}
function chat_list(user){
	$.ajax({
    type: 'GET',
    url: '/chat-list/',
    data: {
        "user": user,
    },
    datatype: "json",
    success: function(data){
    	$('.list_get').html(data);
    	      	
    }
});}