const valid_flight=/(?:(?<=^)|(?<=\.)|(?<=\s))[1-9,A-Z,А-Я][A-Z,А-Я,1-9]\s{0,1}[ ,-]{0,1}\d{3,4}(?=\s|$)/g;
const valid_route=/(?:(?<=^)|(?<=\.)|(?<=\s))(([A-Z,А-ЯЁ]{3,4})([A-Z,А-ЯЁ]{3,4}))(?=\s|$)/g;
const valid_date=/(?:(?<=^)|(?<=\.)|(?<=\s))((\d{2})([A-Z,А-ЯЁ]{3})(\d{2}){0,1})(?=\s|$)/g;
const valid_time=/(?:(?<=^)|(?<=\.)|(?<=\s))(\d{4})\s{1,}(\d{4})(\+1){0,1}(?=\s|$)/g;
const valid_regex = [valid_flight,valid_route,valid_date,valid_time];

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
	//if any fails
	//for ( const v of valid_regex ) {
	//		console.log ( ( pnr_string.match(v) 	|| [] ).length  ) ;
	//};//else
	return valid_regex.every(vr => (pnr_string.match(vr) || []).length == 1);
}

//calls decoder once textbox changes    
async function instant_decoder(filled_form){
	var valid_pnr_strings = [];
	var codes =  document.getElementById("gds_input").value.split(/\r?\n/);
	//console.log(codes);
	//are there any valid PNR strings?
	for (const current_string of codes ){
		let is_valid = await pnr_string_is_valid(current_string);
		if (is_valid)
		{
			console.log(current_string);
			valid_pnr_strings.push(current_string);
		}
	}
//	console.log(valid_pnr_strings);
	if (valid_pnr_strings.length == 0){
		document.getElementById("decoder_out").value = "Ожидаю корректные данные";
		return;
	}
	//get the set language and launch the converter
	//console.log(base_url)
	let parts = base_url.split('/');
	//console.log(parts);
	let urla = parts.slice(0,parts.length-2);
	//console.log(urla);
	let url = urla.join('/');
	//console.log(url);
	let lang_selector = document.getElementById("form-select");
	let language_selected = lang_selector.value;
	//API url for selected language
	let codes_url = url.concat('/', language_selected ).concat('/');	
	//console.log(codes_url);
	//codes = document.getElementById("gds_input").value = "Идет декодирование...";	
	//console.log(codes);
	document.getElementById("decoder_out").value = "Идет декодирование...";	
	let codes_in_json = {
		headers: {
		'Content-Type': 'application/json'
		},
		method: 'POST',
		body: JSON.stringify(valid_pnr_strings)
	}
	console.log(codes_in_json);
	response = null;
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
		let errors_lines = decoded_data.errors.join('\r\n');
		console.log(errors_lines);
		document.getElementById("decoder_out").value = errors_lines;
		return;
	}			
	else{
		console.log(Array(decoded_data.data));
		//format string
		let lines = [];
		for (const line of JSON.parse(decoded_data.data)){			
			console.log(line);
			formatted_line = `${line.flight_code} ${line.day} ${line.month} ${line.year} ${line.from_time}-${line.to_time} ${line.from_airport}-${line.to_airport}`;
			lines.push(formatted_line);
		}
		document.getElementById("decoder_out").value  = lines.join('\r\n');
		console.log(decoded_data.data);//.join('\r\n'));
	 }
}

window.addEventListener('load', (event) => {
	let parts = base_url.split('/');
	let default_language  = parts[parts.length-2];
	let lang_selector = document.getElementById("form-select");
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
