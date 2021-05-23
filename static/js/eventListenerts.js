genCloseBtn.addEventListener("click", ()=>{
    closeGenWindow()
})

genGenBtn.addEventListener("click", genNum)

function openPopUp(domEL){
    domEL.classList.remove("hide");
    dark.classList.remove("hide");
    domEL.style.top = pageYOffset + (window.innerHeight - domEL.getBoundingClientRect().height) / 2 + "px";
    document.body.classList.add("scollBlock")
}

function closePopUp(domEl){
    document.body.classList.remove("scollBlock");
    domEl.classList.add("opacity_zero_slow");
    dark.classList.add("opacity_zero_slow");
    setTimeout(()=>{
        domEl.classList.add("hide");
        dark.classList.add("hide");
        domEl.classList.remove("opacity_zero_slow");
        dark.classList.remove("opacity_zero_slow");
    },200)
}

function drawGenPol(pol){
    currentGenField.innerHTML = "<div class=\"pylynom_add_el\">+</div>";
    for(let i = pol.length - 1; i >= 0; i--){
        let html = `
                <div class="input_element_polynom__part">
                    <div class="polynom_mul">
                        <input class="polynom_mul_top" type="text" value="${pol[i][0][0]}">
                            <br>
                        <div class="polynom_sep"></div>
                        <input class="polynom_mul_bottom" type="text" value="${pol[i][0][1]}">
                    </div>
                    <div class="polynom_x">x</div>
                    <sup><input class="polynom_deg" type="text" value="${pol[i][1]}"></sup>
                </div>
        `
        if(i !== 0){
            html = `<div class="pylynom_plus">+</div>` + html;
        }
        currentGenField.insertAdjacentHTML("afterbegin", html);
    }
    inputButtonsRefresh();
}


function closeGenWindow(){
    closePopUp(genWindow);
    document.getElementsByName("sign").forEach((el, i)=>{
        if(i === 0){
            el.checked = true;
        } else{
            el.checked = false;
        }
    })
}

function openErrorWarning(){
    openPopUp(errorWarning);
}

function closeErrorWarning(){
    closePopUp(errorWarning);
}

function openResultWindow(){
    openPopUp(resultWindow);
}

function closeResultWindow(){
    closePopUp(resultWindow);
    resultField.innerHTML = "";
}

window.addEventListener("scroll", (e)=>{
    if(window.pageYOffset + window.innerHeight >= app.getBoundingClientRect().top){
        if (isDescription === 1){
            isDescription = 0;
            scrollBlock();
            window.scrollTo({
                top: app.getBoundingClientRect().top + 100,
                behavior: "smooth",
            })
            setTimeout(()=>{
                scrollAllow();
            },1000)
        }
    } else {
        if (isDescription === 0){
            isDescription = 1
            //document.body.classList.remove("scollBlock");
        }

    }
})


select.addEventListener("change", async ()=>{
    let res = await getFieldInfo()
    createInputFields(res);
})



errorAgainButton.addEventListener("click", closeErrorWarning)

bgc_video_size();

sendButton.addEventListener("click", serverProcess);

resultButton.addEventListener("click", closeResultWindow)