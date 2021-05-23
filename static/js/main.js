const select = document.querySelector("#option_select");
const errorAgainButton = document.querySelector("#try_again");
const errorWarning = document.querySelector(".smth_went_wrong");
const dark = document.querySelector(".dark");
const description = document.querySelector(".description");
const video = document.querySelector(".background_video__media");
const app = document.querySelector("#app");
const genGenBtn = document.querySelector("#gen_gen");
const genCloseBtn = document.querySelector("#gen_close");
const genWindow = document.querySelector(".gen_window");
let genWindowOpenBtns = document.querySelectorAll(".input_element_gen");
let genWindowClearBtns = document.querySelectorAll(".input_element_clear");
let polynomAddElBtn = document.querySelectorAll(".pylynom_add_el");
let  polynomClear = document.querySelectorAll(".input_polynom_clear");
const input_data = document.querySelector(".input_data");
const sendButton = document.querySelector(".app_send_btn");
const resultWindow = document.querySelector(".result_window");
const resultButton = document.querySelector(".result_button");
const resultField = document.querySelector(".result_field");
const loading = document.querySelector(".loading");

window.onload = bgc_video_size;

let currentGenField;
let isDescription= 1;
let reqFields = ["N", "N"];

function resultWidth(){
    let width = 0;
    for(let i = 0; i < resultField.children.length; i++){
        width += resultField.children[i].getBoundingClientRect().width;
    }
    console.log(width)
    if(width >= 400){
        resultField.classList.add("result_field_justify-left");
    } else{
        resultField.classList.remove("result_field_justify-left");
    }
}


function bgc_video_size(){
    let height =  description.getBoundingClientRect().height;
    let videoWidth = video.getBoundingClientRect().width;
    console.log(height, videoWidth)
    video.style.top =`${height - videoWidth * 3 / 4}px`;
}

function scrollBlock(){
    app.style = `margin-right: ${window.innerWidth - document.body.offsetWidth}px`;
    document.body.classList.add("scollBlock");
}
function scrollAllow(){
    app.style = `margin-right: 0px`;
    document.body.classList.remove("scollBlock");
}


async function genNum(){
    let gen_input_field = document.querySelector(".gen_input_field");
    let radios = document.getElementsByName('sign');
    let sign;
    let type = select.value.slice(0,1)
    if(gen_input_field.value !== ""){
        radios.forEach(el =>{
            if(el.checked){
                sign = el.value;
            }
        })
        let response = await server({len: gen_input_field.value, sign: sign, gen_type: type}, "gen")
        if (type !== "P"){
            currentGenField.value = response.generated;
        } else {
            console.log(response.generated);
            drawGenPol(response.generated);
        }

        gen_input_field.value = "";
        closeGenWindow();

    }else{
        alert("Введите число!");
    }
}
async function getFieldInfo() {
    let func = select.value
    let response = await server({type: func}, "getInfo")
    reqFields = response.argsTypes;
    return response
}
async function createInputFields(response){
    await response;
    input_data.innerHTML = "";
    if(!("error" in response)){
        response.argsTypes.forEach((el, i) =>{
            if(el !== "P"){
                input_data.insertAdjacentHTML("beforeend", `
                        <div class="input_element_number" data-type=${el}>
                            <div class="input_element__auxiliary">
                                <div class="input_element_title">
                                    ${response.argsDesc[i]}
                                </div>
                                <div class="input_element_gen">
                                    G
                                </div>
                                 <div class="input_element_clear">x</div>
                            </div>
                            <input type="text" class="input_field">
                        </div>`)
            } else{
                
                input_data.insertAdjacentHTML("beforeend", `
                                    <div class="input_element_polynom">
                                        <div class="input_element__auxiliary input_polynom__auxiliary">
                                            <div class="input_element_title">
                                                ${response.argsDesc[i]}
                                            </div>
                                            <div class="input_element_gen">
                                                G
                                            </div>
                                            <div class="input_polynom_clear">x</div>
                    
                                        </div>
                    
                                        <div class="input_element_polynom__parts">
                                            <div class="input_element_polynom__part">
                                                <div class="polynom_mul">
                                                    <input class="polynom_mul_top" type="text">
                                                        <br>
                                                            <div class="polynom_sep"></div>
                                                            <input class="polynom_mul_bottom" type="text">
                                                </div>
                                                <div class="polynom_x">x</div>
                                                <sup><input class="polynom_deg" type="text"></sup>
                                            </div>
                    
                                            <div class="pylynom_add_el">+</div>
                                        </div>
                </div>`)
            }
        })

        inputButtonsRefresh();
    }

}

function testAddPoly(){
    input_data.insertAdjacentHTML("beforeend", `
                                    <div class="input_element_polynom">
                                        <div class="input_element__auxiliary input_polynom__auxiliary">
                                            <div class="input_element_title">
                                                Многочлен 1
                                            </div>
                                            <div class="input_element_gen">
                                                G
                                            </div>
                                            <div class="input_polynom_clear">x</div>

                                        </div>

                                        <div class="input_element_polynom__parts">
                                            <div class="input_element_polynom__part">
                                                <div class="polynom_mul">
                                                    <input class="polynom_mul_top" type="text">
                                                        <br>
                                                            <div class="polynom_sep"></div>
                                                            <input class="polynom_mul_bottom" type="text">
                                                </div>
                                                <div class="polynom_x">x</div>
                                                <sup><input class="polynom_deg" type="text"></sup>
                                            </div>

                                            <div class="pylynom_add_el">+</div>
                                        </div>
                </div>`)
    inputButtonsRefresh();
}

function addPolEl(e){
    const html = `
                    <div class="pylynom_plus">+</div>
                    <div class="input_element_polynom__part">
                        <div class="polynom_mul">
                            <input class="polynom_mul_top" type="text">
                            <br>
                            <div class="polynom_sep"></div>
                            <input class="polynom_mul_bottom" type="text">
                        </div>
                        
                        <div class="polynom_x">x</div>
                        <sup><input class="polynom_deg" type="text"></sup>
                    </div>`
    e.target.insertAdjacentHTML("beforebegin", html);
}

function removePolEl(e){
    const partsList = e.target.parentNode.parentNode.children[1].children;
    if(partsList.length > 2){
        partsList[partsList.length - 2].previousElementSibling.remove();
        partsList[partsList.length - 2].remove();
    }
}

function inputButtonsRefresh(){
    polynomClear = document.querySelectorAll(".input_polynom_clear");
    polynomAddElBtn = document.querySelectorAll(".pylynom_add_el");
    genWindowOpenBtns = document.querySelectorAll(".input_element_gen");
    genWindowClearBtns = document.querySelectorAll(".input_element_clear");
    genWindowOpenBtns.forEach(el => {
        el.addEventListener("click", ()=>{
            let type = el.parentNode.parentNode.dataset.type;
            console.log(type == "N")
            if(type === "N" || type === "i+"){
                document.querySelector("#minusSign").disabled = true;
                document.querySelector("#randomSign").disabled = true;
                document.querySelector(".minusSign_label").classList.add("disabled_label");
                document.querySelector(".randomSign_label").classList.add("disabled_label");
            } else {
                document.querySelector("#minusSign").disabled = false;
                document.querySelector("#randomSign").disabled = false;
                document.querySelector(".minusSign_label").classList.remove("disabled_label");
                document.querySelector(".randomSign_label").classList.remove("disabled_label");
            }
            genWindow.classList.remove("hide");
            dark.classList.remove("hide");
            genWindow.style.top = pageYOffset + (window.innerHeight - genWindow.getBoundingClientRect().height) / 2 + "px";
            document.body.classList.add("scollBlock")
            currentGenField = el.parentNode.parentNode.children[1];
        });
    })


    genWindowClearBtns.forEach(el =>{
        el.addEventListener("click", ()=>{
            currentGenField = el.parentNode.parentNode.children[1].value = "";
        })
    })

    polynomAddElBtn.forEach(el=> {
        el.removeEventListener("click", addPolEl)
    })

    polynomAddElBtn.forEach(el=> {
        el.addEventListener("click", addPolEl)
    })

    polynomClear.forEach(el => {
        el.removeEventListener("click", removePolEl)
    })

    polynomClear.forEach(el => {
        el.addEventListener("click", removePolEl)
    })
}
inputButtonsRefresh();

let desc = [
    "Сравнение натуральных чисел",
    "Проверка на ноль",
    "Добавление 1 к натуральному числу",
    "Сложение натуральных чисел",
    "Вычитание из первого большего натурального <br>числа второго меньшего или равного",
    "Умножение натурального числа на цифру",
    "Умножение натурального числа на 10^k",
    "Умножение натуральных чисел",
    "Вычитание из натурального другого,<br> умноженного на цифру для случая <br> с неотрицательным результатом",
    "Вычисление первой цифры деления большего <br>на меньшее, домноженное на 10^k, <br> k - номер позиции этой цифры",
    "Частное от деления большего натурального числа на меньшее<br> или равное натуральное с остатком",
    "Остаток от деления большего натурального <br>числа на меньшее или равное натуральное с остатком",
    "НОД натуральных чисел",
    "НОК натуральных чисел",
    "Абсолютная величина числа, результат - натуральное",
    "Определение положительности числа",
    "Умножение целого на (-1)",
    "Преобразование натурального в целое",
    "Преобразование целого неотрицательного в натуральное",
    "Сложение целых чисел",
    "Вычитание целых чисел",
    "Умножение целых чисел",
    "Частное от деления целого на целое",
    "Остаток от деления целого на",
    "Сокращение дроби",
    "Проверка на целое, если рациональное число является целым",
    "Преобразование целого в дробное",
    "Преобразование дробного в целое (если знаменатель равен 1)",
    "Сложение дробей",
    "Вычитание дробей",
    "Умножение дробей",
    "Деление дробей",
    "Сложение многочленов",
    "Вычитание многочленов",
    "Умножение многочлена на рациональное число",
    "Умножение многочлена на x^k",
    "Старший коэффициент многочлена",
    "Степень многочлена",
    "Вынесение из многочлена НОК знаменателей <br> коэффициентов и НОД числителей",
    "Умножение многочленов",
    "Частное от деления многочлена <br>на многочлен при делении с остатком",
    "Остаток от деления многочлена <br> на многочлен при делении с остатком",
    "НОД многочленов",
    "Производная многочлена",
    "Преобразование многочлена — кратные корни в простые",
]

function createFuncsList(){
    desc.forEach((el, i)=>{
        if(i === 0){
            select.insertAdjacentHTML("beforeend", "<optgroup label=\"Натуральные числа\"></optgroup>")
        } else if(i === 14){
            select.insertAdjacentHTML("beforeend", "<optgroup label=\"Целые числа числа\"></optgroup>")
        }   else if(i === 24){
            select.insertAdjacentHTML("beforeend", "<optgroup label=\"Рациональные числа\"></optgroup>")
        }   else if(i === 32){
            select.insertAdjacentHTML("beforeend", "<optgroup label=\"Многочлены\"></optgroup>")
        }
        if(i < 14){
            select.children[0].insertAdjacentHTML("beforeend", `<option value="N-${i + 1}">${el}</option>`)
        }
        else if(i < 24){
            select.children[1].insertAdjacentHTML("beforeend", `<option value="Z-${i + 1 - 14}">${el}</option>`)
        }
        else if(i < 32){
            select.children[2].insertAdjacentHTML("beforeend", `<option value="Q-${i + 1 - 24}">${el}</option>`)
        }
        else if(i < 45){
            select.children[3].insertAdjacentHTML("beforeend", `<option value="P-${i + 1 - 32}">${el}</option>`)
        }
    })
}

createFuncsList()

//bgc_video_size();

function grabPols(){
    let inputData = []
    let parts = document.querySelectorAll(".input_element_polynom__parts");
    let isError = 0;
    for(let i = 0; i < parts.length && isError === 0; i++){
        let pols = parts[i].children;
        let polynom = []
        for(let j = 0; j < pols.length - 1 && isError === 0; j += 2){
            console.log(pols[j].children)
            let mul_top = pols[j].children[0].children[0].value
            let mul_bottom = pols[j].children[0].children[3].value
            let deg = pols[j].children[2].children[0].value

            if(mul_bottom === "" || mul_top === "" || deg === ""){
                console.log("log is", mul_bottom, mul_top, deg);
                console.log("error")
                isError = 1;
            }
            polynom.push([[mul_top, mul_bottom], deg])
        }
        inputData.push(polynom)
    }

    console.log(inputData)
    return {inputData, isError};
}
function grabNumbers(){
    let inputData = []
    let isError;
    for(let i = 0; i < input_data.children.length; i++){
        if(input_data.children[i].classList.value !== "input_element_polynom"){
            if( input_data.children[i].children[1].value === "" ||
                input_data.children[i].children[1].value === "Введите данные"){

                input_data.children[i].children[1].value = "Введите данные"
                isError = 1;
                break
            }
            else {
                inputData.push(input_data.children[i].children[1].value);
            }
        }

    }
    return {inputData, isError}
}
function prepareFraction(inputData){
    let fractionData = [];
    for(let i = 0; i < inputData.length; i++){
        if(i % 2 === 0){
            fractionData.push([])
        }
        fractionData[fractionData.length - 1].push(inputData[i])
    }

    return fractionData
}


function drawNumRes(num){
    resultField.insertAdjacentHTML("beforeend", `<p>${num}</p>`);
}
function drawFracRes(num1, num2){
    resultField.insertAdjacentHTML("beforeend", `
                         <div class="result_fraction">
                            <div class="result_fraction__top">${num1}</div>
                            <br>
                            <div class="result_fraction__sep"></div>
                            <div class="result_fraction__bottom">${num2}</div>
                        </div>
                `)
}
function drawResPol(pol){
    pol.forEach((el, i)=>{
        let html = ``;
        if(el[0][0][0] === "-"){
            el[0][0] = el[0][0].replace("-", " ")
            console.log(el[0][0])
            html = `<div class="pylynom_plus">-</div>` + html;
        } else if(i !== 0){
            html = `<div class="pylynom_plus">+</div>` + html
        }
        html +=  `
                         <div class="result_fraction">
                            <div class="result_fraction__top">${el[0][0]}</div>
                            <br>
                            <div class="result_fraction__sep"></div>
                            <div class="result_fraction__bottom">${el[0][1]}</div>
                        </div>
                        <div class="result_x">
                                <sup><div class="result_deg">${el[1]}</div></sup>
                                <div class="result_x_x">x</div>
                         
                        </div>
                `

        resultField.insertAdjacentHTML("beforeend", html)
    })
}
function drawBracket(side){
    if(side === "left"){
        resultField.insertAdjacentHTML("beforeend", "<div class=\"result_bracket result_bracket__left\"></div>")
    } else if (side === "right"){
        resultField.insertAdjacentHTML("beforeend", "<div class=\"result_bracket result_bracket__right\"></div>")
    }

}

async function serverProcess(){
    let type = select.value;
    let inputData = []
    let isError = 0;
    console.log("reqField", reqFields);
    if(!reqFields.includes("P")){
        let res = grabNumbers();
        inputData = res.inputData
        isError = res.isError

        if(type.slice(0, 1) === "Q"){
            inputData = prepareFraction(inputData)
        }
    } else {
        let res = grabPols()
        isError = res.isError;
        inputData = res.inputData;
        console.log("isError", isError, res.isError)
        let isN = 0;
        let isQ = 0;
        if(reqFields.includes("Q")){
            isQ = 1;
        } else if(reqFields.includes("i+")){
            isN = 1;
        }
        console.log(reqFields, isN, isQ)

        if (isN || isQ){
            let nData = [];
            let res = grabNumbers()
            nData = res.inputData;
            isError = res.isError;
            console.log("nData", nData)
            if (isQ){
                nData = prepareFraction(nData)
            }
            console.log("nDataPrepared", nData)
            nData.forEach(el => {
                inputData.push(el);
            })
        }
    }
    console.log("input data", inputData)

    if(isError !== 1){
        sendButton.classList.add("hide");
        loading.classList.remove("hide");

        let response = await process(type, inputData)

        sendButton.classList.remove("hide");
        loading.classList.add("hide");

        if(response.error !== -1){
            openResultWindow()
            if (type.slice(0, 1) !== "Q" && type.slice(0, 1) !== "P"){
                drawNumRes(response.result);
                //resultField.innerHTML = `<p>${response.result}</p>`
            } else if  (type.slice(0, 1) === "Q"){
                drawFracRes(response.result[0], response.result[1]);
            } else {
                if(type === "P-6"){
                    drawNumRes(response.result)
                } else if(type === "P-5"){
                    drawFracRes(response.result[0], response.result[1])
                }  else if(type === "P-7"){
                    drawFracRes(response.result[0][0], response.result[0][1])
                    drawBracket("left")
                    drawResPol(response.result[1])
                    drawBracket("right")
                }else {
                    drawResPol(response.result)
                }


            }
            resultWidth()
        }
    }else{
        alert("Input data error");
    }
}