async function server(data, type){
    let response = await fetch(`/${type}`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(data)
    });
    let result = await response.json();
    if ("error" in result){
        openErrorWarning()
    }
    return result
}


async function process(type, inputData){
    let response = await server({type: type, input: inputData}, "process");
    return response;
}




