//	номер рейса
	const valid_flight = /\b[A-Z,А-Я][A-Z,А-Я,1-9][ ,-]{0,1}\d{3,4}\b/;
//	маршрут
	const valid_route = /\b([A-Z,А-ЯЁ]{3,4})([A-Z,А-ЯЁ]{3,4})/;
//	дата 3 группы и общая группа
	const valid_date =  /\b((\d{2})(\w{3})(\d{2}))\b/;
//	время вылета и прилета в 2 группы
//	const valid_time = /(\d{4})\s(\d{4})/;
//	с прилетом на следующий день в отдельной группе
	const valid_time  = /(\d{4})\s(\d{4})(\+1){0,1}/;
//	const valid_pnr_full_ver1 = /^.*(?=.*\b[A-Z,А-Я][A-Z,А-Я,1-9][ ,-]{0,1}\d{3,4}\b){1}(?=.*\b[A-Z,А-ЯЁ]{3,4}[A-Z,А-ЯЁ]{3,4}\b){1}(?=(\b\d{4}\b.*?){2})(\b\d{4}\b).*$/gm;
//	const valid_pnr_full_ver2 = /^\w{2}\s{0,1}\d{3,4}\s\w\s\w{5}\s\d\s\w{6}\s\w{3}\s+\w{4}\s\w{4}(\+1){0,1}\s+\w{3}\s\w\s\d$/gm;

 
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

async function pnr_string_is_valid(pnr_string){
	if (
			((pnr_string.match(valid_flight) || []).length == 1)&&
			((pnr_string.match(valid_route) || []).length == 3)&&
			((pnr_string.match(valid_date) || []).length == 5)&&
			(
				((pnr_string.match(valid_time) || []).length == 3)||
				((pnr_string.match(valid_time) || []).length == 4)
			)
		)
		return true;
	else		
		return false;
}

//calls decoder once textbox changes    
async function instant_decoder(filled_form){
	var valid_pnr_strings = [];
	var codes =  document.getElementById("gds_input").value;
	console.log(codes);
	//are there any valid PNR strings?
	for ( current_string in codes ){
		let is_valid = await pnr_string_is_valid(current_string);
		if (is_valid)
		{
			valid_pnr_strings.push(current_string);
		}
	}
	console.log(valid_pnr_strings);
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
