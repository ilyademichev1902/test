 
/*function instant_decoder(filled_form){
	
	console.log("change");
	$.ajax({
		url:'/list_codes',
		type:'GET',
		success: function(response){
			console.log(response);
		},
		error: function(error) {
			console.log(error);
		}
	});
}*/

//calls decoder once textbox changes    
async function instant_decoder(filled_form){
	var codes =  document.getElementById("gds_input").value;
	console.log(codes);
	//are there any valid PNR strings?
	if ((codes.match(valid_pnr) || []).length == 0) {
		document.getElementById("decoder_out").value = "Ожидаю корректные данные";
		return;
	}
	//get the set language and launch the converter
	//console.log(base_url)
	parts = base_url.split('/');
	//console.log(parts);
	urla = parts.slice(0,parts.length-2);
	//console.log(urla);
	url = urla.join('/');
	//console.log(url);
	lang_selector = document.getElementById("form-select");
	language_selected = lang_selector.value;
	//API url for selected language
	codes_url = url.concat('/', language_selected ).concat('/');	
	//console.log(codes_url);
	//codes = document.getElementById("gds_input").value = "Идет декодирование...";	
	//console.log(codes);
	document.getElementById("decoder_out").value = "Идет декодирование...";	
	codes_in_json = {
		headers: {
		'Content-Type': 'application/json'
		},
		method: 'POST',
		body: JSON.stringify(valid_pnr_strings)
	}
	console.log(codes_in_json);
	try{
		response = await fetch(codes_url,codes_in_json);
		if (!response.ok) throw "Bad response"; 
	}
	catch(err){
		document.getElementById("decoder_out").value = "Ошибка передачи данных.";
		return
	}

	let decoded_data = await response.json();	
	if ((decoded_data.errors || []).length > 0){
		console.log(decoded_data.errors);
		errors_lines = decoded_data.errors.join('\r\n');
		console.log(errors_lines);
		document.getElementById("decoder_out").value = errors_lines;
		return;
	}			
	//console.log(decoded_data.data);
	document.getElementById("decoder_out").value  = decoded_data.data;//  .join('\r\n');

}

window.addEventListener('load', (event) => {
	parts = base_url.split('/');
	default_language  = parts[parts.length-2];
	lang_selector = document.getElementById("form-select");
	lang_selector.value = default_language;
	//console.log(default_language);
	document.getElementById("decoder_out").value = "Ожидаю корректные данные";
	document.getElementById('form-select').addEventListener(
		'change', async function() {
		console.log('You selected: ', this.value);
		await instant_decoder(this);
	}
	);
	document.getElementById('copy-button').addEventListener(
	'click', async function() {		
		try {
		  text = document.getElementById("decoder_out").value;
		  await navigator.clipboard.writeText(text);
		  console.log('Content copied to clipboard');
		} catch (err) {
		  console.error('Failed to copy: ', err);
		}
	}		
	);
})
